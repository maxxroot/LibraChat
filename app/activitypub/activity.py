# app/activitypub/activity.py

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, Union

class Activity(BaseModel):
    id: HttpUrl
    type: str
    actor: HttpUrl
    object: Union[HttpUrl, 'Object']
    published: Optional[datetime] = None

    def to_dict(self):
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.id,
            "type": self.type,
            "actor": self.actor,
            "object": self.object,
            "published": self.published
        }

class Create(Activity):
    type: str = "Create"

class Like(Activity):
    type: str = "Like"

class Follow(Activity):
    type: str = "Follow"

# To avoid circular imports
from app.activitypub.object import Object
Activity.update_forward_refs()

# Additional improvements for handling activity sending/receiving will go here
