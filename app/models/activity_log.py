import uuid
from enum import Enum

from app.models.core import CoreModel, CreatedAtMixin, IDModelMixin


class ActivityLogComponentType(str, Enum):
    offer = "offer"
    data_pass = "data_pass"


class ActivityLogEventType(str, Enum):
    offer_link_clicked = "offer_link_clicked"
    view_entered = "view_entered"
    view_exited = "view_exited"
    info_view_entered = "info_view_entered"
    info_view_exited = "info_view_exited"
    liked = "liked"
    unliked = "unliked"
    activated = "activated"
    deactivated = "deactivated"


class ActivityLogBase(CoreModel):
    component: str
    component_identifier: uuid.UUID
    event: str


ActivityLogNew = ActivityLogBase


class ActivityLogDBModel(IDModelMixin, ActivityLogBase, CreatedAtMixin):
    pass


ActivityLog = ActivityLogDBModel
