from pathlib import Path

from system_commands import run_command


def get_installed_software():
    output = run_command(
        ["system_profiler", "SPApplicationsDataType"]
    )

    software = []
    current_app = None

    for line in output.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if stripped == "Applications:":
            continue

        if line.startswith("    ") and not line.startswith("      "):
            if stripped.endswith(":"):
                if current_app:
                    software.append(current_app)

                current_app = {
                    "name": stripped.rstrip(":"),
                    "version": "Unknown",
                    "location": "Unknown"
                }

        elif current_app and stripped.startswith("Version:"):
            current_app["version"] = stripped.split(":", 1)[1].strip()

        elif current_app and stripped.startswith("Location:"):
            current_app["location"] = stripped.split(":", 1)[1].strip()

    if current_app:
        software.append(current_app)

    return software

def get_reportable_software():
    software = get_installed_software()

    reportable = []

    user_applications = str(Path.home() / "Applications") + "/"

    allowed_locations = [
        "/Applications/",
        "/System/Applications/",
        "/System/Library/",
        "/Library/",
        user_applications
    ]

    for app in software:
        location = app["location"]

        if any(location.startswith(path) for path in allowed_locations):
            reportable.append(app)

    return reportable

if __name__ == "__main__":
    applications = get_reportable_software()

    print("=" * 50)
    print("INSTALLED SOFTWARE")
    print("=" * 50)

    for app in applications:
        print(f"\nName: {app['name']}")
        print(f"Version: {app['version']}")
        print(f"Location: {app['location']}")

    print(f"\nTotal Applications: {len(applications)}")
