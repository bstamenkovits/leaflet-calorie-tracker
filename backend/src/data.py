from fastapi import APIRouter


sample_data = [
    {
        "id": 1,
        "meal": "Breakfast",
        "ingredient": "Bread",
        "quantity": "2",
        "unit": "slices",
        "calories": 150
    },
    {
        "id": 2,
        "meal": "Breakfast",
        "ingredient": "Cheese",
        "quantity": "1",
        "unit": "slice",
        "calories": 100
    },
    {
        "id": 3,
        "meal": "Lunch",
        "ingredient": "Chicken Breast",
        "quantity": "200",
        "unit": "grams",
        "calories": 330
    },
    {
        "id": 4,
        "meal": "Lunch",
        "ingredient": "Rice",
        "quantity": "1",
        "unit": "cup",
        "calories": 200
    },
]


router = APIRouter(prefix="/api", tags=["data"])


@router.get("/food-logs")
async def get_food_logs():
    return sample_data
