import platform
import psutil

from windows_disk_info import get_windows_physical_disks
from windows_software import get_windows_software
from platform_utils import is_macos, is_windows
from disk_info import get_physical_disks, get_physical_disk_info
from software import get_reportable_software
from storage import get_reportable_storage
from system_commands import (
    get_computer_name,
    get_cpu_model,
    get_os_info,
)

def safe_collect(label, collector, default, errors):
    try:
        return collector()

    except Exception as error:
        errors.append(
            f"{label}: {type(error).__name__}: {error}"
        )

        return default

def get_macos_physical_disks():
    disks = []

    for device in get_physical_disks():
        disks.append(
           get_physical_disk_info(device)
        )

    return disks

def build_audit():
    os_info = get_os_info()
    memory = psutil.virtual_memory()

    physical_disks = []
    storage = []
    software = []
    errors = []

    if is_macos():
        physical_disks = safe_collect(
            "Physical disk inventory",
            get_macos_physical_disks,
            [],
            errors
        )

        storage = safe_collect(
            "Storage inventory",
            get_reportable_storage,
            [],
            errors
        )

        software = safe_collect(
            "Software inventory",
            get_reportable_software,
            [],
            errors
        )
  
    elif is_windows():
        physical_disks = safe_collect(
            "Physical disk inventory",
            get_windows_physical_disks,
            [],
            errors
        )

        storage = safe_collect(
            "Storage inventory",
            get_reportable_storage,
            [],
            errors
        )

        software = safe_collect(
            "Software inventory",
            get_windows_software,
            [],
            errors
        )

    audit = {
        "system": {
            "computer_name": get_computer_name(),
            "operating_system": os_info["name"],
            "os_version": os_info["version"],
            "os_build": os_info["build"],
            "architecture": platform.machine()
        },

        "cpu": {
            "processor": get_cpu_model(),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True)
        },

        "memory": {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "available_gb": round(memory.available / (1024 ** 3), 2),
            "usage_percent": memory.percent
        },

        "physical_disks": physical_disks,
        "storage": storage,
        "software": software,
        "errors": errors
    }

    return audit

if __name__== "__main__":
    audit = build_audit()

    print(audit)
