import json
from pathlib import Path


def save_json_report(audit, filename="asset_audit.json"):
    reports_dir = Path("reports")

    reports_dir.mkdir(exist_ok=True)

    output_path = reports_dir / filename

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            audit,
            file,
            indent=4,
            ensure_ascii=False
        )

    return output_path
