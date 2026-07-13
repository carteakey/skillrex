# Security/OTP Cleanup — Full Reference

Robust workflow for identifying and archiving security, OTP, and login emails from the INBOX using paged fetching and robust JSON parsing.

## Identification Logic

### Security Keywords (Inclusions)
- `verification code`, `one time password`, `(otp)`
- `security alert`, `new login`, `magic sign in code`
- `validate your account`, `password reset`, `verify your email`
- `unusual sign-in activity`, `new device logged in`
- `verify your identity`, `action required: new login`
- `login code`, `apple account was used to sign in`
- `security code`, `verification pin`, `one-time password`
- `authorized`, `access code`, `sign-in`, `logged in`, `identity`, `unusual activity`

### Exclusions (False Positives)
- `re:`, `fwd:`, `fw:` (conversations about security)
- `renewal`, `payout`, `credit card failed` (transactional/billing)
- `itinerary`, `departure`, `booking` (travel)
- `interac e-transfer` (financial transactions)
- `expire soon`, `statement`

### Security Matching Pattern
```python
def is_security_email(subject, sender):
    if not subject: subject = ""
    if not sender: sender = ""
    subj = subject.lower()

    # EXCLUSIONS (False Positives)
    if subj.startswith('re:') or subj.startswith('fwd:') or subj.startswith('fw:'):
        return False
    if any(x in subj for x in ['renewal', 'payout', 'credit card failed', 'itinerary',
                                 'departure', 'booking', 'expire soon', 'interac e-transfer']):
        return False

    # INCLUSIONS (Valid Security/OTP)
    security_keywords = [
        'verification code', 'one time password', 'otp', 'security alert', 'new login',
        'magic sign in code', 'validate your account', 'password reset', 'verify your email',
        'verify your identity', 'action required: new login', 'unusual sign-in activity',
        'login code', 'apple account was used to sign in', 'new device logged in',
        'security code', 'verification pin', 'one-time password', 'authorized',
        'access code', 'sign-in', 'logged in', 'identity', 'unusual activity'
    ]
    for kw in security_keywords:
        if kw in subj: return True
    if 'mcafee' in sender.lower() and 'alert' in subj: return True
    return False
```

## Workflow
1. **Account Discovery**: List active accounts to ensure the script targets the correct mailboxes.
2. **Folder Preparation**: Ensure the target folder (e.g., `Admin/Security Logs`) exists.
3. **Paged Fetching**: Fetch emails in chunks (50-100) to avoid malformed/truncated JSON.
4. **Identification Logic**: Filter by security keywords while excluding false positives.
5. **Age Verification**: Calculate email age using UTC-aware date parsing.
6. **Chunked Move**: Move identified emails in batches of 50 to the target folder.
