import csv
from pathlib import Path

def save_csv_reports(audit):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    system_path = reports_dir / "asset_audit_system.csv"

    with system_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Category", "Field", "Value"])

        for key, value in audit["system"].items():
               writer.writerow(["System", key, value])

        for key, value in audit["cpu"].items():
               writer.writerow(["CPU", key, value])

        for key, value in audit["memory"].items():
               writer.writerow(["Memory", key, value])

    disks_path = reports_dir / "asset_audit_disks.csv"

    with disks_path.open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "device",
            "name",
            "capacity",
            "protocol",
            "smart_status",
            "location",
            "drive_type",
            "virtual",
            "read_only"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(audit["physical_disks"])

    storage_path = reports_dir / "asset_audit_storage.csv"

    with storage_path.open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "device",
            "mountpoint",
            "filesystem",
            "total_gb",
            "used_gb",
            "free_gb",
            "usage_percent"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(audit["storage"])

    software_path = reports_dir / "asset_audit_software.csv"

    with software_path.open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "name",
            "version",
            "location"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(audit["software"])

    return system_path, disks_path, storage_path, software_path


