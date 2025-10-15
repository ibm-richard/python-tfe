"""
Terraform Cloud/Enterprise Workspace Management Example

This example demonstrates comprehensive workspace operations using the python-tfe SDK.
It provides a command-line interface for managing TFE workspaces with various operations
including create, read, update, delete, lock/unlock, and advanced filtering capabilities.

Prerequisites:
    - Set TFE_TOKEN environment variable with your Terraform Cloud API token
    - Ensure you have access to the target organization

Basic Usage:
    python examples/workspace.py --help

Core Operations:

1. List Workspaces (default operation):
    python examples/workspace.py --org my-org
    python examples/workspace.py --org my-org --page-size 20
    python examples/workspace.py --org my-org --page 2 --page-size 10

2. Create New Workspace:
    python examples/workspace.py --org my-org --create

3. Read Workspace Details by name and ID:
    python examples/workspace.py --org my-org --workspace "my-workspace"
    python examples/workspace.py --org my-org --workspace-id "ws-abc123xyz"

4. Update Workspace Settings:
    python examples/workspace.py --org my-org --workspace "my-workspace" --update
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    ExecutionMode,
    Tag,
    WorkspaceAddTagsOptions,
    WorkspaceCreateOptions,
    WorkspaceIncludeOpt,
    WorkspaceListOptions,
    WorkspaceListRemoteStateConsumersOptions,
    WorkspaceLockOptions,
    WorkspaceReadOptions,
    WorkspaceTagListOptions,
    WorkspaceUpdateOptions,
)


def _print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Workspace demo for python-tfe SDK")
    parser.add_argument(
        "--address", default=os.getenv("TFE_ADDRESS", "https://app.terraform.io")
    )
    parser.add_argument("--token", default=os.getenv("TFE_TOKEN", ""))
    parser.add_argument("--org", required=True, help="Organization name")
    parser.add_argument("--workspace", help="Workspace name to read/update/delete")
    parser.add_argument("--workspace-id", help="Workspace ID for ID-based operations")
    parser.add_argument("--create", action="store_true", help="Create a new workspace")
    parser.add_argument("--delete", action="store_true", help="Delete the workspace")
    parser.add_argument(
        "--safe-delete", action="store_true", help="Safely delete the workspace"
    )
    parser.add_argument(
        "--update", action="store_true", help="Update workspace settings"
    )
    parser.add_argument("--lock", action="store_true", help="Lock the workspace")
    parser.add_argument("--unlock", action="store_true", help="Unlock the workspace")
    parser.add_argument(
        "--remove-vcs", action="store_true", help="Remove VCS connection"
    )
    parser.add_argument("--page", type=int, default=1, help="Page number for listing")
    parser.add_argument(
        "--page-size", type=int, default=10, help="Page size for listing"
    )
    parser.add_argument("--search", help="Search workspaces by partial name")
    parser.add_argument("--tags", help="Filter by tags (comma-separated)")
    parser.add_argument(
        "--exclude-tags", help="Exclude workspaces with these tags (comma-separated)"
    )
    parser.add_argument("--wildcard-name", help="Filter by wildcard name matching")
    parser.add_argument("--project-id", help="Filter by project ID")
    args = parser.parse_args()

    cfg = TFEConfig(address=args.address, token=args.token)
    client = TFEClient(cfg)

    # 1) List workspaces in the organization
    _print_header("Listing workspaces")
    try:
        # Create options for listing workspaces with pagination and filters
        options = WorkspaceListOptions(
            page_number=args.page,
            page_size=args.page_size,
            search=args.search,
            tags=args.tags,
            exclude_tags=args.exclude_tags,
            wildcard_name=args.wildcard_name,
            project_id=args.project_id,
        )

        filter_info = []
        if args.search:
            filter_info.append(f"search='{args.search}'")
        if args.tags:
            filter_info.append(f"tags='{args.tags}'")
        if args.exclude_tags:
            filter_info.append(f"exclude-tags='{args.exclude_tags}'")
        if args.wildcard_name:
            filter_info.append(f"wildcard='{args.wildcard_name}'")
        if args.project_id:
            filter_info.append(f"project='{args.project_id}'")

        filter_str = f" with filters: {', '.join(filter_info)}" if filter_info else ""
        print(
            f"Fetching workspaces from organization '{args.org}' (page {args.page}, size {args.page_size}){filter_str}..."
        )

        # Get workspaces and convert to list safely
        workspace_gen = client.workspaces.list(args.org, options)
        workspace_list = []
        count = 0
        for ws in workspace_gen:
            workspace_list.append(ws)
            count += 1
            if count >= args.page_size * 2:  # Safety limit based on page size
                break

        print(f"✓ Found {len(workspace_list)} workspaces")
        print()

        if not workspace_list:
            print("No workspaces found in this organization.")
        else:
            for i, ws in enumerate(workspace_list, 1):
                print(f"{i:2d}. {ws.name}")
                print(f"    ID: {ws.id}")
                print(f"    Execution Mode: {ws.execution_mode}")
                print(f"    Auto Apply: {ws.auto_apply}")
                print()
    except Exception as e:
        print(f"✗ Error listing workspaces: {e}")
        print("This could be due to:")
        print("  - Invalid token")
        print("  - No access to the organization")
        print("  - Network issues")
        return

    # 2) Create a new workspace if requested
    if args.create:
        _print_header("Creating a new workspace")
        try:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            workspace_name = f"demo-workspace-{timestamp}"

            create_options = WorkspaceCreateOptions(
                name=workspace_name,
                description=f"Demo workspace created at {datetime.now()}",
                auto_apply=False,
                execution_mode=ExecutionMode.REMOTE,
                terraform_version="1.5.0",
                working_directory="terraform/",
                file_triggers_enabled=True,
                queue_all_runs=False,
                speculative_enabled=True,
                trigger_prefixes=["modules/", "shared/"],
            )

            print(
                f"Creating workspace '{workspace_name}' in organization '{args.org}'..."
            )
            workspace = client.workspaces.create(args.org, create_options)
            print("✓ Successfully created workspace!")
            print(f"   Name: {workspace.name}")
            print(f"   ID: {workspace.id}")
            print(f"   Description: {workspace.description}")
            print(f"   Execution Mode: {workspace.execution_mode}")
            print(f"   Auto Apply: {workspace.auto_apply}")
            print(f"   Terraform Version: {workspace.terraform_version}")
            print()

            args.workspace = (
                workspace.name
            )  # Use the created workspace for other operations
            args.workspace_id = workspace.id
        except Exception as e:
            print(f"✗ Error creating workspace: {e}")
            print("This could be due to:")
            print("  - Invalid token or insufficient permissions")
            print("  - Workspace name already exists")
            print("  - Organization doesn't exist or no access")
            print("  - Invalid workspace configuration")
            return

    # 3) Read workspace details if workspace name is provided
    if args.workspace:
        _print_header(f"Reading workspace: {args.workspace}")
        read_options = WorkspaceReadOptions(
            include=[WorkspaceIncludeOpt.CURRENT_RUN, WorkspaceIncludeOpt.OUTPUTS]
        )

        workspace = client.workspaces.read_with_options(
            args.workspace, read_options, organization=args.org
        )
        print(f"Workspace: {workspace.name}")
        print(f"ID: {workspace.id}")
        print(f"Description: {workspace.description}")
        print(f"Execution Mode: {workspace.execution_mode}")
        print(f"Auto Apply: {workspace.auto_apply}")
        print(f"Locked: {workspace.locked}")
        print(f"Terraform Version: {workspace.terraform_version}")
        print(f"Working Directory: {workspace.working_directory}")

        # Set workspace_id for further operations
        if not args.workspace_id:
            args.workspace_id = workspace.id

    # 4) Update workspace if requested
    if args.update and args.workspace:
        _print_header(f"Updating workspace: {args.workspace}")
        try:
            update_options = WorkspaceUpdateOptions(
                name=args.workspace,  # Name is required
                description=f"Updated workspace at {datetime.now()}",
                auto_apply=True,
                terraform_version="1.6.0",
            )

            print(
                f"Updating workspace '{args.workspace}' in organization '{args.org}'..."
            )
            updated_workspace = client.workspaces.update(
                args.workspace, update_options, organization=args.org
            )
            print("✓ Successfully updated workspace!")
            print(f"   Name: {updated_workspace.name}")
            print(f"   Description: {updated_workspace.description}")
            print(f"   Auto Apply: {updated_workspace.auto_apply}")
            print(f"   Terraform Version: {updated_workspace.terraform_version}")
            print()
        except Exception as e:
            print(f"✗ Error updating workspace: {e}")
            print("This could be due to:")
            print("  - Invalid token or insufficient permissions")
            print("  - Workspace doesn't exist")
            print("  - Invalid update configuration")
            return

    # 5) Lock workspace if requested
    if args.lock and args.workspace_id:
        _print_header(f"Locking workspace: {args.workspace_id}")
        lock_options = WorkspaceLockOptions(reason="Demo lock via python-tfe SDK")

        locked_workspace = client.workspaces.lock(args.workspace_id, lock_options)
        print(f"Locked workspace: {locked_workspace.name}")
        print(f"Lock reason: {locked_workspace.locked_by}")

    # 6) Unlock workspace if requested
    if args.unlock and args.workspace_id:
        _print_header(f"Unlocking workspace: {args.workspace_id}")

        unlocked_workspace = client.workspaces.unlock(args.workspace_id)
        print(f"Unlocked workspace: {unlocked_workspace.name}")

    # 7) Remove VCS connection if requested
    if args.remove_vcs and args.workspace:
        _print_header(f"Removing VCS connection from workspace: {args.workspace}")
        try:
            print(
                f"Removing VCS connection from workspace '{args.workspace}' in organization '{args.org}'..."
            )
            workspace = client.workspaces.remove_vcs_connection(
                args.workspace, organization=args.org
            )
            print("✓ Successfully removed VCS connection from workspace!")
            print(f"   Workspace: {workspace.name}")
            print()
        except Exception as e:
            print(f"✗ Error removing VCS connection: {e}")
            print("This could be due to:")
            print("  - No VCS connection exists on this workspace")
            print("  - Invalid token or insufficient permissions")
            print("  - Workspace doesn't exist")
            # Don't return here since this might be expected if no VCS is connected

    # 8) Demonstrate tag operations
    if args.workspace_id:
        _print_header("Tag operations")

        # List existing tags
        tag_options = WorkspaceTagListOptions(page_size=20)
        try:
            tags = list(client.workspaces.list_tags(args.workspace_id, tag_options))
            print(f"Current tags: {[tag.name for tag in tags]}")
        except Exception as e:
            print(f"Error listing tags: {e}")

        # Add some demo tags
        try:
            add_tag_options = WorkspaceAddTagsOptions(
                tags=[Tag(name="demo"), Tag(name="python-tfe")]
            )
            client.workspaces.add_tags(args.workspace_id, add_tag_options)
            print("Added demo tags: demo, python-tfe")
        except Exception as e:
            print(f"Error adding tags: {e}")

    # 9) Demonstrate remote state consumer operations
    if args.workspace_id:
        _print_header("Remote state consumer operations")

        # List remote state consumers
        try:
            consumer_options = WorkspaceListRemoteStateConsumersOptions(page_size=10)
            consumers = list(
                client.workspaces.list_remote_state_consumers(
                    args.workspace_id, consumer_options
                )
            )
            print(f"Remote state consumers: {len(consumers)}")
            for consumer in consumers:
                print(f"- {consumer.name} (ID: {consumer.id})")
        except Exception as e:
            print(f"Error listing remote state consumers: {e}")

    # 10) Delete workspace if requested (should be last operation)
    if args.delete and args.workspace:
        _print_header(f"Deleting workspace: {args.workspace}")

        if args.safe_delete:
            client.workspaces.safe_delete(args.workspace, organization=args.org)
            print(f"Safely deleted workspace: {args.workspace}")
        else:
            client.workspaces.delete(args.workspace, organization=args.org)
            print(f"Deleted workspace: {args.workspace}")


if __name__ == "__main__":
    main()
