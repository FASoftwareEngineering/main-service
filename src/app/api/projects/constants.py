from enum import Enum


class ProjectStatuses(str, Enum):
    default = "default"
    active = "active"
    paused = "paused"
    finished = "finished"
