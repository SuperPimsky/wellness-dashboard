import json
import subprocess
import sys

with open("/Users/michael/.hermes/profiles/wellness/wellness-dashboard/cron_payload_20261128_1222.json") as f:
    payload = json.load(f)

json_str = json.dumps(payload)
result = subprocess.run(
    ["python3", "build_dashboard.py", json_str],
    cwd="/Users/michael/.hermes/profiles/wellness/wellness-dashboard",
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("RC:", result.returncode)
