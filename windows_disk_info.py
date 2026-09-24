import json

from system_commands import run_command


def run_powershell_json(command):
    output = run_command([
        "powershell",
        "-NoProfile",
        "-Command",
        command
    ])

    if output.startswith("Command"):
        return []

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return []

    if isinstance(data, dict):
        return [data]

    return data


def bytes_to_gb(size_bytes):
    return round(size_bytes / (1024 ** 3), 2)


def yes_no(value):
    return "Yes" if value else "No"


def get_windows_physical_disks():
    disk_command = (
        "Get-Disk | "
        "Select-Object Number,FriendlyName,BusType,"
        "HealthStatus,OperationalStatus,Size,"
        "IsReadOnly,IsOffline,Location | "
        "ConvertTo-Json"
    )

    physical_command = (
        "Get-PhysicalDisk | "
        "Select-Object DeviceId,FriendlyName,MediaType,"
        "HealthStatus,OperationalStatus,Size | "
        "ConvertTo-Json"
    )

    disks = run_powershell_json(disk_command)
    physical_disks = run_powershell_json(physical_command)

    physical_by_id = {
        str(disk["DeviceId"]): disk
        for disk in physical_disks
    }

    results = []

    for disk in disks:
        disk_number = str(disk["Number"])

        physical = physical_by_id.get(
            disk_number,
            {}
        )

        bus_type = disk.get("BusType", "Unknown")
        location = disk.get("Location", "")

        if location and location.startswith("Integrated"):
            device_location = "Internal"
        else:
            device_location = "Unknown"

        if bus_type in ("Virtual", "File Backed Virtual"):
            virtual = "Yes"
        else:
            virtual = "No"

        results.append({
            "device": f"disk{disk_number}",
            "name": disk.get("FriendlyName", "Unknown"),
            "capacity": f"{bytes_to_gb(disk["Size"])} GB",
            "protocol": bus_type,
            "smart_status": disk.get(
                "HealthStatus",
                "Unknown"
            ),
            "location": device_location,
            "drive_type": physical.get(
                "MediaType",
                "Unknown"
            ),
            "virtual": virtual,
            "read_only": yes_no(
                disk.get("IsReadOnly", False)
            )
        })
    return results


if __name__ == "__main__":
    disks = get_windows_physical_disks()

    print("=" * 50)
    print("WINDOWS PHYSICAL DISK INVENTORY")
    print("=" * 50)

    for disk in disks:
        print()

        for key, value in disk.items():
            print(f"{key}: {value}")