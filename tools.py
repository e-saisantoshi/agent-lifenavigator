# tools.py
from typing import Dict, List, Tuple, Union
from gemini_agent import llm


class BaseTool:
    def __init__(self, name: str):
        self.name = name

    def log(self, message: str):
        print(f"[{self.name}] {message}")


class MealPlanner(BaseTool):
    """
    Generates a weekly meal plan and shopping list.
    Can use Gemini for highly personalized plans or fallback to rule-based.
    """

    def generate_meal_plan(
        self,
        prefs: dict,
        personality: dict,
        use_llm: bool = False
    ) -> Tuple[Dict[str, Union[str, Dict[str, str]]], List[str]]:
        self.log("Generating weekly meal plan...")

        if use_llm:
            prompt = f"""
You are a nutritionist and meal planning expert.

User profile:
{prefs}

Behavioral profile:
{personality}

Task:
Create a 7-day meal plan (Breakfast, Lunch, Dinner).
Follow these rules:
- Respect diet type: {personality.get('diet_type')}
- Respect budget level: {personality.get('budget_level')}
- Avoid ingredients: {', '.join(personality.get('restrictions', []))}
- Meals should be realistic and culturally neutral.
- Output in this format:

Monday:
- Breakfast: ...
- Lunch: ...
- Dinner: ...

Tuesday:
- Breakfast: ...
...

Return only the plan in plain text.
            """
            plan_text = llm(prompt)
            meals = {"LLM-Generated Weekly Meal Plan": plan_text}
        else:
            # Simple rule-based fallback
            default_breakfast = "Oatmeal with fruits"
            if "milk" in personality.get("restrictions", []):
                default_breakfast = "Oatmeal with plant-based milk and fruits"

            base_meal = {
                "Breakfast": default_breakfast,
                "Lunch": "Grilled chicken with veggies"
                if personality.get("diet_type") != "vegetarian"
                else "Paneer / tofu with veggies",
                "Dinner": "Rice, lentils, and salad"
            }

            meals = {
                day: base_meal
                for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            }

        # Shopping list (can be improved / LLM-generated later)
        shopping_list = [
            "Oats",
            "Rice",
            "Lentils",
            "Mixed vegetables",
            "Fruits",
            "Cooking oil",
            "Spices"
        ]

        return meals, shopping_list


class TaskOptimizer(BaseTool):
    """
    Orders and enhances tasks based on user profile.
    """

    def optimize_tasks(
        self,
        prefs: dict,
        personality: dict,
        use_llm: bool = False
    ) -> Union[List[str], str]:
        self.log("Optimizing tasks...")

        base_tasks = [
            "Pay electricity bill",
            "Update resume",
            "Deep clean kitchen",
            "Call parents",
            "Read 20 pages of a book"
        ]

        if use_llm:
            prompt = f"""
You are a productivity coach.

Given this user profile:
{prefs}

And behavior profile:
{personality}

Reorder and enhance the following tasks.
- Add priorities (1 = highest).
- Suggest 1–2 extra personalized tasks if relevant.

Tasks:
{base_tasks}

Return output in bullet list format with (priority) Task.
            """
            return llm(prompt)

        # Simple priority ordering (rule-based)
        prioritized = [
            "(1) Pay electricity bill",
            "(1) Update resume",
            "(2) Deep clean kitchen",
            "(2) Call parents",
            "(3) Read 20 pages of a book"
        ]
        return prioritized


class CalendarManager(BaseTool):
    """
    Merges generated content with static or external events.
    """

    def merge_with_events(self, routine_text: str) -> dict:
        self.log("Merging routine with calendar events...")

        events = [
            "2025-11-28 10:00 Team standup meeting (Online)",
            "2025-11-29 14:00 Doctor appointment (Clinic)"
        ]

        return {
            "routine": routine_text,
            "events": events
        }


class MarkdownBuilder(BaseTool):
    """
    Assembles the final life plan into a Markdown document.
    """

    def build_markdown(
        self,
        prefs: dict,
        personality: dict,
        routine: str,
        meals: dict,
        shopping: List[str],
        tasks: Union[List[str], str],
        calendar: dict
    ) -> str:
        self.log("Building final markdown...")

        md = f"# Agent LifeNavigator – Weekly Plan for {prefs.get('name', 'User')}\n\n"

        md += "## 1. Personalized Profile Summary\n"
        for k, v in personality.items():
            md += f"- **{k}**: {v}\n"
        md += "\n"

        md += "## 2. Daily Routine\n"
        md += routine + "\n\n"

        md += "## 3. Weekly Meal Plan\n"
        for day, plan in meals.items():
            md += f"### {day}\n"
            if isinstance(plan, dict):
                for meal_type, item in plan.items():
                    md += f"- **{meal_type}**: {item}\n"
            else:
                # LLM-generated text block
                md += plan + "\n"
            md += "\n"

        md += "## 4. Shopping List\n"
        for item in shopping:
            md += f"- {item}\n"
        md += "\n"

        md += "## 5. Optimized Tasks\n"
        if isinstance(tasks, list):
            for item in tasks:
                md += f"- {item}\n"
        else:
            md += tasks + "\n"
        md += "\n"

        md += "## 6. Calendar Schedule\n"
        for event in calendar["events"]:
            md += f"- {event}\n"

        md += "\n---\nGenerated by Agent LifeNavigator.\n"
        return md
