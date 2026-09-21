import platform

def get_platform():
    return platform.system()


def is_macos():
    return get_platform() == "Darwin"


def is_windows():
    return get_platform() == "Windows"


def is_linux():
    return get_platform() == "Linux"


if __name__ == "__main__":
    print(f"Platform: {get_platform()}")
    print(f"macOS: {is_macos()}")
    print(f"Windows: {is_windows()}")
    print(f"Linux: {is_linux()}")

