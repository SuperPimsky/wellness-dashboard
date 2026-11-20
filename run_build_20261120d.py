import json, subprocess, sys

with open("cron_payload_20261120d.json") as f:
    payload = json.load(f)

json_str = json.dumps(payload)
result = subprocess.run(
    [sys.executable, "build_dashboard.py", json_str],
    cwd="/Users/michael/.hermes/profiles/wellness/wellness-dashboard",
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr)
print("returncode", result.returncode)
