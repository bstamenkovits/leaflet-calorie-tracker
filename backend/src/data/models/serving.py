from typing import Optional
from pydantic import BaseModel, Field
from util.hash import generate_technical_key


class ServingData(BaseModel):
    id: Optional[str] = Field(default=None)
    ingredient_id: str
    name: str
    size_g: float

    def model_post_init(self, __context):
        """Called after model initialization to set computed fields"""
        if not self.id:
            input_str = f"{self.ingredient_id}{self.name}{self.size_g}"
            self.id = generate_technical_key(input_str)

    def to_dict(self):
        """Convert to dictionary for Supabase"""
        return self.model_dump()
