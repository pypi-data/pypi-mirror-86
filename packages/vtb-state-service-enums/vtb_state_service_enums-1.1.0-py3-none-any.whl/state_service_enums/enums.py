import logging
from enum import Enum


class ActionType(Enum):
    DEPLOY = 'deploy'
    BILLING = 'billing'


class ActionSubType(Enum):
    # TODO: deprecated
    RUN = 'run'
    RUN_NODE = 'run_node'
    ROLLBACK = 'rollback'
    ROLLBACK_NODE = 'rollback_node'


ActionDeploy = ActionSubType
logging.warning('ActionSubType is deprecated, use ActionDeploy')


class ActionStatus(Enum):
    # TODO: deprecated
    STARTED = 'started'
    COMPLETED = 'completed'
    ERROR = 'error'


ActionDeployStatus = ActionStatus
logging.warning('ActionStatus is deprecated, use ActionDeployStatus')


class ActionBilling(Enum):
    FOLDER = 'folder'


class ActionFolderStatus(Enum):
    CHANGED = 'changed'


class ActionStatus(Enum):
    STARTED = 'started'
    COMPLETED = 'completed'
    ERROR = 'error'


class EventType(Enum):
    VM = 'vm'
    CLUSTER = 'cluster'
    PROJECT = 'project'
    LICENSE = 'license'


class EventSubType(Enum):
    STATE = 'state'
    CONFIG = 'config'
    PARENT = 'parent'
    VIRTUALIZATION = 'virtualization'


class EventState(Enum):
    ON = 'on'
    OFF = 'off'
    REBOOT = 'reboot'
    DELETED = 'deleted'


class EventVirtualization(Enum):
    OPENSTACK = 'openstack'
    VMWARE = 'vmware'
    NUTANIX = 'nutanix'
    OPENSHIFT = 'openshift'
    KUBERNETES = 'kubernetes'
