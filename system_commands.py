import platform
import subprocess

from platform_utils import is_macos, is_windows

def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
            errors="replace"
        )

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return "Command failed: timed out after 30 seconds"

    except subprocess.CalledProcessError as error:
        message = error.stderr.strip() if error.stderr else str(error)
        return f"Command failed: {message}"

    except FileNotFoundError:
        return f"Command not found: {command[0]}"

    except OSError as error:
        return f"Command failed: {command[0]}"

def get_cpu_model():
    if is_macos():
        output = run_command(
            ["sysctl", "-n", "machdep.cpu.brand_string"]
        )

    elif is_windows():
        output = run_command([
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_Processor | "
            "Select-Object -First 1 -ExpandProperty Name)"
        ])

    else:
        return "Unknnown"

    if output.startswith("Command"):
        return "Unknown"

    return output


def get_os_info():
    if is_macos():
        product_name = run_command(
            ["sw_vers", "-productName"]
        )

        product_version = run_command(
            ["sw_vers", "-productVersion"]
        )

        build_version = run_command(
            ["sw_vers", "-buildVersion"]
        )

        return {
            "name": product_name,
            "version": product_version,
            "build": build_version
        }

    elif is_windows():
        product_name = run_command([
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_OperatingSystem).Caption"
        ])

        product_version = run_command([
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_OperatingSystem).Version"
        ])

        build_version = run_command([
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_OperatingSystem).BuildNumber"
        ])

        return {
            "name": product_name,
            "version": product_version,
            "build": build_version
        }

    return {
        "name": "Unknown",
        "version": "Unknown",
        "build": "Unknown"
    }


def get_computer_name():
    if is_macos():
        output = run_command(
            ["scutil", "--get", "ComputerName"]
        )

        if output.startswith("Command"):
            return "Unknown"

        return output

    elif is_windows():
        return platform.node()
    
    return "Unknown"

    if output.startswith("Command"):
        return "Unknown"

    return output

if __name__ == "__main__":
    print("CPU Model:", get_cpu_model())
