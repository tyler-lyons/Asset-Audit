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


def get_windows_software():
    powershell_command = r"""
$paths = @(
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*'
)

Get-ItemProperty $paths -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName } |
    Select-Object DisplayName,DisplayVersion,InstallLocation |
    Sort-Object DisplayName |
    ConvertTo-Json
""".strip()

    apps = run_powershell_json(powershell_command)

    software = []
    seen = set()

    for app in apps:
        name = app.get("DisplayName") or "Unknown"
        version = app.get("DisplayVersion") or "Unknown"
        location = app.get("InstallLocation") or "Unknown"

        key = (
            name.lower(),
            version.lower(),
            location.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        software.append({
            "name": name,
            "version": version,
            "location": location
        })

    return software


if __name__ == "__main__":
    applications = get_windows_software()

    print("=" * 50)
    print("WINDOWS SOFTWARE INVENTORY")
    print("=" * 50)

    for app in applications[:15]:
        print()
        print(f"Name: {app['name']}")
        print(f"Version: {app['version']}")
        print(f"Location: {app['location']}")

    print(f"\nTotal Applications: {len(applications)}")