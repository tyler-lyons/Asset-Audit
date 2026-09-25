# Cross-Platform Asset Audit Tool

A Python-based IT asset inventory and system auditing tool designed to collect and report hardware, operating system, storage, disk health, and installed software information across macOS and Windows.

The project was built as a hands-on IT support and systems administration portfolio project, with an emphasis on cross-platform troubleshooting, Python automation, native operating-system commands, structured data collection, and professional report generation.


## Features

- Cross-platform support for macOS and Windows
- System and operating system inventory
- CPU and memory information
- Physical disk inventory
- Logical storage and filesystem usage
- Installed software inventory
- Terminal-based reporting
- JSON report export
- CSV report export
- Responsive HTML report generation
- Collector failure isolation
- Report-generation error handling
- Command-line interface using `argparse`


## Technologies Used

- Python 3
- psutil
- PowerShell
- macOS Terminal
- Windows Registry
- Git
- GitHub
- JSON
- CSV
- HTML / CSS


## Supported Platforms

### macOS

Tested on:

- Apple Silicon MacBook Pro
- macOS
- Apple M3 Pro architecture

### Windows

Tested on:

- Dell Latitude E7270
- Windows 10 Pro
- Intex x86-64 architecture


## Architecture

The Asset Audit Tool uses platform-specific collectors to gather system information from macOS and Windows, then normalizes the results into a shared Python data structure.

This allows the same reporting modules to generate output regardless of the operating system being audited.

```text
macOS Collectors                         Windows Collectors
----------------                         ------------------
system_commands.py                       system_commands.py
disk_info.py                             windows_disk_info.py
software.py                              windows_software.py
        \                                      /
         \                                    /
          ------ audit.py --------------------
                 |
                 v
        Normalized Audit Data
                 |
     ---------------------------
     |          |       |      |
     v          v       v      v
  Terminal     JSON     CSV    HTML
```

### Data Collected

The audit currenctly collects:

- Computer name
- Operating system name
- OS version and build
- System architecture
- CPU model
- Physical CPU core count
- Total and available memory
- Physical disk information
- Disk capacity
- Disk protocol / bus type
- Disk health status
- SSD / HDD media type
- Internal / external disk location
- Read-only status
- Mounted storage volumes
- Filesystem type
- Used and available storage
- Installed software
- Application versions
- Application install locations


## Installation

### Requirements

- Python 3
- Git
- `pip`
- macOS or Windows
- PowerShell on Windows

The project currently uses the following Python dependency:

```text
psutil
```


Dependencies are listed in `requirements.txt`.

### Clone the Repository

```bash
git clone https://github.com/tyler-lyons/Asset-Audit.git
cd Asset-Audit
```


### macOS Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```


### Windows Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```


## Usage

The tool supports four report formats:

```text
terminal
json
csv
html
```


### Terminal Report

```bash
python main.py --format terminal
```


Displays the asset audit directly in the terminal.


### JSON Report

```bash
python main.py --format json
```


Creates:

```text
reports/asset_audit.json
```


### CSV Reports

```bash
python main.py --format csv
```


Creates:

```text
reports/asset_audit_system.csv
reports/asset_audit_disks.csv
reports/asset_audit_storage.csv
reports/asset_audit_software.csv
```


### HTML Report

```bash
python main.py --format html
```


Creates:

```text
reports/asset_audit.html
```


On macOS, open the report with:

```bash
open reports/asset_audit.html
```


On Windows PowerShell:

```powershell
Start-Process reports\asset_audit.html
```


### CLI Help

```bash
python main.py --help
```


If no format is specified, the tool defaults to terminal output:

```bash
python main.py
```


## Project Structure

```text
Asset-Audit/
├── main.py
├── audit.py
├── platform_utils.py
├── system_commands.py
├── disk_info.py
├── windows_disk_info.py
├── storage.py
├── software.py
├── windows_software.py
├── json_report.py
├── csv_report.py
├── html_report.py
├─report_utils.py
├─requirements.txt
├─README.md
└─reports/
```


## Error Handling and Reliability

The project includes several layers of defensive handling to improve reliability across both macOS and Windows.

### Native Command Protection

Native operating-system commands are executed through a shared command runner that handles:

- Missing commands
- Command execution failures
- Operating-system errors
- Command timeouts
- Unexpected character-decoding issues

Commands use a timeout so a failed native process cannot indefinitely block the audit.

### Collector Failure Isolation

Major data collectors are executed through a safe collection wrapper.

If one collector fails, the error is recorded and a safe default value is returned so the remaining audit can continue.

For example, a software inventory failure does not necessarily prevent system, CPU, memory, disk, and storage data from being collected.

Collector errors are stored in the audit data under:

```text
errors
```


A healthy audit should normally contain:

```json
"errors": []
```


### Report Generation Errors

JSON, CSV, and HTML report generation use shared report error handling.

If a report cannot be created because of a filesystem or data error, the command-line interface displays a controlled error instead of an unhandled Python traceback.

The CLI uses process exit codes to indicate execution status:

```text
0 = Successful execution
1 = Report-generation failure
2 = Invalid command-line usage
```


## Testing and Validation

The Asset Audit Tool was tested end-to-end on both macOS and Windows.

### macOS Validation

Tested on an Apple Silicon MacBook Pro.

Validation included:

- Python syntax compilation
- System information collection
- CPU and memory collection
- Internal and external physical disk detection
- Disk health reporting
- Mounted storage collection
- Installed software inventory
- Terminal output
- JSON generation and JSON validation
- CSV generation
- HTML generation and browser rendering
- CLI help and invalid-argument handling
- Collector error tracking
- Report-writing failure handling

