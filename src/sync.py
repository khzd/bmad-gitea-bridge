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
        discovery = AgentDiscovery(str(project_config.bmad_root))
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


# Phase 1: Agent Discovery
    console.print("[bold]📋 Phase 1: Agent Discovery[/bold]")

    try:
        discovery = AgentDiscovery(str(project_config.bmad_root))
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

