from __future__ import annotations

# ── Agent & Agent Pools ────────────────────────────────────────────────────────
from .agent import (
    Agent,
    AgentListOptions,
    AgentPool,
    AgentPoolAllowedWorkspacePolicy,
    AgentPoolAssignToWorkspacesOptions,
    AgentPoolCreateOptions,
    AgentPoolListOptions,
    AgentPoolReadOptions,
    AgentPoolRemoveFromWorkspacesOptions,
    AgentPoolUpdateOptions,
    AgentReadOptions,
    AgentStatus,
    AgentToken,
    AgentTokenCreateOptions,
    AgentTokenListOptions,
)

# ── Configuration Versions ────────────────────────────────────────────────────
# (Old: .configuration_version_types) → import directly from real module
from .configuration_version import (
    ConfigurationSource,
    ConfigurationStatus,
    ConfigurationVersion,
    ConfigurationVersionCreateOptions,
    ConfigurationVersionList,
    ConfigurationVersionListOptions,
    ConfigurationVersionReadOptions,
    ConfigurationVersionUpload,
    ConfigVerIncludeOpt,
    IngressAttributes,
)

# ── OAuth ─────────────────────────────────────────────────────────────────────
from .oauth_client import (
    OAuthClient,
    OAuthClientAddProjectsOptions,
    OAuthClientCreateOptions,
    OAuthClientIncludeOpt,
    OAuthClientList,
    OAuthClientListOptions,
    OAuthClientReadOptions,
    OAuthClientRemoveProjectsOptions,
    OAuthClientUpdateOptions,
    ServiceProviderType,
)

from .oauth_token import (
    OAuthToken,
    OAuthTokenList,
    OAuthTokenListOptions,
    OAuthTokenUpdateOptions,
)

# ── Query Runs ────────────────────────────────────────────────────────────────
from .query_run import (
    QueryRun,
    QueryRunCancelOptions,
    QueryRunCreateOptions,
    QueryRunForceCancelOptions,
    QueryRunList,
    QueryRunListOptions,
    QueryRunLogs,
    QueryRunReadOptions,
    QueryRunResults,
    QueryRunStatus,
    QueryRunType,
)

# ── Registry Modules / Providers ──────────────────────────────────────────────
# (Old: .registry_module_types / .registry_provider_types) → import from real modules
from .registry_module import (
    AgentExecutionMode,
    Commit,
    CommitList,
    Input,
    Output,
    ProviderDependency,
    PublishingMechanism,
    RegistryModule,
    RegistryModuleCreateOptions,
    RegistryModuleCreateVersionOptions,
    RegistryModuleCreateWithVCSConnectionOptions,
    RegistryModuleID,
    RegistryModuleList,
    RegistryModuleListIncludeOpt,
    RegistryModuleListOptions,
    RegistryModulePermissions,
    RegistryModuleStatus,
    RegistryModuleUpdateOptions,
    RegistryModuleVCSRepo,
    RegistryModuleVCSRepoOptions,
    RegistryModuleVCSRepoUpdateOptions,
    RegistryModuleVersion,
    RegistryModuleVersionStatus,
    RegistryModuleVersionStatuses,
    RegistryName,
    Resource,
    Root,
    TerraformRegistryModule,
    TestConfig,
)

from .registry_provider import (
    RegistryProvider,
    RegistryProviderCreateOptions,
    RegistryProviderID,
    RegistryProviderIncludeOps,
    RegistryProviderList,
    RegistryProviderListOptions,
    RegistryProviderPermissions,
    RegistryProviderReadOptions,
)

# ── Reserved Tag Keys ─────────────────────────────────────────────────────────
from .reserved_tag_key import (
    ReservedTagKey,
    ReservedTagKeyCreateOptions,
    ReservedTagKeyList,
    ReservedTagKeyListOptions,
    ReservedTagKeyUpdateOptions,
)

# ── SSH Keys ──────────────────────────────────────────────────────────────────
from .ssh_key import (
    SSHKey,
    SSHKeyCreateOptions,
    SSHKeyList,
    SSHKeyListOptions,
    SSHKeyUpdateOptions,
)

