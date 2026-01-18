from src.gitea.client import GiteaClient
import os
from dotenv import load_dotenv

# Load .env
load_dotenv('.env')

client = GiteaClient(
    base_url='http://192.168.0.76:3000',
    token=os.getenv('GITEA_ADMIN_TOKEN'),
    repository='projet-medical-main',
    verify_ssl=False
)

print("Testing list_issues()...")
issues = client.list_issues(state='open')
print(f"Found {len(issues)} open issues")

if issues:
    print("\nFirst 5 issues:")
    for issue in issues[:5]:
        print(f"  #{issue['number']}: {issue['title']}")
else:
    print("  ❌ No issues returned!")
