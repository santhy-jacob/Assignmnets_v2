import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"


def load_json(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))