# ── Core models split out of old types.py ─────────────────────────────────────
# Adjust these imports to match where you placed them during the split.

# Common / pagination / enums
from .common import Pagination, Tag, TagBinding, EffectiveTagBinding, TagList   # if you put ExecutionMode enum here
from .organization import Entitlements, ExecutionMode

# Organization / Project
from .organization import (
    Organization,
    OrganizationCreateOptions,
    OrganizationUpdateOptions,
)

from .project import Project

# Data retention policy family
from .organization import (
    DataRetentionPolicy,
    DataRetentionPolicyChoice,             
    DataRetentionPolicyDeleteOlder,
    DataRetentionPolicyDeleteOlderSetOptions,
    DataRetentionPolicyDontDelete,
    DataRetentionPolicyDontDeleteSetOptions,
    DataRetentionPolicySetOptions,
)


# Variables
from .variable import (
    Variable,
    VariableCreateOptions,
    VariableListOptions,
    VariableUpdateOptions,
)

# Workspaces
from .workspace import (
    LockedByChoice,
    VCSRepo,
    Workspace,
    WorkspaceActions,
    WorkspaceAddRemoteStateConsumersOptions,
    WorkspaceAddTagBindingsOptions,
    WorkspaceAddTagsOptions,
    WorkspaceAssignSSHKeyOptions,
    WorkspaceCreateOptions,
    WorkspaceIncludeOpt,
    WorkspaceList,
    WorkspaceListOptions,
    WorkspaceListRemoteStateConsumersOptions,
    WorkspaceLockOptions,
    WorkspaceOutputs,
    WorkspacePermissions,
    WorkspaceReadOptions,
    WorkspaceRemoveRemoteStateConsumersOptions,
    WorkspaceRemoveTagsOptions,
    WorkspaceRemoveVCSConnectionOptions,
    WorkspaceSettingOverwrites,
    WorkspaceSource,
    WorkspaceTagListOptions,
    WorkspaceUpdateOptions,
    WorkspaceUpdateRemoteStateConsumersOptions,
)

# Runs
from .run import (
    Run,
    RunStatus,
)

from .organization import (
     RunQueue,
     ReadRunQueueOptions,
)

