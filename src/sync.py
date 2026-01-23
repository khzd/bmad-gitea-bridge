#!/usr/bin/env python3
"""
BMad-Gitea-Bridge - Main Script
Authors: Khaled Z. & Claude (Anthropic)
"""

import click
import logging
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

from core.config_loader import ConfigLoader
from core.agent_discovery import AgentDiscovery
from core.email_generator import EmailGenerator

console = Console()
__version__ = "0.1.0"

def setup_logging(log_level: str):
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

@click.group()
@click.version_option(version=__version__)
def cli():
    """BMad-Gitea-Bridge - Sync BMad agents with Gitea"""
    pass

@cli.command()
@click.option('--project', '-p', required=True, help='Project name')
@click.option('--dry-run', is_flag=True, help='Simulation mode')
def sync(project: str, dry_run: bool):
    """Synchronize BMad project with Gitea"""
    
    config_loader = ConfigLoader()
    
    try:
        project_config = config_loader.load_project_config(project)
    except Exception as e:
        console.print(f"[red]❌ Error loading config:[/red] {e}")
        sys.exit(1)
    
    logger = setup_logging(project_config.log_level)
    
    console.print("\n[bold cyan]🌉 BMad-Gitea-Bridge[/bold cyan]")
    console.print(f"[dim]Version {__version__}[/dim]")
    console.print("=" * 60)
    
    console.print(f"\n[bold]Project:[/bold] {project_config.name}")
    console.print(f"[bold]BMad Root:[/bold] {project_config.bmad_root}")
    console.print(f"[bold]Gitea:[/bold] {project_config.gitea_url}")
    
    if dry_run:
        console.print("\n[yellow]🔍 DRY RUN - No changes[/yellow]")
    
    console.print()
    
    # Phase 1: Agent Discovery
    console.print("[bold]📋 Phase 1: Agent Discovery[/bold]")
    
    try:
        discovery = AgentDiscovery(
            str(project_config.bmad_root),
            str(project_config.bmad_manifest)
            )
        agents = discovery.discover_all_agents()
        
        console.print(f"   [green]✅ Discovered {len(agents)} agents[/green]")
        
        table = Table(title="Discovered Agents")
        table.add_column("Icon", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Display Name", style="yellow")
        table.add_column("Module", style="magenta")
        
        for agent in agents:
            table.add_row(agent.icon, agent.name, agent.display_name, agent.module)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Agent discovery failed")
        sys.exit(1)
    
    # Phase 2: Email Assignment
    console.print("\n[bold]📧 Phase 2: Email Assignment[/bold]")
    
    try:
        email_mapping_file = Path(f"config/projects/{project}.email-mapping.yaml")
        
        email_gen = EmailGenerator(
            gmail_base=project_config.gmail_base,
            gmail_domain=project_config.gmail_domain,
            config_path=str(email_mapping_file)
        )
        
        agents = email_gen.assign_emails_to_agents(agents, save=not dry_run)
        
        console.print(f"   [green]✅ Assigned emails to {len(agents)} agents[/green]")
        
        email_table = Table(title="Email Mappings")
        email_table.add_column("Agent", style="cyan")
        email_table.add_column("Email", style="green")
        
        for agent in agents:
            email_table.add_row(agent.name, agent.email or "Not assigned")
        
        console.print(email_table)
        
    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Email assignment failed")
        sys.exit(1)
# Phase 3: Gitea User Provisioning
    console.print("\n[bold]🔧 Phase 3: Gitea User Provisioning[/bold]")
    
    if dry_run:
        console.print("   [yellow]⏭️  Skipped (dry-run mode)[/yellow]")
    else:
        try:
            from gitea.client import GiteaClient
            from core.gitea_provisioner import GiteaProvisioner
            
            # Connect to Gitea
            gitea_client = GiteaClient(
                base_url=project_config.gitea_url,
                token=project_config.gitea_admin_token,
                organization=project_config.gitea_organization,
                repository=project_config.gitea_repository,
                verify_ssl=False
            )
            
            # Test connection
            if not gitea_client.test_connection():
                console.print("   [red]❌ Cannot connect to Gitea[/red]")
                sys.exit(1)
            
            # Provision users
            provisioner = GiteaProvisioner(
                gitea_client=gitea_client,
                mode=project_config.sync_provisioning if hasattr(project_config, 'sync_provisioning') else 'issue'
            )
            
            results = provisioner.provision_all_agents(agents)
            
            # Display results
            console.print(f"   [green]✅ Provisioning complete[/green]")
            console.print(f"      Created: {len(results['created'])}")
            console.print(f"      Already exist: {len(results['exists'])}")
            console.print(f"      Pending (issues): {len(results['pending'])}")
            
            # Show details if any created or pending
            if results['created'] or results['pending']:
                prov_table = Table(title="Provisioning Results")
                prov_table.add_column("Agent", style="cyan")
                prov_table.add_column("Status", style="yellow")
                prov_table.add_column("Details", style="green")
                
                for item in results['created']:
                    prov_table.add_row(
                        item['username'],
                        "✅ Created",
                        f"Email: {item['email']}"
                    )
                
                for item in results['pending']:
                    prov_table.add_row(
                        item['username'],
                        "📋 Issue created",
                        f"Issue #{item.get('issue_number', 'N/A')}"
                    )
                
                console.print(prov_table)
        
        except Exception as e:
            console.print(f"   [red]❌ Error:[/red] {e}")
            logger.exception("Gitea provisioning failed")

    # Phase 4: Organization & Team Setup
    if project_config.organization_config and not dry_run:
        console.print("\n[bold]🏢 Phase 4: Organization & Team Setup[/bold]")

        try:
            from gitea.organizations import GiteaOrganizations

            # Ensure Gitea client is initialized
            if 'gitea_client' not in locals():
                from gitea.client import GiteaClient
                gitea_client = GiteaClient(
                    base_url=project_config.gitea_url,
                    token=project_config.gitea_admin_token,
                    organization=project_config.gitea_organization,
                    repository=project_config.gitea_repository,
                    verify_ssl=False
                )

            org_manager = GiteaOrganizations(gitea_client)
            org_config = project_config.organization_config

            # Ensure organization exists
            org_data = org_manager.ensure_organization(
                org_config.name,
                org_config.description
            )

            if org_manager.organization_exists(org_config.name):
                console.print(f"   [green]✅ Organization:[/green] {org_config.name} (exists)")
            else:
                console.print(f"   [green]✅ Created organization:[/green] {org_config.name}")

            # Create teams and add members
            for team_config in org_config.teams:
                team_data = org_manager.create_team(
                    org_config.name,
                    team_config.name,
                    team_config.description,
                    team_config.permission,
                    team_config.includes_all_repositories,
                    team_config.units
                )

                console.print(f"   [green]✅ Created team:[/green] {team_config.name}")

                # Add members
                if team_config.members == "all":
                    # Add all discovered agents
                    usernames = [f"bmad-{agent.name}" for agent in agents]
                    results = org_manager.add_users_to_team(team_data['id'], usernames)
                    console.print(f"   [green]✅ Added {results['success']} members to {team_config.name}[/green]")

            # Create repositories
            for repo_config in org_config.repositories:
                repo_data = org_manager.create_repo_in_org(
                    org_config.name,
                    repo_config.name,
                    repo_config.description,
                    repo_config.private,
                    repo_config.auto_init
                )

                console.print(f"   [green]✅ Created repository:[/green] {repo_config.name}")

        except Exception as e:
            console.print(f"   [red]❌ Error:[/red] {e}")
            logger.exception("Organization setup failed")

    # Summary
    console.print("\n" + "=" * 60)
    
    if dry_run:
        console.print("[bold green]✅ Dry-run completed![/bold green]")
        console.print("\nNo changes were made. Remove --dry-run to execute.")
    else:
        console.print("[bold green]✅ Discovery completed![/bold green]")
    
    console.print()

@cli.command()
@click.option('--project', '-p', required=True, help='Project name')
@click.option('--dry-run', is_flag=True, help='Simulation mode')
def sync_artifacts(project: str, dry_run: bool):
    """Synchronize BMad artifacts (epics, stories) with Gitea"""
    
    config_loader = ConfigLoader()
    
    try:
        project_config = config_loader.load_project_config(project)
    except Exception as e:
        console.print(f"[red]❌ Error loading config:[/red] {e}")
        sys.exit(1)
    
    logger = setup_logging(project_config.log_level)
    
    console.print("\n[bold cyan]🌉 BMad-Gitea-Bridge - Artifact Sync[/bold cyan]")
    console.print(f"[dim]Version {__version__}[/dim]")
    console.print("=" * 60)
    
    console.print(f"\n[bold]Project:[/bold] {project_config.name}")
    console.print(f"[bold]BMad Root:[/bold] {project_config.bmad_root}")
    console.print(f"[bold]Gitea:[/bold] {project_config.gitea_url}")
    
    if dry_run:
        console.print("\n[yellow]🔍 DRY RUN - No changes[/yellow]")
    
    console.print()
    
    # Import syncers
    from core.epic_syncer import EpicSyncer
    from core.story_syncer import StorySyncer
    from core.agent_discovery import AgentDiscovery
    from core.email_generator import EmailGenerator
    from gitea.client import GiteaClient
    
    # Check artifacts path
    artifacts_path = getattr(project_config, 'bmad_artifacts', None)
    
    if not artifacts_path:
        console.print("[red]❌ No artifacts path configured[/red]")
        console.print("\nAdd to config/projects/{project}.yaml:")
        console.print("  bmad:")
        console.print("    artifacts: /path/to/artifacts")
        sys.exit(1)
    
    artifacts_path = Path(artifacts_path)
    
    if not artifacts_path.exists():
        console.print(f"[red]❌ Artifacts path not found: {artifacts_path}[/red]")
        sys.exit(1)
    
    # Phase 1: Agent Discovery (needed for assignee mapping)
    console.print("[bold]📋 Phase 1: Agent Discovery[/bold]")
    
    try:
        discovery = AgentDiscovery(
            str(project_config.bmad_root),
            str(project_config.bmad_manifest)
        )
        agents = discovery.discover_all_agents()
        
        # Assign emails
        email_mapping_file = Path(f"config/projects/{project}.email-mapping.yaml")
        email_gen = EmailGenerator(
            gmail_base=project_config.gmail_base,
            gmail_domain=project_config.gmail_domain,
            config_path=str(email_mapping_file)
        )
        agents = email_gen.assign_emails_to_agents(agents, save=not dry_run)
        
        console.print(f"   [green]✅ Discovered {len(agents)} agents[/green]")
        
    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Agent discovery failed")
        sys.exit(1)
    
    # Phase 2: Connect to Gitea
    console.print("\n[bold]🔗 Phase 2: Gitea Connection[/bold]")
    
    try:
        gitea_client = GiteaClient(
            base_url=project_config.gitea_url,
            token=project_config.gitea_admin_token,
            organization=project_config.gitea_organization,
            repository=project_config.gitea_repository,
            verify_ssl=False
        )
        
        if not gitea_client.test_connection():
            console.print("   [red]❌ Cannot connect to Gitea[/red]")
            sys.exit(1)
        
    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Gitea connection failed")
        sys.exit(1)
    
    # Phase 3: Sync Epics → Milestones
    console.print("\n[bold]🎯 Phase 3: Epic Sync (Epics → Milestones)[/bold]")
    
    try:
        epic_syncer = EpicSyncer(gitea_client, artifacts_path)
        epic_results = epic_syncer.sync_all_epics(dry_run=dry_run)
        
        console.print(f"   [green]✅ Epic sync complete[/green]")
        console.print(f"      Created: {len(epic_results['created'])}")
        console.print(f"      Already exist: {len(epic_results['exists'])}")
        console.print(f"      Failed: {len(epic_results['failed'])}")
        
        if epic_results['created'] or epic_results['failed']:
            epic_table = Table(title="Epic Sync Results")
            epic_table.add_column("Epic", style="cyan")
            epic_table.add_column("Status", style="yellow")
            epic_table.add_column("Milestone", style="green")
            
            for item in epic_results['created']:
                epic_table.add_row(
                    Path(item['epic_file']).name,
                    "✅ Created",
                    f"#{item['milestone'].get('id', 'N/A')}"
                )
            
            for item in epic_results['failed']:
                epic_table.add_row(
                    Path(item['epic_file']).name,
                    "❌ Failed",
                    item.get('error', 'Unknown error')
                )
            
            console.print(epic_table)
    
    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Epic sync failed")
    
    # Phase 4: Sync Stories → Issues
    console.print("\n[bold]📝 Phase 4: Story Sync (Stories → Issues)[/bold]")
    
    try:
        story_syncer = StorySyncer(gitea_client, artifacts_path, agents)
        story_results = story_syncer.sync_all_stories(dry_run=dry_run)
        
        console.print(f"   [green]✅ Story sync complete[/green]")
        console.print(f"      Created: {len(story_results['created'])}")
        console.print(f"      Already exist: {len(story_results['exists'])}")
        console.print(f"      Failed: {len(story_results['failed'])}")
        
        if story_results['created'] or story_results['failed']:
            story_table = Table(title="Story Sync Results")
            story_table.add_column("Story", style="cyan")
            story_table.add_column("Status", style="yellow")
            story_table.add_column("Assignee", style="magenta")
            story_table.add_column("Issue", style="green")
            
            for item in story_results['created']:
                story_table.add_row(
                    Path(item['story_file']).name,
                    "✅ Created",
                    item.get('assignee', 'None'),
                    f"#{item['issue'].get('number', 'N/A')}"
                )
            
            for item in story_results['failed']:
                story_table.add_row(
                    Path(item['story_file']).name,
                    "❌ Failed",
                    "N/A",
                    item.get('error', 'Unknown error')
                )
            
            console.print(story_table)
    
    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Story sync failed")
    
    # Summary
    console.print("\n" + "=" * 60)
    
    if dry_run:
        console.print("[bold green]✅ Dry-run completed![/bold green]")
        console.print("\nNo changes were made. Remove --dry-run to execute.")
    else:
        console.print("[bold green]✅ Artifact sync completed![/bold green]")
    
    console.print()

@cli.command()
def version():
    """Show version"""
    console.print(f"\n[bold cyan]BMad-Gitea-Bridge[/bold cyan]")
    console.print(f"Version: {__version__}")
    console.print(f"Authors: Khaled Z. & Claude (Anthropic)")
    console.print(f"License: MIT\n")

def main():
    cli()

if __name__ == '__main__':
    main()


# Phase 1: Agent Discovery
    console.print("[bold]📋 Phase 1: Agent Discovery[/bold]")

    try:
        discovery = AgentDiscovery(
            str(project_config.bmad_root),
            str(project_config.bmad_manifest)
            )        
        agents = discovery.discover_all_agents()

        console.print(f"   [green]✅ Discovered {len(agents)} agents[/green]")

        table = Table(title="Discovered Agents")
        table.add_column("Icon", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Display Name", style="yellow")
        table.add_column("Module", style="magenta")

        for agent in agents:
            table.add_row(agent.icon, agent.name, agent.display_name, agent.module)

        console.print(table)

    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Agent discovery failed")
        sys.exit(1)

    # Phase 2: Email Assignment
    console.print("\n[bold]📧 Phase 2: Email Assignment[/bold]")

    try:
        email_mapping_file = Path(f"config/projects/{project}.email-mapping.yaml")

        email_gen = EmailGenerator(
            gmail_base=project_config.gmail_base,
            gmail_domain=project_config.gmail_domain,
            config_path=str(email_mapping_file)
        )

        agents = email_gen.assign_emails_to_agents(agents, save=not dry_run)

        console.print(f"   [green]✅ Assigned emails to {len(agents)} agents[/green]")

        email_table = Table(title="Email Mappings")
        email_table.add_column("Agent", style="cyan")
        email_table.add_column("Email", style="green")

        for agent in agents:
            email_table.add_row(agent.name, agent.email or "Not assigned")

        console.print(email_table)

    except Exception as e:
        console.print(f"   [red]❌ Error:[/red] {e}")
        logger.exception("Email assignment failed")
        sys.exit(1)

    # Summary
    console.print("\n" + "=" * 60)

    if dry_run:
        console.print("[bold green]✅ Dry-run completed![/bold green]")
        console.print("\nNo changes were made. Remove --dry-run to execute.")
    else:
        console.print("[bold green]✅ Discovery completed![/bold green]")

    console.print()

@cli.command()
def version():
    """Show version"""
    console.print(f"\n[bold cyan]BMad-Gitea-Bridge[/bold cyan]")
    console.print(f"Version: {__version__}")
    console.print(f"Authors: Khaled Z. & Claude (Anthropic)")
    console.print(f"License: MIT\n")

def main():
    cli()

if __name__ == '__main__':
    main()

