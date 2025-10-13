#!/usr/bin/env python3
"""
Example usage of Notification Configuration API

This example demonstrates how to use the Python TFE library to manage
notification configurations for workspaces and teams.

Based on the Go TFE notification_configuration.go implementation.
"""

import os
import sys

# Add the src directory to the Python path so we can import the tfe module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pytfe.client import TFEClient
from pytfe.models.notification_configuration import (
    NotificationConfigurationCreateOptions,
    NotificationConfigurationListOptions,
    NotificationConfigurationSubscribableChoice,
    NotificationConfigurationUpdateOptions,
    NotificationDestinationType,
    NotificationTriggerType,
)


def main():
    """Demonstrate notification configuration operations."""

    # Initialize the TFE client
    # Make sure to set TFE_ADDRESS and TFE_TOKEN environment variables
    client = TFEClient()

    print("=== Python TFE Notification Configuration Example ===\n")

    # Use example workspace ID (replace with your actual workspace ID)
    workspace_id = "ws-example123456789"  # Replace with your workspace ID
    workspace_name = "your-workspace-name"
    print(f"Using workspace: {workspace_name} (ID: {workspace_id})")

    # Use fake team ID for demonstration (teams not available in free plan)
    team_id = "team-example123456789"
    print("Using fake team ID for demonstration (teams not available in free plan)")

    try:
        # ===== List notification configurations for workspace =====
        print("1. Listing notification configurations for workspace...")
        try:
            workspace_notifications = client.notification_configurations.list(
                subscribable_id=workspace_id
            )
            print(
                f"Found {len(workspace_notifications.items)} notification configurations"
            )
            for nc in workspace_notifications.items:
                print(f"  - {nc.name} (ID: {nc.id}, Enabled: {nc.enabled})")
        except Exception as e:
            print(f"  Error listing workspace notifications: {e}")

        print()

        # ===== List notification configurations for team =====
        print("2. Listing notification configurations for team...")
        try:
            team_choice = NotificationConfigurationSubscribableChoice(
                team={"id": team_id}
            )
            options = NotificationConfigurationListOptions(
                subscribable_choice=team_choice
            )
            team_notifications = client.notification_configurations.list(
                subscribable_id=team_id, options=options
            )
            print(
                f"Found {len(team_notifications.items)} team notification configurations"
            )
            for nc in team_notifications.items:
                print(f"  - {nc.name} (ID: {nc.id}, Enabled: {nc.enabled})")
        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg:
                print(f"  ⚠️  Team not found (expected with fake team ID): {team_id}")
                print("  💡 Teams are not available in HCP Terraform free plan")
            else:
                print(f"  ❌ Error listing team notifications: {e}")

        print()

        # ===== Create a new workspace notification configuration =====
        print("3. Creating a new workspace notification configuration...")
        try:
            workspace_choice = NotificationConfigurationSubscribableChoice(
                workspace={"id": workspace_id}
            )
            create_options = NotificationConfigurationCreateOptions(
                destination_type=NotificationDestinationType.SLACK,
                enabled=True,
                name="Python TFE Example Slack Notification",
                subscribable_choice=workspace_choice,
                url="https://hooks.slack.com/services/YOUR_SLACK_WORKSPACE/YOUR_CHANNEL/YOUR_WEBHOOK_TOKEN",
                triggers=[
                    NotificationTriggerType.COMPLETED,
                    NotificationTriggerType.ERRORED,
                ],
            )

            new_notification = client.notification_configurations.create(
                workspace_id, create_options
            )
            print(
                f"  Created notification: {new_notification.name} (ID: {new_notification.id})"
            )

            notification_id = new_notification.id

            # ===== Read the notification configuration =====
            print("\n4. Reading the notification configuration...")
            read_notification = client.notification_configurations.read(
                notification_config_id=notification_id
            )
            print(f"  Read notification: {read_notification.name}")
            print(f"  Destination type: {read_notification.destination_type}")
            print(f"  Enabled: {read_notification.enabled}")
            print(f"  Triggers: {read_notification.triggers}")

            # ===== Update the notification configuration =====
            print("\n5. Updating the notification configuration...")
            update_options = NotificationConfigurationUpdateOptions(
                name="Updated Python TFE Example Webhook",
                enabled=False,
                triggers=[NotificationTriggerType.ERRORED],  # Only notify on errors
            )

            updated_notification = client.notification_configurations.update(
                notification_config_id=notification_id, options=update_options
            )
            print(f"  Updated notification: {updated_notification.name}")
            print(f"  Enabled: {updated_notification.enabled}")

            # ===== Verify the notification configuration =====
            print("\n6. Verifying the notification configuration...")
            print("  Note: This will fail with fake URLs - that's expected!")
            try:
                client.notification_configurations.verify(
                    notification_config_id=notification_id
                )
                print(
                    f"  ✅ Verification successful for notification ID: {notification_id}"
                )
                print("  Note: Verification sends a test payload to the configured URL")
            except Exception as e:
                print(f"  ⚠️  Verification failed (expected with fake URL): {e}")
                print(
                    "  💡 To test verification, use a real webhook URL from Slack, Teams, or Discord"
                )

            # ===== Delete the notification configuration =====
            print("\n7. Deleting the notification configuration...")
            client.notification_configurations.delete(
                notification_config_id=notification_id
            )
            print(f"  Deleted notification configuration: {notification_id}")

            # Verify deletion
            try:
                client.notification_configurations.read(
                    notification_config_id=notification_id
                )
                print("  ERROR: Notification still exists after deletion!")
            except Exception:
                print("  Confirmed: Notification configuration has been deleted")

        except Exception as e:
            error_msg = str(e).lower()
            if "verification failed" in error_msg and "404" in error_msg:
                print("  ⚠️  Webhook verification failed (expected with fake URL)")
                print(
                    "  💡 The fake Slack URL returns 404 - this is normal for testing"
                )
                print("  🔗 To test real verification, use a webhook from:")
                print("     • webhook.site (instant test URL)")
                print("     • Slack, Teams, or Discord webhook")
            else:
                print(f"  ❌ Error in workspace notification operations: {e}")

        print()

        # ===== Create a team notification configuration =====
        print("8. Creating a team notification configuration...")
        try:
            if team_id != "team-example123456789":  # Only try if we have a real team ID
                team_choice = NotificationConfigurationSubscribableChoice(
                    team={"id": team_id}
                )
                team_create_options = NotificationConfigurationCreateOptions(
                    destination_type=NotificationDestinationType.SLACK,
                    enabled=True,
                    name="Team Slack Notifications",
                    subscribable_choice=team_choice,
                    url="https://hooks.slack.com/services/YOUR_SLACK_WORKSPACE/YOUR_CHANNEL/YOUR_WEBHOOK_TOKEN",
                    triggers=[NotificationTriggerType.COMPLETED],
                )

                team_notification = client.notification_configurations.create(
                    team_id, team_create_options
                )
                print(
                    f"  Created team notification: {team_notification.name} (ID: {team_notification.id})"
                )

                # Clean up team notification
                client.notification_configurations.delete(
                    notification_config_id=team_notification.id
                )
                print(f"  Cleaned up team notification: {team_notification.id}")
            else:
                print(
                    f"  Skipping team notifications - no real team ID available (using: {team_id})"
                )

        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "team" in error_msg:
                print("  ⚠️  Team operations not available (expected with fake team ID)")
                print("  💡 Teams require HCP Terraform paid plan or Enterprise")
            else:
                print(f"  ❌ Error in team notification operations: {e}")

        print()

        # ===== Create a Microsoft Teams notification configuration =====
        print("9. Creating a Microsoft Teams notification configuration...")
        try:
            workspace_choice = NotificationConfigurationSubscribableChoice(
                workspace={"id": workspace_id}
            )
            teams_create_options = NotificationConfigurationCreateOptions(
                destination_type=NotificationDestinationType.MICROSOFT_TEAMS,
                enabled=True,
                name="Teams Notifications",
                subscribable_choice=workspace_choice,
                url="https://outlook.office.com/webhook/YOUR_TENANT_ID@YOUR_TENANT_ID/IncomingWebhook/YOUR_CONNECTOR_ID/YOUR_TEAMS_WEBHOOK_TOKEN",
                triggers=[
                    NotificationTriggerType.ERRORED,
                    NotificationTriggerType.NEEDS_ATTENTION,
                ],
            )

            teams_notification = client.notification_configurations.create(
                workspace_id, teams_create_options
            )
            print(
                f"  Created Teams notification: {teams_notification.name} (ID: {teams_notification.id})"
            )

            # Clean up Teams notification
            client.notification_configurations.delete(
                notification_config_id=teams_notification.id
            )
            print(f"  Cleaned up Teams notification: {teams_notification.id}")

        except Exception as e:
            print(f"  Error in Teams notification operations: {e}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure to:")
        print(
            "1. Set TFE_ADDRESS environment variable (e.g., https://app.terraform.io)"
        )
        print("2. Set TFE_TOKEN environment variable with your API token")
        print(
            "3. Replace workspace_id and team_id with actual values from your organization"
        )

    print("\n=== Notification Configuration Example Complete ===")


if __name__ == "__main__":
    main()
