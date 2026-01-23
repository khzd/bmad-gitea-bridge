#!/usr/bin/env python3
"""
Script de diagnostic Gitea
Teste la connexion et les opérations de base
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from gitea.client import GiteaClient

# Load .env
load_dotenv('.env')

print("=" * 70)
print("🔍 DIAGNOSTIC GITEA CONNECTION")
print("=" * 70)

# Configuration
GITEA_URL = os.getenv('GITEA_URL', 'http://192.168.0.76:3000')
GITEA_TOKEN = os.getenv('GITEA_ADMIN_TOKEN')
REPO = 'projet-medical-main'

print(f"\n📋 Configuration:")
print(f"   URL: {GITEA_URL}")
print(f"   Token: {GITEA_TOKEN[:10]}..." if GITEA_TOKEN else "   Token: NOT SET!")
print(f"   Repository: {REPO}")

if not GITEA_TOKEN:
    print("\n❌ GITEA_ADMIN_TOKEN not set in .env!")
    sys.exit(1)

# Test 1: Create client
print(f"\n🔗 Test 1: Creating Gitea client...")
try:
    client = GiteaClient(
        base_url=GITEA_URL,
        token=GITEA_TOKEN,
        repository=REPO,
        verify_ssl=False
    )
    print("   ✅ Client created")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Test connection
print(f"\n🔗 Test 2: Testing connection...")
try:
    if client.test_connection():
        print("   ✅ Connection successful")
    else:
        print("   ❌ Connection failed")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Get current user
print(f"\n👤 Test 3: Getting current user...")
try:
    user = client.get_current_user()
    print(f"   ✅ Logged in as: {user['login']}")
    print(f"   Email: {user.get('email', 'N/A')}")
    print(f"   Full name: {user.get('full_name', 'N/A')}")
    print(f"   Is admin: {user.get('is_admin', False)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: List existing issues
print(f"\n📋 Test 4: Listing existing issues in '{REPO}'...")
try:
    issues = client.list_issues(state='all')
    print(f"   ✅ Found {len(issues)} issues (all states)")

    if issues:
        print("\n   Recent issues:")
        for issue in issues[:5]:
            status = "🟢" if issue['state'] == 'open' else "🔴"
            print(f"      {status} #{issue['number']}: {issue['title']}")
    else:
        print("   ℹ️  No issues found in repository")

except Exception as e:
    print(f"   ❌ Error listing issues: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Try creating a test issue
print(f"\n📝 Test 5: Creating a test issue...")
try:
    test_issue = client.create_issue(
        title="[TEST] Diagnostic test issue",
        body="This is a test issue created by the diagnostic script.\n\nIf you see this, the connection works!",
    )

    print(f"   ✅ Test issue created!")
    print(f"   Issue number: #{test_issue['number']}")
    print(f"   URL: {test_issue.get('html_url', 'N/A')}")

    # Try to close it immediately
    print(f"\n🔒 Test 6: Closing the test issue...")
    try:
        closed_issue = client.update_issue(test_issue['number'], state='closed')
        print(f"   ✅ Test issue closed successfully")
    except Exception as e:
        print(f"   ⚠️  Could not close test issue: {e}")

except Exception as e:
    print(f"   ❌ Error creating test issue: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 70)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 70)
print("""
If all tests passed:
  ✅ Your Gitea connection is working correctly
  ✅ The bridge should be able to create issues

Next steps:
  1. Run: python3 src/sync.py sync-artifacts -p medical --dry-run
  2. Check the output for any errors
  3. If dry-run works, run without --dry-run

If tests failed:
  ❌ Check your .env configuration
  ❌ Verify Gitea is accessible at {GITEA_URL}
  ❌ Verify your admin token has correct permissions
  ❌ Check that repository '{REPO}' exists
""".format(GITEA_URL=GITEA_URL, REPO=REPO))
print("=" * 70)
