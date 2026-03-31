import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Prevent pytest from collecting src/ functions whose names start with test_
collect_ignore_glob = ["src/*"]
collect_ignore = ["src"]
