# agents.py
from gemini_agent import llm
from tools import MealPlanner, TaskOptimizer, CalendarManager, MarkdownBuilder
from memory import MemoryStore


class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def log(self, message: str):
        print(f"[{self.name}] {message}")


class RoutineDesignerAgent(BaseAgent):
    """
    Builds a personalized daily routine using prefs + personality.
    """

    def generate(self, prefs: dict, personality: dict, use_llm: bool = False) -> str:
        self.log("Generating daily routine...")

        if use_llm:
            prompt = f"""
You are a lifestyle optimization coach.

User preferences:
{prefs}

Behavior profile:
{personality}

Task:
Generate a realistic, healthy, and productive weekday routine.
- Use concrete time ranges (HH:MM–HH:MM).
- Include work, breaks, meals, gym (if applicable), learning (if applicable),
  skincare (if applicable), and wind-down time.
- Align energy-high tasks with user's sleep_type and work_style.

Return the routine as bullet points only.
            """
            return llm(prompt)

        # Offline fallback: simple deterministic schedule
        routine = []
        routine.append(f"{prefs['wake_time']}–07:30 Morning hygiene & skincare")
        routine.append(f"{prefs['work_start']}–{prefs['work_end']} Work / Study")

        if prefs.get("wants_gym"):
            routine.append("18:00–19:00 Gym / Workout")

        if prefs.get("wants_learning"):
            routine.append("19:30–20:30 Learning / Upskilling")

        routine.append(f"{prefs['sleep_time']} Wind down & sleep")
        return "\n".join(routine)


class OrchestratorAgent(BaseAgent):
    """
    Coordinates all agents, glues everything together.
    """

    def __init__(self, use_llm: bool = False, user_prefs: dict | None = None, personality: dict | None = None):
        super().__init__("Orchestrator")
        self.use_llm = use_llm
        self.prefs = user_prefs or {}
        self.personality = personality or {}

        self.memory = MemoryStore()

        self.routine_agent = RoutineDesignerAgent("RoutineDesigner")
        self.meal_planner = MealPlanner("MealPlanner")
        self.task_optimizer = TaskOptimizer("TaskOptimizer")
        self.calendar_manager = CalendarManager("CalendarSync")
        self.markdown_builder = MarkdownBuilder("MarkdownBuilder")

    def run_full_pipeline(self) -> str:
        self.log(f"Starting full LifeNavigator pipeline (LLM mode = {self.use_llm})")

        # 1. Routine
        routine_text = self.routine_agent.generate(
            self.prefs, self.personality, self.use_llm
        )

        # 2. Meals
        weekly_meals, shopping_list = self.meal_planner.generate_meal_plan(
            self.prefs, self.personality, self.use_llm
        )

        # 3. Tasks
        optimized_tasks = self.task_optimizer.optimize_tasks(
            self.prefs, self.personality, self.use_llm
        )

        # 4. Calendar
        merged_calendar = self.calendar_manager.merge_with_events(routine_text)

        # 5. Markdown assembly
        final_markdown = self.markdown_builder.build_markdown(
            self.prefs,
            self.personality,
            routine_text,
            weekly_meals,
            shopping_list,
            optimized_tasks,
            merged_calendar
        )

        # 6. Save preferences
        self.memory.save_preferences(self.prefs)

        self.log("Pipeline complete.")
        return final_markdown
