from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PACKAGE_DIR.parent
PROJECT_ROOT = SRC_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
DEMO_DIR = PROJECT_ROOT / "demo"


def relative_to_root(path: Path) -> str:
    """Return a stable display path for logging and validation messages."""
    return str(path.resolve().relative_to(PROJECT_ROOT))
