import json, subprocess, sys
with open("dash_data.json") as f:
    data = json.load(f)
js = json.dumps(data)
r = subprocess.run(["python3", "build_dashboard.py", js], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
print("rc", r.returncode)
