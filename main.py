"""
main.py
Entry point for Agent LifeNavigator.
"""

from __future__ import annotations
from typing import Any, Dict, List

from agents import OrchestratorAgent
from memory import PreferenceMemory


def build_sample_user_profile() -> Dict[str, Any]:
    return {
        "name": "Sai",
        "wake_time": "07:00",
        "sleep_time": "23:00",
        "work_start": "09:00",
        "work_end": "17:00",
        "wants_gym": True,
        "wants_skincare": True,
        "wants_learning": True,
        "diet_type": "balanced",
        "budget_level": "medium",
        "avoid_ingredients": ["milk"],
    }


def build_sample_tasks() -> List[Dict[str, Any]]:
    return [
        {"title": "Pay electricity bill", "priority": 1},
        {"title": "Deep clean kitchen", "priority": 2},
        {"title": "Update resume", "priority": 1},
        {"title": "Read 20 pages", "priority": 3},
        {"title": "Call parents", "priority": 2},
    ]


def main() -> None:
    memory = PreferenceMemory(path="preferences.json")

    orchestrator = OrchestratorAgent(memory=memory)

    user_profile = build_sample_user_profile()
    tasks = build_sample_tasks()
    output_path = "life_plan.md"

    result = orchestrator.run_full_pipeline(
        user_profile=user_profile,
        tasks=tasks,
        calendar_source=None,
        output_path=output_path,
    )

    print("\n=== LifeNavigator Run Complete ===")
    print(f"Plan saved to: {result['saved_path']}")


if __name__ == "__main__":
    main()
