import subprocess
import json

himalaya_cmd = '/home/kchauhan/.local/bin/himalaya'

newsletter_domains = [
    "substack.com",
    "medium.com",
    "beehiiv.com",
    "luma-mail.com",
    "promo.thestar.com",
    "birds.cornell.edu",
    "mail.aitinkerers.org",
    "newsletters.analyticsvidhya.com",
    "capacities.io"
]

accounts = ['personal', 'primary']

for account in accounts:
    print(f"Scanning '{account}' Inbox for newsletters...")
    result = subprocess.run([himalaya_cmd, '--account', account, 'envelope', 'list', '--page-size', '500', '--output', 'json'], capture_output=True, text=True)
    
    try:
        start_idx = result.stdout.find('[')
        if start_idx != -1:
            data = json.loads(result.stdout[start_idx:])
            to_move = []
            for email in data:
                addr = email.get('from', {}).get('addr', '')
                is_newsletter = any(addr.endswith(domain) for domain in newsletter_domains)
                if is_newsletter:
                    to_move.append(email['id'])
            
            print(f"Found {len(to_move)} newsletter emails to move in {account}.")
            
            moved_count = 0
            for msg_id in to_move:
                subprocess.run([himalaya_cmd, '--account', account, 'message', 'move', str(msg_id), 'Newsletters'])
                moved_count += 1
                
            print(f"Successfully moved {moved_count} emails to the 'Newsletters' folder in {account}!\n")
        else:
            print(f"No emails found or failed to parse for {account}.\n")
    except Exception as e:
        print(f"Error during move process for {account}: {e}\n")
