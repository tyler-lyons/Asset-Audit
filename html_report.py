from datetime import datetime
from pathlib import Path

def get_smart_status_class(status):
    if not status:
        return "status-unknown"

    status = status.lower()

    if status in ("verified", "healthy", "passed"):
        return "status-good"

    if status in ("warning", "caution"):
        return "status-warning"

    if status in ("failing", "failed", "error"):
        return "status-bad"

    return "status-unknown"

def save_html_report(audit, filename="asset_audit.html"):
    reports_dir = Path("Reports")
    reports_dir.mkdir(exist_ok=True)

    output_path = reports_dir / filename
    system = audit["system"]
    cpu = audit["cpu"]
    memory = audit["memory"]
    generated_at = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    physical_disk_count = len(audit["physical_disks"])
    application_count = len(audit["software"])

    disk_rows = ""

    for disk in audit["physical_disks"]:
        smart_class = get_smart_status_class(disk["smart_status"])

        disk_rows += f"""
        <tr>
            <td>{disk["device"]}</td>
            <td>{disk["name"]}</td>
            <td>{disk["capacity"]}</td>
            <td>{disk["protocol"]}</td>
            <td>{disk["drive_type"]}</td>
            <td>{disk["location"]}</td>
            <td><span class="{smart_class}">{disk["smart_status"]}</span></td>
            <td>{disk["read_only"]}</td>
        </tr>
        """

    storage_rows = ""

    for storage in audit["storage"]:
        storage_rows += f"""
        <tr>
            <td>{storage["device"]}</td>
            <td>{storage["mountpoint"]}</td>
            <td>{storage["filesystem"]}</td>
            <td>{storage["total_gb"]:.2f} GB</td>
            <td>{storage["used_gb"]:.2f} GB</td>
            <td>{storage["free_gb"]:.2f} GB</td>
            <td>{storage["usage_percent"]}%</td>
        </tr>
        """

    software_rows = ""

    for app in audit["software"]:
        software_rows += f"""
        <tr>
            <td>{app["name"]}</td>
            <td>{app["version"]}</td>
            <td>{app["location"]}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asset Audit Report</title>
<style>
    body {{
        font-family: Arial, Helvetica, sans-serif;
        background-color: #f4f6f8;
        color: #1f2933;
        margin: 0;
        padding: 0;
    }}

    .container {{
        width: 95%;
        max-width: 1400px;
        margin: 30px auto;
    }}

    .header {{
        background-color: #0f2742;
        color: white;
        padding: 28px;
        border-radius: 10px
        margin-bottom: 24px;
    }}

    .header h1 {{
        margin: 0;
    }}

    .header p {{
        margin-top: 8px;
        margin-bottom: 0;
    }}

    .section {{
        background-color: white;
        padding: 22px;
        margin-bottom: 22px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }}

    h2 {{
       margin-top: 0;
       color: #0f2742;
    }}

    table {{
       width: 100%;
       border-collapse: collapse;
       margin-top: 12px;
    }}

    th,
    td {{
       padding: 10px 12px;
       border-bottom: 1px solid #d9e0e7;
       text-align: left;
       vertical-align: top;
    }}

    th {{
       background-color: #eaf0f6;
       front-weight: bold;
    }}

    .software-table {{
       font-size: 14px;
    }}

    .software-table td:nth-child(3) {{
       word-break: break-word;
    }}

    .summary-grid {{
       display: grid;
       grid-template-columns: repeat(4, 1fr);
       gap: 16px;
    }}

    .summary-card {{
       background-color: white;
       padding: 20px;
       border-radius: 10px;
       box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }}

    .summary-card h3 {{
       margin: 0 0 8px 0;
       font-size: 14px;
       color: #5b6773;
       text-transform: uppercase;
    }}

    .summary-card p {{
       margin: 0;
       font-size: 22px;
       font-weight: bold;
       color: #0f2742;
    }}

    .status-good {{
        display: inline-block;
        background-color: dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 13px;
    }}

    .status-warning {{
        display: inline-block;
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 13px;
    }}

    .status-bad {{
        display: inline-block;
        background-color: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fca5a5;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 13px;
    }}

    .status-unknown {{
        display: inline-block;
        background-color: #e5e7eb;
        color: #4b5563;
        border: 1px solid #cbd5e1;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 13px;
    }}

    .footer {{
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        padding: 18px 10px 28px 10px;
    }}

    .footer p {{
        margin: 4px 0;
    }}

    .table-wrapper {{
        width: 100%;
        overflow-x: auto;
    }}

@media (max-width: 900px) {{
    .summary-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media (max-width: 600px) {{
    .summary-grid {{
        grid-template-columns: 1fr;
    }}

    .container {{
        width: 95%;
        margin: 10px auto;
    }}

    .header {{
        padding: 20px;
    }}

    .section {{
        padding: 16px;
    }}

    h1 {{
        font-size: 24px;
    }}

    h2 {{
        font-size: 20px;
    }}
}}
</style>
</head>

<body>
<div class="container">
<div class="header".
    <h1>IT Asset Audit Report</h1>
    <p>Cross-Platform System Inventory Tool</p>
    <p>Generated: {generated_at}</p>
</div>

<div class="summary-grid">

    <div class="summary-card">
        <h3>Operating System</h3>
        <p>{system["operating_system"]} {system["os_version"]}</p>
    </div>

    <div class="summary-card">
        <h3>Total Memory</h3>
        <p>{memory["total_gb"]:.2f} GB</p>
    </div>

    <div class="summary-card">
        <h3>Physical Disk</h3>
        <p>{physical_disk_count}</p>
    </div>

    <div class="summary-card">
        <h3>Applications</h3>
        <p>{application_count}</p>
    </div>

</div>

<div class="section">
    <h2>System Information</h2>

    <table>
           <tr>
              <th>Computer Name</th>
              <td>{system["computer_name"]}</td>
           </tr>
           <tr>
              <th>Operating System</th>
              <td>{system["operating_system"]}</td>
           </tr>
           <tr>
              <th>OS Version</th>
              <td>{system["os_version"]}</td>
           </tr>
           <tr>
              <th>OS Build</th>
              <td>{system["os_build"]}</td>
           </tr>
           <tr>
              <th>Architecture</th>
              <td>{system["architecture"]}</td>
           </tr>
    </table>
</div>

<div class="section">
    <h2>CPU Information</h2>

    <table>
        <tr>
            <th>Processor</th>
            <td>{cpu["processor"]}</td>
        </tr>
        <tr>
            <th>Physical Cores</th>
            <td>{cpu["physical_cores"]}</td>
        </tr>
        <tr>
            <th>Logical Cores</th>
            <td>{cpu["logical_cores"]}</td>
        </tr>
    </table>
</div>

<div class="section">
    <h2>Memory Information</h2>

    <table>
        <tr>
            <th>Total RAM</th>
            <td>{memory["total_gb"]:.2f} GB</td>
        </tr>
        <tr>
            <th>Available RAM</th>
            <td>{memory["available_gb"]:.2f} GB</td>
        </tr>
        <tr>
            <th>RAM Usage</th>
            <td>{memory["usage_percent"]}%</td>
        </tr>
    </table>
</div>

<div class="section">
    <h2>Physical Disk Inventory</h2>

    <div class="table-wrapper">
        <table>
            <tr>
                <th>Device</th>
                <th>Name</th>
                <th>Capacity</th>
                <th>Protocol</th>
                <th>Drive Type</th>
                <th>Location</th>
                <th>SMART Status</th>
                <th>Read Only</th>
            </tr>

            {disk_rows}
        </table>
    </div>
</div>

<div class="section">
    <h2>Storage Inventory</h2>

    <div class="table-wrapper">
        <table>
            <tr>
                <th>Device</th>
                <th>Mount Point</th>
                <th>Filesystem</th>
                <th>Total</th>
                <th>Used</th>
                <th>Free</th>
                <th>Usage</th>
            </tr>

            {storage_rows}
        </table>
    </div>
</div>

<div class="section">
    <h2>Software Inventory</h2>

    <p>Total Applications: <strong>{len(audit["software"])}</strong></p>

    <div class="table-wrapper">
        <table class="software-table">
            <tr>
                <th>Name</th>
                <th>Version</th>
                <th>Location</th>
            </tr>

            {software_rows}
        </table>
    </div>
</div>

    <div class="footer">
        <p>Generated by Cross-Platform IT Asset Audit Tool</p>
        <p>{system["computer_name"]} | {generated_at}</p>
    </div>

</div>

</body>
</html>
"""


    with output_path.open("w", encoding="utf-8") as file:
        file.write(html)

    return output_path
