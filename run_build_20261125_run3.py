import json, subprocess, sys

with open("/Users/michael/.hermes/profiles/wellness/cache/scratch/dash_payload_20261125_run3.json") as f:
    data = json.load(f)

payload = json.dumps(data)
result = subprocess.run(
    ["python3", "build_dashboard.py", payload],
    cwd="/Users/michael/.hermes/profiles/wellness/wellness-dashboard",
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr)
sys.exit(result.returncode)
