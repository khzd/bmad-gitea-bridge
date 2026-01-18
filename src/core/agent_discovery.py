"""
Agent Discovery - reads agent-manifest.csv
Authors: Khaled Z. & Claude (Anthropic)
"""

import csv
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    display_name: str
    title: str
    icon: str
    role: str
    module: str
    path: str
    email: str = None
    gitea_username: str = None




class AgentDiscovery:
    def __init__(self, bmad_root: str):
        self.bmad_root = Path(bmad_root)
        self.manifest_path = self.bmad_root / "_bmad/_config/agent-manifest.csv"
    
    def discover_all_agents(self):
        agents = []
        with open(self.manifest_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                agent = Agent(
                  name=row['name'].strip('"'),
                  display_name=row['displayName'].strip('"'),
                  title=row['title'].strip('"'),
                  icon=row.get('icon', '🤖').strip('"'),
                  role=row['role'].strip('"'),
                  module=row['module'].strip('"'),
                  path=row['path'].strip('"')
                )
                agents.append(agent)
        return agents
