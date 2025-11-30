"""
agents.py

Core multi-agent classes for Agent LifeNavigator.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from tools import (
    generate_meal_plan,
    generate_shopping_list,
    read_calendar_events,
    write_markdown_plan,
)
from memory import PreferenceMemory
from validation import (
    validate_routine,
    validate_meal_plan,
    validate_schedule_merge,
)


# ----------------------------
# Base Agent
# ----------------------------

class BaseAgent:
    """Base class for all agents."""

    def __init__(self, name: str, memory: Optional[PreferenceMemory] = None):
        self.name = name
        self.memory = memory

    def log(self, message: str) -> None:
        print(f"[{self.name}] {message}")

    def run(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement run()")


# ----------------------------
# Routine Designer Agent
# ----------------------------

class RoutineDesignerAgent(BaseAgent):
    def run(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        self.log("Designing routine...")

        wake_time = user_profile.get("wake_time", "07:00")
        sleep_time = user_profile.get("sleep_time", "23:00")
        work_start = user_profile.get("work_start", "09:00")
        work_end = user_profile.get("work_end", "17:00")
        wants_gym = user_profile.get("wants_gym", True)
        wants_skincare = user_profile.get("wants_skincare", True)
        wants_learning = user_profile.get("wants_learning", True)

        routine: Dict[str, List[Dict[str, str]]] = {"daily": []}

        routine["daily"].append(
            {"start": wake_time, "end": "07:30", "task": "Morning hygiene & skincare"}
        )
        routine["daily"].append(
            {"start": "07:30", "end": "08:00", "task": "Breakfast"}
        )
        routine["daily"].append(
            {"start": work_start, "end": work_end, "task": "Work / Study"}
        )

        if wants_gym:
            routine["daily"].append(
                {"start": "18:00", "end": "19:00", "task": "Gym / Workout"}
            )

        if wants_learning:
            routine["daily"].append(
                {"start": "19:30", "end": "20:30", "task": "Learning / Upskilling"}
            )

        if wants_skincare:
            routine["daily"].append(
                {"start": "22:30", "end": sleep_time, "task": "Night skincare & wind down"}
            )
        else:
            routine["daily"].append(
                {"start": "22:30", "end": sleep_time, "task": "Wind down / Relax"}
            )

        if not validate_routine(routine):
            self.log("Routine validation failed. Using fallback routine...")
            routine = {
                "daily": [
                    {"start": wake_time, "end": work_start, "task": "Morning routine"},
                    {"start": work_start, "end": work_end, "task": "Work / Study"},
                    {"start": "18:00", "end": sleep_time, "task": "Evening routine"},
                ]
            }

        self.log("Routine created successfully.")
        return routine


# ----------------------------
# Meal Planner Agent
# ----------------------------

class MealPlannerAgent(BaseAgent):
    def run(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        self.log("Generating meal plan...")

        diet = user_profile.get("diet_type", "balanced")
        budget = user_profile.get("budget_level", "medium")
        avoids = user_profile.get("avoid_ingredients", [])

        meal_plan = generate_meal_plan(diet, budget, avoids)

        if not validate_meal_plan(meal_plan):
            self.log("Meal plan validation failed. Using fallback...")
            meal_plan = generate_meal_plan("balanced", "low", [])

        shopping_list = generate_shopping_list(meal_plan)
        self.log("Meal plan generated successfully.")
        return {"meal_plan": meal_plan, "shopping_list": shopping_list}


# ----------------------------
# Task Optimizer Agent
# ----------------------------

class TaskOptimizerAgent(BaseAgent):
    def run(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.log("Optimizing tasks...")
        sorted_tasks = sorted(tasks, key=lambda t: t.get("priority", 3))
        for index, task in enumerate(sorted_tasks, start=1):
            task["recommended_order"] = index
        self.log("Task optimization complete.")
        return sorted_tasks


# ----------------------------
# Calendar Sync Agent
# ----------------------------

class CalendarSyncAgent(BaseAgent):
    def run(self, routine: Dict[str, Any], source: Optional[str] = None) -> Dict[str, Any]:
        self.log("Reading calendar...")
        events = read_calendar_events(source)

        merged = {
            "routine": routine,
            "calendar_events": events,
            "notes": "Calendar merged (simple mode)."
        }

        if not validate_schedule_merge(merged):
            self.log("Validation failed. Returning routine only.")
            merged["calendar_events"] = []
            merged["notes"] = "Calendar unavailable."

        self.log("Calendar merged successfully.")
        return merged


# ----------------------------
# Plan Editor Agent
# ----------------------------

class PlanEditorAgent(BaseAgent):
    def run(self, text: str) -> str:
        self.log("Editing final plan output...")
        cleaned = text.strip() + "\n\n---\nGenerated by Agent LifeNavigator.\n"
        return cleaned


# ----------------------------
# Export Agent
# ----------------------------

class ExportAgent(BaseAgent):
    def run(self, markdown: str, output_path: str) -> str:
        self.log(f"Saving plan to {output_path}...")
        write_markdown_plan(output_path, markdown)
        self.log("Export complete.")
        return output_path


# ----------------------------
# Orchestrator Agent
# ----------------------------

@dataclass
class OrchestratorAgent(BaseAgent):
    name: str = "OrchestratorAgent"
    memory: PreferenceMemory = None

    def __post_init__(self):
        super().__init__(name=self.name, memory=self.memory)

        self.routine_agent = RoutineDesignerAgent("RoutineDesigner", self.memory)
        self.meal_agent = MealPlannerAgent("MealPlanner", self.memory)
        self.task_agent = TaskOptimizerAgent("TaskOptimizer", self.memory)
        self.calendar_agent = CalendarSyncAgent("CalendarSync", self.memory)
        self.editor_agent = PlanEditorAgent("PlanEditor", self.memory)
        self.export_agent = ExportAgent("Exporter", self.memory)

    def run_full_pipeline(
        self, user_profile: Dict[str, Any], tasks: List[Dict[str, Any]],
        calendar_source: Optional[str], output_path: str
    ) -> Dict[str, Any]:

        self.log("Starting LifeNavigator pipeline...")

        self.memory.update_preferences(user_profile)
        routine = self.routine_agent.run(user_profile)
        meals = self.meal_agent.run(user_profile)
        optimized = self.task_agent.run(tasks)
        merged = self.calendar_agent.run(routine, calendar_source)

        markdown = self._build_markdown(user_profile, routine, meals, optimized, merged)
        edited = self.editor_agent.run(markdown)
        saved = self.export_agent.run(edited, output_path)

        self.log("Pipeline complete.")
        return {
            "saved_path": saved,
            "routine": routine,
            "meals": meals,
            "optimized_tasks": optimized,
            "merged_schedule": merged,
        }

    def _build_markdown(
        self, profile, routine, meals, optimized, merged
    ) -> str:
        lines = []

        lines.append("# Agent LifeNavigator – Personalized Plan\n")
        lines.append("## 1. User Profile\n")
        for k, v in profile.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

        lines.append("## 2. Daily Routine\n")
        for block in routine.get("daily", []):
            lines.append(f"- {block['start']}–{block['end']}: {block['task']}")
        lines.append("")

        lines.append("## 3. Weekly Meal Plan\n")
        for day, meals_day in meals["meal_plan"].items():
            lines.append(f"### {day}")
            for meal_name, meal_desc in meals_day.items():
                lines.append(f"- **{meal_name}**: {meal_desc}")
            lines.append("")

        lines.append("## 4. Shopping List\n")
        for item in meals["shopping_list"]:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("## 5. Optimized Tasks\n")
        for t in optimized:
            lines.append(
                f"- ({t['recommended_order']}) [Priority {t.get('priority', 3)}] {t['title']}"
            )
        lines.append("")

        lines.append("## 6. Calendar Schedule\n")
        lines.append(merged.get("notes", ""))
        lines.append("")

        if merged["calendar_events"]:
            for e in merged["calendar_events"]:
                lines.append(f"- {e['start']} {e['title']} ({e.get('location', '')})")
        else:
            lines.append("_No calendar events loaded._")

        return "\n".join(lines)
