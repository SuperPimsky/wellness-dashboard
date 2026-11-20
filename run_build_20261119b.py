import json, subprocess, sys
with open("/Users/michael/.hermes/profiles/wellness/wellness-dashboard/cron_payload_20261119b.json") as f:
    payload = json.load(f)
js = json.dumps(payload)
r = subprocess.run(
    ["python3", "build_dashboard.py", js],
    cwd="/Users/michael/.hermes/profiles/wellness/wellness-dashboard",
    capture_output=True, text=True
)
print("RC", r.returncode)
print(r.stdout[-2000:])
print(r.stderr[-2000:])
