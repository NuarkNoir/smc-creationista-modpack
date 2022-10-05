import pathlib
import re
import sys

packfile = pathlib.Path("pack.toml")

rx = re.compile(r"version = \"(\d+).(\d+).(\d+)\"")

with open(packfile, "r") as f:
    text = f.read()
    matches = rx.search(text)
    if matches is None:
        print("No version found")
        sys.exit(1)
    mj, mn, pt = matches.groups()
    updated_text = re.sub(rx, f'version = "{mj}.{mn}.{int(pt)+1}"', text)

with open(packfile, "w") as f:
    f.write(updated_text)
