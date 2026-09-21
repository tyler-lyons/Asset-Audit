import argparse

from audit import build_audit
from csv_report import save_csv_reports
from html_report import save_html_report
from json_report import save_json_report

def print_report(audit):
    print("=" * 50)
    print("ASSET AUDIT - SYSTEM INVENTORY")
    print("=" * 50)

    system = audit["system"]

    print("\nSYSTEM INFORMATION")
    print(f"Computer Name: {system['computer_name']}")
    print(f"Operating System: {system['operating_system']}")
    print(f"OS Version: {system['os_version']}")
    print(f"OS Build: {system['os_build']}")
    print(f"Architecture: {system['architecture']}")

    cpu = audit["cpu"]

    print("\nCPU INFORMATION")
    print(f"Processor: {cpu['processor']}")
    print(f"Physical Cores: {cpu['physical_cores']}")
    print(f"Logical Cores: {cpu['logical_cores']}")

    memory = audit["memory"]

    print("\nMEMORY INFORMATION")
    print(f"Total RAM: {memory['total_gb']:.2f} GB")
    print(f"Available RAM: {memory['available_gb']:.2f} GB")
    print(f"RAM Usage: {memory['usage_percent']}%")

    print("\nPHYSICAL DISK INVENTORY")

    for disk in audit["physical_disks"]:
        print("\n" + "-" * 50)
        print(f"Device: {disk['device']}")
        print(f"Name: {disk['name']}")
        print(f"Capacity: {disk['capacity']}")
        print(f"Protocol: {disk['protocol']}")
        print(f"Drive Type: {disk['drive_type']}")
        print(f"Location: {disk['location']}")
        print(f"SMART Status: {disk['smart_status']}")
        print(f"Virtual: {disk['virtual']}")
        print(f"Read Only: {disk['read_only']}")

    print("\nSTORAGE INVENTORY")

    for disk in audit["storage"]:
        print("\n" + "-" * 50)
        print(f"Device: {disk['device']}")
        print(f"Mount Point: {disk['mountpoint']}")
        print(f"Filesystem: {disk['filesystem']}")
        print(f"Total: {disk['total_gb']} GB")
        print(f"Used: {disk['used_gb']} GB")
        print(f"Free: {disk['free_gb']} GB")
        print(f"Usage: {disk['usage_percent']}%")

    print("\nSOFTWARE INVENTORY")
    print(f"Total Applications: {len(audit['software'])}")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Cross-platform IT Asset Audit Tool"
    )

    parser.add_argument(
        "--format",
        choices=["terminal", "json", "csv", "html"],
        default="terminal",
        help="Choose the report format"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    audit = build_audit()

    if args.format == "terminal":
        print_report(audit)

    elif args.format == "json":
        json_path = save_json_report(audit)
        print(f"JSON Report: {json_path}")

    elif args.format == "csv":
        csv_paths = save_csv_reports(audit)

        print("CSV Reports:")

        for path in csv_paths:
            print(f"  {path}")

    elif args.format=="html":
        html_path = save_html_report(audit)
        print(f"HTML Report: {html_path}")

if __name__ == "__main__":
    main()