# ── Public surface ────────────────────────────────────────────────────────────
__all__ = [
    # OAuth
    "OAuthClient",
    "OAuthClientAddProjectsOptions",
    "OAuthClientCreateOptions",
    "OAuthClientIncludeOpt",
    "OAuthClientList",
    "OAuthClientListOptions",
    "OAuthClientReadOptions",
    "OAuthClientRemoveProjectsOptions",
    "OAuthClientUpdateOptions",
    "ServiceProviderType",
    # OAuth token
    "OAuthToken",
    "OAuthTokenList",
    "OAuthTokenListOptions",
    "OAuthTokenUpdateOptions",
    # SSH keys
    "SSHKey",
    "SSHKeyCreateOptions",
    "SSHKeyList",
    "SSHKeyListOptions",
    "SSHKeyUpdateOptions",
    # Reserved tag keys
    "ReservedTagKey",
    "ReservedTagKeyCreateOptions",
    "ReservedTagKeyList",
    "ReservedTagKeyListOptions",
    "ReservedTagKeyUpdateOptions",
    # Agent & pools
    "Agent",
    "AgentPool",
    "AgentPoolAllowedWorkspacePolicy",
    "AgentPoolAssignToWorkspacesOptions",
    "AgentPoolCreateOptions",
    "AgentPoolListOptions",
    "AgentPoolReadOptions",
    "AgentPoolRemoveFromWorkspacesOptions",
    "AgentPoolUpdateOptions",
    "AgentStatus",
    "AgentListOptions",
    "AgentReadOptions",
    "AgentToken",
    "AgentTokenCreateOptions",
    "AgentTokenListOptions",
    # Configuration versions
    "ConfigurationSource",
    "ConfigurationStatus",
    "ConfigurationVersion",
    "ConfigurationVersionCreateOptions",
    "ConfigurationVersionList",
    "ConfigurationVersionListOptions",
    "ConfigurationVersionReadOptions",
    "ConfigurationVersionUpload",
    "ConfigVerIncludeOpt",
    "IngressAttributes",
    # Registry modules
    "AgentExecutionMode",
    "Commit",
    "CommitList",
    "Input",
    "Output",
    "ProviderDependency",
    "PublishingMechanism",
    "RegistryModule",
    "RegistryModuleCreateOptions",
    "RegistryModuleCreateVersionOptions",
    "RegistryModuleCreateWithVCSConnectionOptions",
    "RegistryModuleID",
    "RegistryModuleList",
    "RegistryModuleListIncludeOpt",
    "RegistryModuleListOptions",
    "RegistryModulePermissions",
    "RegistryModuleStatus",
    "RegistryModuleUpdateOptions",
    "RegistryModuleVCSRepo",
    "RegistryModuleVCSRepoOptions",
    "RegistryModuleVCSRepoUpdateOptions",
    "RegistryModuleVersion",
    "RegistryModuleVersionStatus",
    "RegistryModuleVersionStatuses",
    "RegistryName",
    "Resource",
    "Root",
    "TestConfig",
    "TerraformRegistryModule",
    # Registry providers
    "RegistryProvider",
    "RegistryProviderCreateOptions",
    "RegistryProviderID",
    "RegistryProviderIncludeOps",
    "RegistryProviderList",
    "RegistryProviderListOptions",
    "RegistryProviderPermissions",
    "RegistryProviderReadOptions",
    # Query runs
    "QueryRun",
    "QueryRunCancelOptions",
    "QueryRunCreateOptions",
    "QueryRunForceCancelOptions",
    "QueryRunList",
    "QueryRunListOptions",
    "QueryRunLogs",
    "QueryRunReadOptions",
    "QueryRunResults",
    "QueryRunStatus",
    "QueryRunType",
    # Core (from old types.py, now split)
    "Entitlements",
    "ExecutionMode",
    "Pagination",
    "Organization",
    "OrganizationCreateOptions",
    "OrganizationUpdateOptions",
    "Project",
    "DataRetentionPolicy",
    "DataRetentionPolicyChoice",
    "DataRetentionPolicyDeleteOlder",
    "DataRetentionPolicyDeleteOlderSetOptions",
    "DataRetentionPolicyDontDelete",
    "DataRetentionPolicyDontDeleteSetOptions",
    "DataRetentionPolicySetOptions",
    "EffectiveTagBinding",
    "Tag",
    "TagBinding",
    "TagList",
    "Variable",
    "VariableCreateOptions",
    "VariableListOptions",
    "VariableUpdateOptions",
    "LockedByChoice",
    "VCSRepo",
    "Workspace",
    "WorkspaceActions",
    "WorkspaceAddRemoteStateConsumersOptions",
    "WorkspaceAddTagBindingsOptions",
    "WorkspaceAddTagsOptions",
    "WorkspaceAssignSSHKeyOptions",
    "WorkspaceCreateOptions",
    "WorkspaceIncludeOpt",
    "WorkspaceList",
    "WorkspaceListOptions",
    "WorkspaceListRemoteStateConsumersOptions",
    "WorkspaceLockOptions",
    "WorkspaceOutputs",
    "WorkspacePermissions",
    "WorkspaceReadOptions",
    "WorkspaceRemoveRemoteStateConsumersOptions",
    "WorkspaceRemoveTagsOptions",
    "WorkspaceRemoveVCSConnectionOptions",
    "WorkspaceSettingOverwrites",
    "WorkspaceSource",
    "WorkspaceTagListOptions",
    "WorkspaceUpdateOptions",
    "WorkspaceUpdateRemoteStateConsumersOptions",
    "Run",
    "RunQueue",
    "RunStatus",
    "ReadRunQueueOptions",
]
