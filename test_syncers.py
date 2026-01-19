#!/usr/bin/env python3
"""
Test script for Epic & Story Syncers

Quick test to verify sync functionality works.

Usage:
    python3 test_syncers.py
"""

import sys
from pathlib import Path

# Add src to path (adjust if needed)
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from parsers.epic_parser import EpicParser
from parsers.story_parser import StoryParser

print("=" * 60)
print("🧪 Testing Epic & Story Parsers")
print("=" * 60)

# Test data directory
test_dir = Path("test-artifacts")

if not test_dir.exists():
    print(f"❌ Test directory not found: {test_dir}")
    print("Please copy test-artifacts/ to current directory")
    sys.exit(1)

# Test Epic Parser
print("\n📋 Testing Epic Parser...")
epic_file = test_dir / "epics" / "epic-001-patient-portal.md"

if epic_file.exists():
    try:
        parser = EpicParser(epic_file)
        data = parser.parse()
        
        print(f"   ✅ Epic parsed successfully")
        print(f"   Title: {data['title']}")
        print(f"   Description: {data['description'][:50]}...")
        print(f"   Stories: {len(data['stories'])} referenced")
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print(f"   ⚠️  Epic file not found: {epic_file}")

# Test Story Parser
print("\n📝 Testing Story Parser...")
story_files = list((test_dir / "stories").glob("story-*.md"))

print(f"   Found {len(story_files)} story files")

for story_file in story_files[:3]:  # Test first 3
    try:
        parser = StoryParser(story_file)
        data = parser.parse()
        
        print(f"   ✅ {story_file.name}")
        print(f"      Title: {data['title']}")
        print(f"      Assignee: {data.get('assignee', 'None')}")
        print(f"      Tasks: {len(data.get('tasks', []))}")
    except Exception as e:
        print(f"   ❌ {story_file.name}: {e}")

print("\n" + "=" * 60)
print("✅ Parser tests complete!")
print("=" * 60)
print("\nNext steps:")
print("1. Install syncers: cp epic_syncer.py src/core/")
print("2. Install syncers: cp story_syncer.py src/core/")
print("3. Update config with artifacts path")
print("4. Run: python src/sync.py sync-artifacts --project medical --dry-run")
