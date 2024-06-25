import requests
from datetime import datetime
import os

# Ganti dengan nama pengguna GitHub Anda
USERNAME = 'idugeni'
TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'token {TOKEN}'}

# Mendapatkan semua repositori pengguna
repos_url = f'https://api.github.com/users/{USERNAME}/repos'
repos = requests.get(repos_url, headers=HEADERS).json()

# Mengambil aktivitas terbaru dari semua repositori
events = []
for repo in repos:
    repo_name = repo['name']
    events_url = f'https://api.github.com/repos/{USERNAME}/{repo_name}/events'
    repo_events = requests.get(events_url, headers=HEADERS).json()
    events.extend(repo_events)

# Mengurutkan aktivitas berdasarkan waktu dan mengambil 5 aktivitas terbaru
events = sorted(events, key=lambda x: x['created_at'], reverse=True)[:5]

# Format aktivitas
last_activities = []
for event in events:
    event_type = event['type']
    repo_name = event['repo']['name']
    created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    created_at_formatted = created_at.strftime('%d %B %Y')
    last_activities.append(f"- **{created_at_formatted}**: {event_type} di {repo_name}")

# Membaca konten README.md
with open('README.md', 'r') as file:
    readme_contents = file.readlines()

# Menemukan dan mengganti bagian "Last Activity"
start_marker = '<!--START_SECTION:activity-->\n'
end_marker = '<!--END_SECTION:activity-->\n'

try:
    start_idx = readme_contents.index(start_marker) + 1
    end_idx = readme_contents.index(end_marker)
except ValueError:
    print("Markers not found in README.md")
    exit(1)

new_readme_contents = (
    readme_contents[:start_idx] +
    [f"{activity}\n" for activity in last_activities] +
    readme_contents[end_idx:]
)

# Menulis ulang konten README.md jika ada perubahan
if new_readme_contents != readme_contents:
    with open('README.md', 'w') as file:
        file.writelines(new_readme_contents)
else:
    print("No changes in activity detected")
