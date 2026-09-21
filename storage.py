
import psutil


def get_storage_info():
    partitions = psutil.disk_partitions()

    storage = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            disk_info = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total_gb": round(usage.total / (1024 ** 3), 2),
                "used_gb": round(usage.used / (1024 ** 3), 2),
                "free_gb": round(usage.free / (1024 ** 3), 2),
                "usage_percent": usage.percent
            }

            storage.append(disk_info)

        except PermissionError:
            continue

    return storage

def get_reportable_storage():
    storage = get_storage_info()

    reportable = []

    excluded_mounts = [
        "/System/Volumes/",
        "/Library/Developer/CoreSimulator/"
    ]

    for disk in storage:
        mountpoint = disk["mountpoint"]

        if mountpoint == "/":
            reportable.append(disk)
            continue

        if any(mountpoint.startswith(path) for path in excluded_mounts):
            continue

        reportable.append(disk)

    return reportable

if __name__ == "__main__":
    disks = get_reportable_storage()

    print("=" * 50)
    print("STORAGE INVENTORY")
    print("=" * 50)

    for disk in disks:
        print(f"\nDevice: {disk['device']}")
        print(f"Mount Point: {disk['mountpoint']}")
        print(f"Filesystem: {disk['filesystem']}")
        print(f"Total: {disk['total_gb']} GB")
        print(f"Used: {disk['used_gb']} GB")
        print(f"Free: {disk['free_gb']} GB")
        print(f"Usage: {disk['usage_percent']}%")
