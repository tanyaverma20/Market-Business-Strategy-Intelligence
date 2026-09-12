from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

print(f"Project root: {ROOT}")
print(f"Python path inserted: {SRC}")
result = pytest.main(["-q"])
print(f"Pytest exit code: {result}")
raise SystemExit(result)
