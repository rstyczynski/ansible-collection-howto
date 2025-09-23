#!/usr/bin/env python3
import yaml
import sys

if len(sys.argv) < 2:
    print("Usage: clean_requirements.py <input_file>", file=sys.stderr)
    sys.exit(1)

infile = sys.argv[1]

with open(infile, "r") as f:
    data = yaml.safe_load(f)

# Keep only entries where type is "dir" or "git"
filtered = []
for c in data.get("collections", []):
    if c.get("type") in ("dir", "git"):
        filtered.append(c)

data["collections"] = filtered

# Keep only roles with src starting with "git+" or "https://" or type "dir"
filtered_roles = []
for r in data.get("roles", []):
    if isinstance(r, dict):
        if r.get("src", "").startswith("git+") or r.get("src", "").startswith("https://") or r.get("type") == "dir":
            filtered_roles.append(r)

data["roles"] = filtered_roles

yaml.dump(data, sys.stdout, sort_keys=False, explicit_start=True)
