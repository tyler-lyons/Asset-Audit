import json
from pathlib import Path
from report_utils import ReportGenerationError

def save_json_report(audit, filename="asset_audit.json"):
    reports_dir = Path("reports")
    output_path = reports_dir / filename

    try:
        reports_dir.mkdir(exist_ok=True)

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(
                audit,
                file,
                indent=4,
                ensure_ascii=False
            )

    except (OSError, TypeError, ValueError) as error:
        raise ReportGenerationError(
            f"Unable to create JSON report '{output_path}': {error}"
        ) from error

    return output_path
