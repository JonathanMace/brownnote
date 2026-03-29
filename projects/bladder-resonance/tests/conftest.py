"""Configure sys.path for bladder-resonance tests."""
import sys
import os

# Add bladder-resonance project root (for bladder_model imports)
_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _project_dir not in sys.path:
    sys.path.insert(0, _project_dir)

# Add repository root (for src.analytical imports)
_repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)
