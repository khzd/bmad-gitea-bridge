"""
Email Generator
Authors: Khaled Z. & Claude (Anthropic)
"""

import yaml
from pathlib import Path

class EmailGenerator:
    def __init__(self, gmail_base: str, gmail_domain: str = "gmail.com", config_path: str = None):
        self.gmail_base = gmail_base
        self.gmail_domain = gmail_domain
        self.config_path = Path(config_path) if config_path else None
        self.mapping = {}
        
        # Transformations
        self.transformations = {
            'quick-flow-solo-dev': 'quickdev',
            'tech-writer': 'techwriter',
            'agent-builder': 'agentbuilder',
            'module-builder': 'modulebuilder',
            'workflow-builder': 'workflowbuilder',
        }
        
        # Load existing mapping if available
        if self.config_path and self.config_path.exists():
            self._load_mapping()
    
    def _load_mapping(self):
        """Load existing email mapping"""
        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
                self.mapping = data.get('agent_emails', {}) if data else {}
        except Exception:
            self.mapping = {}
    
    def _save_mapping(self):
        """Save email mapping to file"""
        if not self.config_path:
            return
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'agent_emails': self.mapping,
            'gmail_base': self.gmail_base,
            'gmail_domain': self.gmail_domain
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True)
    
    def _clean_agent_name(self, agent_name: str) -> str:
        """Clean agent name for email"""
        if agent_name in self.transformations:
            return self.transformations[agent_name]
        return agent_name.replace('_', '').replace('-', '').lower()
    
    def generate_email(self, agent_name: str) -> str:
        """Generate email for an agent"""
        return f"bmad-{agent_name}@{self.gmail_domain}"         
#        return f"{self.gmail_base}-{clean}@{self.gmail_domain}"
    
    def assign_emails_to_agents(self, agents, save: bool = True):
        """Assign emails to all agents"""
        updated = False
        
        for agent in agents:
            agent_name = agent.name
            
            if agent_name in self.mapping:
                agent.email = self.mapping[agent_name]
            else:
                email = self.generate_email(agent_name)
                agent.email = email
                self.mapping[agent_name] = email
                updated = True
        
        if updated and save:
            self._save_mapping()
        
        return agents
