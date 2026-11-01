import json, subprocess

with open('dashboard_payload.json') as f:
    d = json.load(f)
js = json.dumps(d)
r = subprocess.run(['python3', 'build_dashboard.py', js], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
print('RC', r.returncode)
