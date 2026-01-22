"""
Config Loader
Authors: Khaled Z. & Claude (Anthropic)
"""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
import logging
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class TeamConfig:
    """Team configuration"""
    name: str
    description: str = ""
    permission: str = "write"
    includes_all_repositories: bool = True
    members: str = "all"
    units: List[str] = field(default_factory=lambda: [
        "repo.code", "repo.issues", "repo.pulls",
        "repo.releases", "repo.wiki", "repo.projects"
    ])


@dataclass
class RepositoryConfig:
    """Repository configuration"""
    name: str
    description: str = ""
    private: bool = True
    auto_init: bool = True


@dataclass
class OrganizationConfig:
    """Organization configuration"""
    name: str
    description: str = ""
    create_if_missing: bool = True
    teams: List[TeamConfig] = field(default_factory=list)
    repositories: List[RepositoryConfig] = field(default_factory=list)


@dataclass
class ProjectConfig:
    """Project configuration"""
    name: str
    description: str
    bmad_root: Path
    bmad_manifest: Path
    gitea_url: str
    gitea_organization: str
    gitea_repository: str
    gitea_admin_token: str
    gmail_base: str
    gmail_domain: str
    log_level: str = "INFO"
    sync_provisioning: str = "issue"
# with default warninig!!! !!! !!!
    bmad_artifacts: Optional[Path] = None
    organization_config: Optional[OrganizationConfig] = None    


    def __post_init__(self):
       """Validate after init"""
        if isinstance(self.bmad_root, str):
            self.bmad_root = Path(self.bmad_root)

        if isinstance(self.bmad_manifest, str):
           manifest_path = Path(self.bmad_manifest)
           # Si chemin absolu, utiliser tel quel
        if manifest_path.is_absolute():
           self.bmad_manifest = manifest_path
        else:
           # Si relatif, ajouter à bmad_root
           self.bmad_manifest = self.bmad_root / self.bmad_manifest

            # DEBUG
        print(f"DEBUG: Final manifest path: {self.bmad_manifest}")


        if isinstance(self.bmad_manifest, str):
            self.bmad_manifest = self.bmad_root / self.bmad_manifest
        
        if not self.bmad_root.exists():
            raise ValueError(f"BMad root does not exist: {self.bmad_root}")
        
        if not self.bmad_manifest.exists():
            raise ValueError(f"Agent manifest not found: {self.bmad_manifest}")


class ConfigLoader:
    """Loads configuration files"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        
        # Load .env
        env_file = self.base_dir / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            logger.info(f"Loaded .env from {env_file}")
    
    def _expand_env_vars(self, value):
        """Expand ${VAR} in config"""
        if isinstance(value, str):
            if value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                return os.getenv(env_var, "")
            return value
        elif isinstance(value, dict):
            return {k: self._expand_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._expand_env_vars(item) for item in value]
        return value
    
    def load_project_config(self, project_name: str) -> ProjectConfig:
        """Load project configuration"""
        config_file = self.config_dir / "projects" / f"{project_name}.yaml"
        
        if not config_file.exists():
            raise ValueError(f"Config not found: {config_file}")
        
        with open(config_file, 'r') as f:
            raw_config = yaml.safe_load(f)
        
        # Expand env vars
        config = self._expand_env_vars(raw_config)
        
        # Parse organization config if present
        org_config = None
        if 'organization' in config:
            org_data = config['organization']
            teams = []
            if 'teams' in org_data:
                for team_data in org_data['teams']:
                    teams.append(TeamConfig(**team_data))

            repos = []
            if 'repositories' in org_data:
                for repo_data in org_data['repositories']:
                    repos.append(RepositoryConfig(**repo_data))

            org_config = OrganizationConfig(
                name=org_data['name'],
                description=org_data.get('description', ''),
                create_if_missing=org_data.get('create_if_missing', True),
                teams=teams,
                repositories=repos
            )

        # Create ProjectConfig object
        project_config = ProjectConfig(
            name=config['project']['name'],
            description=config['project'].get('description', ''),
            bmad_root=config['bmad']['root'],
            bmad_manifest=config['bmad']['manifest'],
            bmad_artifacts=config['bmad'].get('artifacts'),
            gitea_url=config['gitea']['url'],
            gitea_organization=config['gitea'].get('organization', ''),
            gitea_repository=config['gitea']['repository'],
            gitea_admin_token=config['gitea']['admin_token'],
            gmail_base=config['gmail']['base'],
            gmail_domain=config['gmail'].get('domain', 'gmail.com'),
            log_level=config.get('logging', {}).get('level', 'INFO'),
            sync_provisioning=config.get('sync', {}).get('provisioning', 'issue'),
            organization_config=org_config
            )

# Convert and validate manifest path
        from pathlib import Path
        manifest_path = Path(config['bmad']['manifest'])
        if manifest_path.is_absolute():
            project_config.bmad_manifest = manifest_path
        else:
            project_config.bmad_manifest = Path(config['bmad']['root']) / manifest_path
        
        # Validate existence
        if not project_config.bmad_manifest.exists():
            raise ValueError(f"Manifest not found: {project_config.bmad_manifest}")

        logger.info(f"✅ Loaded project: {project_name}")
        return project_config
