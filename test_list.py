from src.gitea.client import GiteaClient
import os
from dotenv import load_dotenv

load_dotenv('.env')

client = GiteaClient(
    base_url='http://192.168.0.76:3000',
    token=os.getenv('GITEA_ADMIN_TOKEN'),
    repository='projet-medical-main',
    verify_ssl=False
)

print(f"Current user: {client.get_current_user()['login']}")
print(f"Organization: '{client.organization}'")
print(f"Repository: '{client.repository}'")

# Call list_issues
issues = client.list_issues(state='open')
print(f"\nlist_issues() returned: {len(issues)} issues")

# Test direct API call
import requests
token = os.getenv('GITEA_ADMIN_TOKEN')

# Construire l'URL comme le ferait le code
current_user = client.get_current_user()
repo_path = f"{current_user['login']}/{client.repository}"
url = f"http://192.168.0.76:3000/api/v1/repos/{repo_path}/issues"

print(f"\nDirect API test:")
print(f"URL: {url}")

resp = requests.get(url, headers={'Authorization': f'token {token}'}, params={'state': 'open'})
print(f"Status: {resp.status_code}")
print(f"Issues: {len(resp.json())}")

if resp.json():
    print(f"First issue: #{resp.json()[0]['number']} - {resp.json()[0]['title']}")
