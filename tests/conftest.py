import sys
import pathlib

# Ensure project root is on sys.path for imports
project_root = pathlib.Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))