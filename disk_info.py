from system_commands import run_command


def get_disk_info(target="/"):
    output = run_command(["diskutil", "info", target])

    disk_info = {}

    for line in output.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip()
        value = value.strip()

        disk_info[key] = value

    return disk_info

def get_physical_disks():
    output = run_command(["diskutil", "list"])

    physical_disks = []

    for line in output.splitlines():
        line = line.strip()

        if line.startswith("/dev/") and "(internal, physical)" in line:
            device = line.split()[0]
            physical_disks.append(device)

        elif line.startswith("/dev/") and "(external, physical)" in line:
            device = line.split()[0]
            physical_disks.append(device)

    return physical_disks


def get_drive_type(solid_state):
    if solid_state == "Yes":
        return "SSD"
    elif solid_state == "No":
        return "HDD"
    else:
        return "Unknown"


def clean_capacity(capacity):
    if not capacity:
        return "Unknown"

    return capacity.split(" (")[0]


def get_physical_disk_info(device):
    disk = get_disk_info(device)

    return {
        "device": disk.get("Device Identifier"),
        "name": disk.get("Device / Media Name"),
        "capacity": clean_capacity(disk.get("Disk Size")),
        "protocol": disk.get("Protocol"),
        "smart_status": disk.get("SMART Status"),
        "location": disk.get("Device Location"),
        "drive_type": get_drive_type(disk.get("Solid State")),
        "virtual": disk.get("Virtual"),
        "read_only": disk.get("Media Read-Only")
    }


if __name__ == "__main__":
    disks = get_physical_disks()

    print("=" * 50)
    print("PHYSICAL DISK INVENTORY")
    print("=" * 50)

    for device in disks:
        disk = get_physical_disk_info(device)

        print("\n" + "-" * 50)

        for key, value in disk.items():
            print(f"{key}: {value}")
