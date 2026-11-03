"""Entry point: `python -m calorie_tracker ...`."""

import sys

from .cli import run

if __name__ == "__main__":
    sys.exit(run())