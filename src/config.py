from pathlib import Path
from typing import List


# Root of this repo
REPO_ROOT = Path(__file__).resolve().parents[1]

def _detect_bids_root() -> Path:
    """优先使用 `data/raw/ds004147`，若不存在则回退到 `原/ds004147`。
    这样即使你尚未移动数据，也能一键运行；当你把数据放到 data/raw 后将自动使用该路径。
    """
    candidates = [
        REPO_ROOT / "data" / "raw" / "ds004147",
        REPO_ROOT / "原" / "ds004147",
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]

# Default BIDS root (autodetected)
BIDS_ROOT = _detect_bids_root()

# Output folders
FIGURES_DIR = REPO_ROOT / "figures"
RESULTS_DIR = REPO_ROOT / "results"


def ensure_dirs() -> None:
    """Create commonly used output directories if missing."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def list_subjects() -> List[str]:
    """Return available BIDS subject IDs (without 'sub-' prefix)."""
    if not BIDS_ROOT.exists():
        return []
    subs = sorted(p.name.replace("sub-", "") for p in (BIDS_ROOT.glob("sub-*")) if p.is_dir())
    return subs
