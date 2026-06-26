import os
import sys
import importlib.util
from pathlib import Path

spec = importlib.util.find_spec("cnhkmcp")
if not spec or not spec.submodule_search_locations:
    print("cnhkmcp not found")
    sys.exit(1)

for loc in spec.submodule_search_locations:
    loc_path = Path(loc)
    print(f"cnhkmcp location: {loc_path}")
    
    untracked = loc_path / "untracked"
    if untracked.exists():
        print(f"untracked path exists: {untracked}")
        # List contents of untracked
        for item in untracked.iterdir():
            if item.is_dir():
                print(f"  [DIR] {item.name}")
                if item.name == "skills":
                    for sub in item.iterdir():
                        print(f"    [SKILL] {sub.name}")
                        if sub.is_dir():
                            for f in sub.iterdir():
                                print(f"      - {f.name}")
            else:
                print(f"  [FILE] {item.name}")
    else:
        print("untracked path does not exist")
