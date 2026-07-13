import json
import datetime
import subprocess
import sys

def run_cmd(cmd):
    # Using subprocess instead of the agent terminal tool to allow execution via terminal tool
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "output": result.stdout,
        "exit_code": result.returncode,
        "error": result.stderr
    }

def get_emails(account, folder="INBOX"):
    res = run_cmd(f'himalaya envelope list -a {account} -f "{folder}" --page-size 500 -o json')
    if res.get('exit_code', 1) != 0:
        return []
    try:
        output = res.get('output', '')
        # Himalaya might print some info to stdout before the JSON
        # We need to find the JSON part. Usually it's the last block or we can filter.
        # The original script had: json_str = "".join([l for l in lines if not l.startswith("2026")])
        # Let's try to find the first '[' and last ']' to get the JSON array.
        start_idx = output.find('[')
        end_idx = output.rfind(']')
        if start_idx == -1 or end_idx == -1:
            return []
        json_str = output[start_idx:end_idx+1]
        return json.loads(json_str)
    except Exception as e:
        # print(f"Error parsing JSON for {account}: {e}", file=sys.stderr)
        return []

def is_security_email(subject, sender):
    subj = subject.lower()
    
    # 1. EXCLUSIONS (False Positives)
    if subj.startswith('re:') or subj.startswith('fwd:') or subj.startswith('fw:'):
        return False
    if 'renewal' in subj or 'payout' in subj or 'credit card failed' in subj:
        return False
    if 'itinerary' in subj or 'departure' in subj or 'booking' in subj:
        return False
    if 'expire soon' in subj:
        return False
    if 'interac e-transfer' in subj:
        return False
        
    # 2. STRICT INCLUSIONS (Valid Security/OTP)
    security_keywords = [
        'verification code',
        'one time password',
        '(otp)',
        'security alert',
        'new login',
        'magic sign in code',
        'validate your account',
        'password reset',
        'verify your email',
        'verify your identity',
        'action required: new login',
        'unusual sign-in activity',
        'login code',
        'apple account was used to sign in',
        'new device logged in'
    ]
    
    for kw in security_keywords:
        if kw in subj:
            return True
            
    if 'mcafee' in sender.lower() and 'alert' in subj:
        return True
        
    return False

def is_older_than_a_day(date_str):
    try:
        # Himalaya date format might be 'Wed, 13 Jun 2026 10:00:00 +0000' or ISO
        # Let's try to parse it. If it's already ISO:
        iso_str = date_str.replace(' ', 'T')
        # If it's not ISO, we might need to handle more formats.
        # For now, let's try fromisoformat and fallback to a more general parser if needed.
        try:
            email_date = datetime.datetime.fromisoformat(iso_str)
        except ValueError:
            # Try common email date format: 'Wed, 13 Jun 2026 10:00:00 +0000'
            # This is a bit complex for a single try/except. 
            # Let's assume it's ISO-like or similar.
            # A better way would be using email.utils.parsedate_to_datetime
            import email.utils
            email_date = email.utils.parsedate_to_datetime(date_str)
            
        if email_date.tzinfo is None:
            email_date = email_date.replace(tzinfo=datetime.timezone.utc)
            
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - email_date) > datetime.timedelta(days=1)
    except Exception:
        return False 

total_moved = 0
for account in ['primary', 'personal']:
    emails = get_emails(account, "INBOX")
    to_move = []
    
    for e in emails:
        subj = e.get('subject', '')
        sender_info = e.get('from', {})
        sender = f"{sender_info.get('name', '')} {sender_info.get('address', '')}"
        date_str = e.get('date', '')
        
        if is_security_email(subj, sender) and is_older_than_a_day(date_str):
            to_move.append(str(e['id']))
            
    if to_move:
        chunk_size = 50
        for i in range(0, len(to_move), chunk_size):
            chunk = to_move[i:i+chunk_size]
            cmd = f'himalaya message move -a {account} -f "INBOX" "Admin/Security Logs" {" ".join(chunk)}'
            res = run_cmd(cmd)
            if res.get('exit_code') == 0:
                total_moved += len(chunk)

if total_moved > 0:
    print(f"Moved {total_moved} security/OTP emails older than 1 day to Admin/Security Logs.")
else:
    print("[SILENT]")
