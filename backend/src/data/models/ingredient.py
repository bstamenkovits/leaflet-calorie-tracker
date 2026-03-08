from typing import Optional
from pydantic import BaseModel, Field
from util.hash import generate_technical_key



class IngredientData(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str
    calories_kcal: float
    fat_g: float
    carbs_g: float
    protein_g: float
    type: str

    def model_post_init(self, __context):
        """Called after model initialization to set computed fields"""
        if not self.id:
            input_str = f"{self.name}{self.calories_kcal}{self.fat_g}{self.carbs_g}{self.protein_g}{self.type}"
            self.id = generate_technical_key(input_str)

    def to_dict(self):
        """Convert to dictionary for Supabase"""
        return self.model_dump()
