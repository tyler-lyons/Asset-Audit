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


def build_audit():
    os_info = get_os_info()
    memory = psutil.virtual_memory()

    physical_disks = []
    storage = []
    software = []

    if is_macos():
        for device in get_physical_disks():
            physical_disks.append(
                get_physical_disk_info(device)
            )

        storage = get_reportable_storage()
        software = get_reportable_software()
  
    elif is_windows():
        physical_disks = get_windows_physical_disks()
        storage = get_reportable_storage()
        software = get_windows_software()

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

        "software": software
    }

    return audit

if __name__== "__main__":
    audit = build_audit()

    print(audit)
