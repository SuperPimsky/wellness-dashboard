import json
import subprocess
import sys

with open("payload_20261125_run2.json") as f:
    data = json.load(f)

json_str = json.dumps(data)
result = subprocess.run(
    ["python3", "build_dashboard.py", json_str],
    cwd="/Users/michael/.hermes/profiles/wellness/wellness-dashboard",
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
sys.exit(result.returncode)
