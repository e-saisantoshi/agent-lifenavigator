# main.py
from agents import OrchestratorAgent
from user_input import load_user_profile, ask_user_interactively
from personality_engine import personalize_profile

# Toggle: True = use Gemini 2.0 Pro, False = offline rule-based
USE_LLM = True


def main():
    print("\n=== Agent LifeNavigator ===")
    print("1) Load profile.json")
    print("2) Enter new profile manually")
    print("3) Use default profile\n")

    choice = input("Select option (1/2/3): ").strip()

    if choice == "1":
        raw_prefs = load_user_profile("profile.json")
    elif choice == "2":
        raw_prefs = ask_user_interactively()
    else:
        raw_prefs = load_user_profile("profile.json")  # will fall back to default if missing

    personality = personalize_profile(raw_prefs)

    orchestrator = OrchestratorAgent(
        use_llm=USE_LLM,
        user_prefs=raw_prefs,
        personality=personality
    )

    print("\nRunning LifeNavigator pipeline...\n")
    result_md = orchestrator.run_full_pipeline()

    output_file = "life_plan.md"
    with open(output_file, "w") as f:
        f.write(result_md)

    print(f"\n✔ Life plan generated for {raw_prefs.get('name', 'User')}")
    print(f"📄 Saved to: {output_file}\n")


if __name__ == "__main__":
    main()
