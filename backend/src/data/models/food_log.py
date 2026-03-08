import datetime
from typing import Optional
from pydantic import BaseModel, Field
from util.hash import generate_technical_key


class FoodLogData(BaseModel):
    id: Optional[str] = Field(default=None)
    meal_id: str
    ingredient_id: str
    serving_id: str
    user_id: str
    quantity: float
    date_added: datetime.datetime = Field(default_factory=datetime.datetime.now)

    def model_post_init(self, __context):
        """Called after model initialization to set computed fields"""
        if not self.id:
            input_str = f"{self.meal_id}{self.ingredient_id}{self.serving_id}{self.user_id}{self.date_added}{self.quantity}"
            self.id = generate_technical_key(input_str)

    def to_dict(self):
        """Convert to dictionary with datetime as ISO string for Supabase"""
        data = self.model_dump()

        # Convert datetime to ISO format string (required for Supabase)
        data['date_added'] = self.date_added.isoformat()
        return data
