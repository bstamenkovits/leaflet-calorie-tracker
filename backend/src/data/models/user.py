from typing import Optional
from pydantic import BaseModel, Field
from util.hash import generate_technical_key


class UserData(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str

    def model_post_init(self, __context):
        """Called after model initialization to set computed fields"""
        if not self.id:
            self.id = generate_technical_key(self.name)

    def to_dict(self):
        """Convert to dictionary for Supabase"""
        return self.model_dump()
