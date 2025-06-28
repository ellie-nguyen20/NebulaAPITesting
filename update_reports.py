import os
import re
from datetime import datetime

INDEX_FILE = "index.html"
MAX_REPORTS_EACH = 7

# --- Helpers ---
def extract_timestamp(filename):
    match = re.search(r'report_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d_%H-%M-%S")
        except ValueError:
            return datetime.min
    return datetime.min

def generate_list_items(files):
    html = ""
    for f in files:
        ts = extract_timestamp(f)
        display = ts.strftime("%Y-%m-%d %H:%M:%S") if ts != datetime.min else "Unknown"
        html += f"""
        <li class="report-item">
            <a href="{f}" class="report-link">{f}</a>
            <div class="timestamp">Generated on: {display}</div>
        </li>"""
    return html

# --- Get all report files ---
all_files = [f for f in os.listdir(".") if f.endswith(".html") and f != INDEX_FILE]
personal_reports = sorted(
    [f for f in all_files if "_personal.html" in f],
    key=extract_timestamp, reverse=True
)
team_reports = sorted(
    [f for f in all_files if "_team.html" in f],
    key=extract_timestamp, reverse=True
)

# --- Trim to 7 each ---
personal_latest = personal_reports[:MAX_REPORTS_EACH]
team_latest = team_reports[:MAX_REPORTS_EACH]

# --- Remove old files ---
for f in personal_reports[MAX_REPORTS_EACH:] + team_reports[MAX_REPORTS_EACH:]:
    os.remove(f)

# --- Generate HTML blocks ---
personal_html = generate_list_items(personal_latest)
team_html = generate_list_items(team_latest)

# --- Update index.html in-place ---
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Replace only between special HTML comments
content = re.sub(
    r"(<!-- PERSONAL_START -->)(.*?)(<!-- PERSONAL_END -->)",
    rf"\1{personal_html}\3",
    content,
    flags=re.DOTALL
)

content = re.sub(
    r"(<!-- TEAM_START -->)(.*?)(<!-- TEAM_END -->)",
    rf"\1{team_html}\3",
    content,
    flags=re.DOTALL
)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(content)
