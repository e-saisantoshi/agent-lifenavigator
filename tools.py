"""
tools.py

Utility "tools" used by agents: meal planning, calendar reading, exporting files.
These simulate external tools (OpenAPI, calendar, etc.) in a lightweight way.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional


# ----------------------------
# Meal Planning Tool
# ----------------------------

def generate_meal_plan(
    diet_type: str,
    budget_level: str,
    avoid_ingredients: List[str],
) -> Dict[str, Dict[str, str]]:
    """
    Generates a simple weekly meal plan.
    In a real system, this would call an OpenAPI nutrition / recipe service.
    """
    base_breakfast = "Oatmeal with fruits"
    base_lunch = "Grilled chicken with veggies"
    base_dinner = "Rice, lentils, and salad"

    if diet_type.lower() == "vegetarian":
        base_lunch = "Paneer / tofu with veggies"
        base_dinner = "Dal, rice, and mixed veg"
    elif diet_type.lower() == "vegan":
        base_breakfast = "Overnight oats with plant milk and fruits"
        base_lunch = "Tofu stir-fry with vegetables"
        base_dinner = "Chickpea curry with rice"

    if budget_level.lower() == "low":
        base_breakfast = "Homemade oats with banana"
        base_lunch = "Rice + lentils"
        base_dinner = "Simple vegetable curry + rice"

    def maybe_remove_avoids(desc: str) -> str:
        for ingredient in avoid_ingredients:
            if ingredient.lower() in desc.lower():
                desc = desc.replace(ingredient, "alternative ingredient")
        return desc

    meal_plan: Dict[str, Dict[str, str]] = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for d in days:
        meal_plan[d] = {
            "Breakfast": maybe_remove_avoids(base_breakfast),
            "Lunch": maybe_remove_avoids(base_lunch),
            "Dinner": maybe_remove_avoids(base_dinner),
        }

    return meal_plan


def generate_shopping_list(
    meal_plan: Dict[str, Dict[str, str]]
) -> List[str]:
    """
    Very naive shopping list generator: just returns a static list.
    In a real implementation, parse ingredients from meal descriptions.
    """
    return [
        "Oats",
        "Rice",
        "Lentils",
        "Mixed vegetables",
        "Fruits",
        "Milk / Plant milk",
        "Spices",
        "Oil",
        "Yogurt / Plant yogurt",
    ]


# ----------------------------
# Calendar Tool
# ----------------------------

def read_calendar_events(source: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Simulates reading calendar events.
    In a real system, integrate Google Calendar API via OpenAPI / SDK.
    """
    # You could read from a JSON file here instead if `source` is provided.
    return [
        {
            "start": "2025-11-28 10:00",
            "end": "2025-11-28 11:00",
            "title": "Team standup meeting",
            "location": "Online",
        },
        {
            "start": "2025-11-29 14:00",
            "end": "2025-11-29 15:00",
            "title": "Doctor appointment",
            "location": "Clinic",
        },
    ]


# ----------------------------
# Export Tool
# ----------------------------

def write_markdown_plan(output_path: str, markdown: str) -> None:
    """
    Writes markdown content to a file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)
