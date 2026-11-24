import json, subprocess, pathlib

data_path = pathlib.Path("/Users/michael/.hermes/profiles/wellness/wellness-dashboard/dash_data_20261124.json")
payload = data_path.read_text()
# validate JSON
json.loads(payload)

result = subprocess.run(
    ["python3", "build_dashboard.py", payload],
    cwd="/Users/michael/.hermes/profiles/wellness/wellness-dashboard",
    capture_output=True, text=True
)
print("returncode", result.returncode)
print("stdout", result.stdout)
print("stderr", result.stderr)
