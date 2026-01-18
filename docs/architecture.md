# BMad-Gitea-Bridge - Architecture

## Overview

This tool synchronizes BMad AI agents with Gitea project management.

## Key Features

- Auto-discovers agents from manifest
- Zero-config sync
- Safe provisioning (manual or auto)
- Multi-project support

## Architecture

BMad Agents → Bridge (Python) → Gitea (Issues/Wiki) → Gmail (Notifications)

## Components

1. Agent Discovery (reads agent-manifest.csv)
2. Email Generator (Gmail + aliases)
3. Gitea Provisioner (creates users)
4. File Parsers (epics, stories)
5. Gitea Client (API wrapper)

## Data Flow

1. BMad agents generate files
2. Sync script discovers changes
3. Creates Gitea entities
4. Sends Gmail notifications

## Mappings

- Epic files → Gitea Milestones
- Story files → Gitea Issues  
- Architecture → Gitea Wiki
- Agents → Gitea Users

## Configuration

See config/projects/template.yaml for all options.

## Authors

Khaled Z. & Claude (Anthropic)
