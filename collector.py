import json
import os
from datetime import datetime, timezone

DATA_FILE = "collector_results.json"


def save_result(value):
    """Aviator raund natijasini tarixga saqlaydi."""
    try:
        value = float(value)
        if value < 1:
            return False

        data = []

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.append({
            "value": round(value, 2),
            "time": datetime.now(timezone.utc).isoformat()
        })

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except (ValueError, OSError, json.JSONDecodeError):
        return False