### Windows Validation

Tested on a Dell Latitude E7270 running Windows 10 Pro.

Validation included:

- Python syntax compilation
- Windows system and OS detection
- CPU and memory collection
- Physical SSD detection
- Windows storage health collection
- NTFS storage reporting
- Windows uninstall-registry software inventory
- Terminal output
- JSON generation and validation
- CSV generation
- HTML generation and browser rendering
- CLI help and invalid-argument handling
- Collector error tracking
- Cross-platform compatibility after Git synchronization

The same normalized audit structure and reporting modules were used on both operating systems.


## Skills Demonstrated

This project demonstrates practical experience with:

### Python

- Functions and modular program design
- Dictionaries and lists
- Exception handling
- File input/output
- JSON serialization
- CSV generation
- String parsing
- Platform detection
- Subprocess execution
- Command-line argument parsing
- Virtual environments
- Third-party Python packages

### IT Support and System Administration

- Hardware inventory
- Operating-system identification
- CPU and memory inspection
- Physical disk identification
- Disk health interpretation
- Storage and filesystem analysis
- Installed software inventory
- Native macOS administration commands
- Windows PowerShell administration
- Windows Registry-based software discovery
- Cross-platform troubleshooting

### PowerShell and macOS Command Line

This project integrates native operating-system tools including:

- `diskutil`
- `system_profiler`
- `sysctl`
- `sw_vers`
- PowerShell
- `Get-CimInstance`
- `Get-Disk`
- `Get-PhysicalDisk`
- Windows uninstall registry queries

### Software Development Workflow

The project also demonstrates:

- Git version control
- GitHub repository management
- Cross-machine development
- Branch and working-tree verification
- Incremental testing
- Regression testing
- Error simulation
- Debugging syntax and runtime errors
- Refactoring
- Documentation
- Croos-platform validation



## Project Goals

The primary goal of this project was to build a practical cross-platform IT inventory tool while developing hands-on skills relevant to IT support, desktop support, endpoint administration, and systems troubleshooting.

Rather than creating separate standaline scripts for each operating system, the project was designed around a shared audit structure so macOS and Windows could use different native collection methods while producing consistent output.

Key project goals included:

- Build a modular Python application rather tan a single large script
- Practice collecting real system information from macOS and Windows
- Learn how native operating-system tools can be integrated with Python
- Normalize platform-specific data into a shared structure
- Generate multiple professional report formats from the same audit data
- Practice troubleshooting and debugging real implementation problems
- Use Git and GitHub throughout the development lifecycle
- Validate the project on multiple physical computers
- Produce a portfolio project that reflects practical IT support workflows


## Lessons Learned

Building the Asset Audit Tool reinforced several important technical concepts.

### Cross-Platform Development Requires Abstraction

macOS and Windows often expose similar system information in very different ways.

For example:

- macOS physical disks can be queried with `diskutil`
- Windows physical disks can be queried through PowerShell storage cmdlets
- macOS software inventory can be collected with `system_profiler`
- Windows traditional software inventory can be collected from uninstall registry locations

Normalizing these diferent sources into a shared Python structure allowed the report generators to remain platform-independent.

### Structured Data Simplifies Reporting

Separating data collection from presentation made it possible to generate Terminal, JSON, CSV, and HTML reports from the same audit.

This reduced duplicated logic and made the application easier to extend.

### Error Handling Is Part of Tool Design

A working script is not enough for a reliable support utility.

The project was improved to account for:

- Missing native commands
- Failed operating-system commands
- Command timeouts
- Missing data
- Individual collector failures
- Filesystem and report-writing failures
- Invalid command-line arguments

Testing intentional failures helped verify that the program could fail predictably instead of relying only on successful test cases.

### Real Systems Produce Imperfect Data

System inventory data is not always presented consistently.

Examples encountered during development included:

- Different disk identifiers between systems
- Windows reporting a SATA SSD through a RAID controller
- Missing software installation paths
- Duplicate software registry entries
- Operating-system-specific storage structures
- Dynamically changing memory and storage values

The project required interpreting and normalizing these differences rather than assuming every data source would be identical.

### Incremental Testing Reduced Debugging Complexity

The project was developed one component at a time:

```text
Collect → Inspect → Normalize → Test → Integrate → Retest
```


This made it easier to identify whether a problem originated in data collection, parsing, normalization, reporting, or presentation.


## Future Improvements

The current version is functional and validated on macOS and Windows, but several future improvements could extend the project.

Potential additions include:

- Linux system inventory support
- Microsoft Store / AppX application inventory
- Additional Windows and macOS hardware details
- Network adapter and IP configuration inventory
- Battery health reporting for laptops
- BIOS / firmware information
- Device manufacturer and model detection
- Additional disk-health details where supported
- Configurable report output directories
- Timestamped report filenames
- Optional combined report generation
- Logging to a dedicated log file
- Automated CLI filtering options
- Packaging the application for easier installation
- Expanded HTML dashboard visualizations

Linux detection already exists in the platform utility layer, providing a foundation for future Linux collector development.

### Near-Term Priority

- Package the application for easier installation and deployment on additional devices
- Reduce setup requirements for end users
- Explore standalone executables or packaged installers for Windows and macOS


## Poject Status

The core Asset Audit Tool is complete and has been successfully validated on both macOS and Windows.

Current supported report formats:

```text
Terminal
JSON
CSV
HTML
```


Current supported operating systems:

```text
macOS
Windows
```


Linux support is planned as a potential future extension.
