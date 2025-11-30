# personality_engine.py

def personalize_profile(prefs: dict) -> dict:
    """
    Build a behavioral + lifestyle profile from raw preferences.
    This is what makes each user's plan different, not just their name.
    """

    profile = {}

    # Sleep type
    wake_h = int(prefs["wake_time"].split(":")[0])
    if wake_h < 6:
        profile["sleep_type"] = "early_riser"
    elif wake_h > 9:
        profile["sleep_type"] = "late_riser"
    else:
        profile["sleep_type"] = "regular_riser"

    # Work style
    work_start_h = int(prefs["work_start"].split(":")[0])
    work_end_h = int(prefs["work_end"].split(":")[0])
    work_hours = (work_end_h - work_start_h) % 24

    if work_hours >= 9:
        profile["work_style"] = "heavy_worker"
    elif work_hours <= 5:
        profile["work_style"] = "light_worker"
    else:
        profile["work_style"] = "balanced_worker"

    # Fitness level
    profile["fitness_level"] = "active" if prefs.get("wants_gym") else "low_activity"

    # Learning mindset
    profile["learning_mode"] = "growth_oriented" if prefs.get("wants_learning") else "minimal_learning"

    # Skincare importance
    profile["skincare_importance"] = "high" if prefs.get("wants_skincare") else "low"

    # Diet and budget
    profile["diet_type"] = prefs.get("diet_type", "balanced")
    profile["budget_level"] = prefs.get("budget_level", "medium")
    profile["restrictions"] = prefs.get("avoid_ingredients", [])

    return profile
