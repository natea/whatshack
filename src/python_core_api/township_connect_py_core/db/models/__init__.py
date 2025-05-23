"""township_connect_py_core models."""

import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="township_connect_py_core.db.models.",
    )
    for module in modules:
        __import__(module.name)
