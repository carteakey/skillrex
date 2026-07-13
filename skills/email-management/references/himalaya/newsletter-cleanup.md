# Newsletter Cleanup — Full Script Template

Automated cleanup of email accounts by moving newsletters from the Inbox to a specific folder using optimized search queries and batch operations.

## Optimized Workflow

### 1. Identify and Verify Target Folders
Determine the correct path for the destination folder using JSON output for safe parsing in scripts.
```bash
himalaya folder list --account <name> --output json
```
Check if the target folder (e.g., `Newsletters` or `Updates/Newsletters`) exists before attempting moves.

### 2. Native Search Query (Recommended)
Use `himalaya` native search syntax to find only the relevant emails. This is much faster than fetching all envelopes and filtering in Python.
```bash
himalaya --quiet envelope list --account <name> --page-size 1000 --output json "from substack.com or from medium.com or from beehiiv.com"
```

### 3. Batch Move
Pass multiple IDs as strings in a single command to move emails efficiently.
```bash
himalaya --quiet message move --account <name> <DEST_FOLDER> <ID1> <ID2> <ID3>...
```

## Newsletter Domains
Common newsletter domains to target:
- substack.com, medium.com, beehiiv.com, luma-mail.com
- promo.thestar.com, birds.cornell.edu, aitinkerers.org
- analyticsvidhya.com, capacities.io

## Pitfalls
- **Search Query Specificity**: Native `from <domain>` search queries are highly efficient but behavior varies by backend. Some IMAP servers require the full email address or don't support partial domain matches. Fall back to Python: `addr.lower().endswith(domain.lower())`.
- **ID String Conversion**: When building batch commands in Python, ensure all envelope IDs are converted to strings: `[str(id) for id in ids]`.
- **Target Folder Position**: The target folder name MUST come before the envelope IDs in the `move` command.
- **Buffer/Size Limits**: Large JSON responses (e.g., `--page-size 1000`) can exceed terminal output buffers. Use pagination (100-200) and loop.

## Full Script Template
```python
import subprocess
import json

himalaya_cmd = 'himalaya'
newsletter_domains = [
    "substack.com", "medium.com", "beehiiv.com", "luma-mail.com",
    "promo.thestar.com", "birds.cornell.edu", "aitinkerers.org",
    "analyticsvidhya.com", "capacities.io"
]
accounts = ['personal', 'primary']
dest_folder = 'Newsletters'

conditions = [f"from {domain}" for domain in newsletter_domains]
query = " or ".join(conditions)

for account in accounts:
    print(f"Cleaning up {account}...")
    total_moved = 0
    while True:
        cmd = [himalaya_cmd, 'envelope', 'list', '--account', account, '--page-size', '1000', '--output', 'json', query]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            break
        start_idx = res.stdout.find('[')
        if start_idx == -1:
            break
        try:
            data = json.loads(res.stdout[start_idx:], strict=False)
        except Exception as e:
            print(f"  Failed to parse JSON: {e}")
            break
        ids = [email['id'] for email in data]
        if not ids:
            break
        move_cmd = [himalaya_cmd, 'message', 'move', '--account', account, dest_folder] + ids
        move_res = subprocess.run(move_cmd, capture_output=True, text=True)
        if move_res.returncode == 0:
            total_moved += len(ids)
            print(f"  Moved batch of {len(ids)} emails.")
        elif "folder not found" in move_res.stderr.lower():
            print(f"  Folder {dest_folder} missing, creating it...")
            subprocess.run([himalaya_cmd, 'folder', 'add', '--account', account, dest_folder])
            if subprocess.run(move_cmd, capture_output=True).returncode == 0:
                total_moved += len(ids)
                print(f"  Moved batch of {len(ids)} emails after folder creation.")
            else:
                print(f"  Batch move failed: {move_res.stderr}")
                break
    print(f"Finished {account}. Total moved: {total_moved}")
```
