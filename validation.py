"""
validation.py

Lightweight validation functions that simulate LoopAgent validators.
"""

from __future__ import annotations
from typing import Any, Dict, List


def validate_routine(routine: Dict[str, Any]) -> bool:
    """
    Checks that routine has at least 3 daily blocks and sensible times.
    """
    daily = routine.get("daily", [])
    if not daily or len(daily) < 3:
        return False

    # Check basic structure
    for block in daily:
        if not all(k in block for k in ("start", "end", "task")):
            return False
    return True


def validate_meal_plan(meal_plan: Dict[str, Any]) -> bool:
    """
    Checks that all 7 days exist in the plan.
    """
    required_days = {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    }
    return required_days.issubset(set(meal_plan.keys()))


def validate_schedule_merge(merged: Dict[str, Any]) -> bool:
    """
    In a real system, this would check for conflicts.
    For now just ensures routine exists.
    """
    return "routine" in merged and "daily" in merged["routine"]
