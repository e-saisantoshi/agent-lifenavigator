# user_input.py
import json
import os

DEFAULT_PROFILE = {
    "name": "User",
    "wake_time": "07:00",
    "sleep_time": "23:00",
    "work_start": "09:00",
    "work_end": "17:00",
    "wants_gym": True,
    "wants_learning": True,
    "wants_skincare": True,
    "diet_type": "balanced",
    "budget_level": "medium",
    "avoid_ingredients": ["milk"]
}


def load_user_profile(path: str = "profile.json") -> dict:
    """
    Load user preferences from a JSON file.
    If it doesn't exist or fails, fall back to DEFAULT_PROFILE.
    """
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_PROFILE
    return DEFAULT_PROFILE


def ask_user_interactively() -> dict:
    """
    Ask the user for their preferences via the terminal.
    """
    print("\n===== Create New LifeNavigator Profile =====\n")

    name = input("Your name: ").strip() or "User"
    wake = input("Wake-up time (HH:MM, default 07:00): ").strip() or "07:00"
    sleep = input("Sleep time (HH:MM, default 23:00): ").strip() or "23:00"
    work_start = input("Work start time (HH:MM, default 09:00): ").strip() or "09:00"
    work_end = input("Work end time (HH:MM, default 17:00): ").strip() or "17:00"

    wants_gym = input("Do you want gym in your routine? (y/n): ").lower().startswith("y")
    wants_learning = input("Do you want a learning block? (y/n): ").lower().startswith("y")
    wants_skincare = input("Do you want skincare steps? (y/n): ").lower().startswith("y")

    diet = input("Diet type (balanced/vegetarian/vegan/high-protein, default balanced): ").strip() or "balanced"
    budget = input("Budget level (low/medium/high, default medium): ").strip() or "medium"
    avoid_raw = input("Ingredients to avoid (comma separated, optional): ").strip()
    avoid_list = [a.strip() for a in avoid_raw.split(",")] if avoid_raw else []

    return {
        "name": name,
        "wake_time": wake,
        "sleep_time": sleep,
        "work_start": work_start,
        "work_end": work_end,
        "wants_gym": wants_gym,
        "wants_learning": wants_learning,
        "wants_skincare": wants_skincare,
        "diet_type": diet,
        "budget_level": budget,
        "avoid_ingredients": avoid_list
    }
