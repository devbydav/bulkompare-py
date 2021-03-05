from enum import Enum

from api.utils.constants import Status


class ActionStatus(Enum):
    DISABLED = -1  # cannot be used, usually because a previously needed step is not valid yet
    INVALID = 1  # can (and must) be used, as it is not valid
    VALID = 2  # can be used

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


ACTION_STATUS = {  # ActionStatus for property selection,     mapping selection,     column selection
    Status.INITIALIZED:             (ActionStatus.DISABLED, ActionStatus.DISABLED, ActionStatus.DISABLED),
    Status.FILES_SELECTED:          (ActionStatus.INVALID,  ActionStatus.DISABLED, ActionStatus.DISABLED),
    Status.COLUMNS_AVAILABLE:       (ActionStatus.VALID,    ActionStatus.INVALID,  ActionStatus.DISABLED),
    Status.MAPPING_VALID:           (ActionStatus.VALID,    ActionStatus.VALID,    ActionStatus.INVALID),
    Status.READY_TO_IMPORT:         (ActionStatus.VALID,    ActionStatus.VALID,    ActionStatus.VALID),
    Status.DATA_IMPORTED:           (ActionStatus.VALID,    ActionStatus.VALID,    ActionStatus.VALID),
}
