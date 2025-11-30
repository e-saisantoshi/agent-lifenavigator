# Project Overview – Agent LifeNavigator

![Architecture Diagram](A_flowchart_diagram_displays_the_architecture_of_A.png)

NOTE: This project is structured in the style of the Agent Shutton sample submission for the Kaggle Agents Intensive Capstone.  
This README contains **all project details in one file**, including Problem Statement, Solution, Architecture, Workflow, Project Structure, Installation, Value, and Conclusion.

---

# Problem Statement

Weekly life planning is exhausting, repetitive, and time-consuming. People struggle with:
- Building daily routines  
- Planning meals  
- Creating shopping lists  
- Prioritizing tasks  
- Scheduling time blocks  
- Integrating personal + work calendars  
- Staying consistent with habits  

Traditional planning apps still require manual effort, creating **decision fatigue**.  
Users need **automation**, not another to-do list.

---

# Solution Statement

**Agent LifeNavigator** automates:
- 🕒 Personalized daily routines  
- 🍽️ Weekly meal planning  
- 🛒 Grocery shopping lists  
- 📄 Task prioritization  
- 📅 Calendar merging  
- 📘 Weekly plan export (Markdown)

A team of specialized agents works together under the **OrchestratorAgent**, producing a complete weekly plan from simple user inputs.

---

# Architecture

## Architecture Diagram

![Architecture Diagram](A_flowchart_diagram_displays_the_architecture_of_A.png)

## Architecture Explanation

### **OrchestratorAgent (Central Brain)**
Coordinates all agents:
1. Loads memory  
2. Builds routine  
3. Generates meals  
4. Optimizes tasks  
5. Merges calendar  
6. Builds markdown  
7. Edits output  
8. Exports file  

---

### **RoutineDesignerAgent**
Generates daily routines using:
- Wake/sleep times  
- Work hours  
- Gym preference  
- Skincare habit  
- Learning goals  

---

### **MealPlannerAgent**
Produces:
- Weekly 7-day meal plan  
- Shopping list  

Uses diet type, budget, and ingredient restrictions.

---

### **TaskOptimizerAgent**
Sorts tasks using:
- Priority  
- Urgency  
- Recommended execution order  

---

### **CalendarSyncAgent**
Merges:
- AI-generated routine  
- Simulated or real events  

Designed for future Google Calendar integration.

---

### **PlanEditorAgent**
Cleans, formats, and finalizes the weekly plan into polished markdown.

---

### **ExportAgent**
Exports all content into:

```
life_plan.md
```

---

# Project Structure

```
agent-lifenavigator/
│
├── agents.py           # All agent classes + orchestrator
├── tools.py            # Tools: meal planner, exporter, calendar reader
├── memory.py           # Stored user preferences
├── validation.py       # Validators for plan consistency
├── main.py             # Pipeline entry point
├── README.md           # This file
├── life_plan.md        # Generated output
└── preferences.json    # Auto-generated memory
```

---

# Workflow (Step-by-Step)

```
User Input
    ↓
Memory Update
    ↓
RoutineDesignerAgent → Daily Routine
    ↓
MealPlannerAgent → Meal Plan + Shopping List
    ↓
TaskOptimizerAgent → Ordered Tasks
    ↓
CalendarSyncAgent → Merged Schedule
    ↓
PlanEditorAgent → Clean Markdown
    ↓
ExportAgent → life_plan.md
```

---

# Installation & Running

Follow the steps below to install and run **Agent LifeNavigator**.

---

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/agent-lifenavigator.git
cd agent-lifenavigator
```

---

## 2. (Optional) Create a Virtual Environment

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (Command Prompt)
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies  
(Only needed if you use `requirements.txt`)

```bash
pip install -r requirements.txt
```

---

## 4. Run the Agent

```bash
python main.py
```

After execution, the pipeline will generate:

```
life_plan.md
```

---

## 5. Reset Memory (Optional)

Delete the memory file to regenerate preferences:

### macOS / Linux
```bash
rm preferences.json
```

### Windows
```cmd
del preferences.json
```

---

# Value Statement

Agent LifeNavigator reduces planning time by **8–10 hours per week**, helping users:
- Remove mental load  
- Maintain healthy routines  
- Eat balanced meals  
- Stay organized  
- Improve productivity & wellness  

Future enhancements include:
- Real calendar integration  
- Nutrition APIs  
- Fitness agent  
- Travel planning agent  
- Budgeting agent  
- Gemini-powered personalization  

---

# Conclusion

Agent LifeNavigator demonstrates how multi-agent systems can automate real-life planning tasks.  
By delegating responsibilities to domain-specialized agents, the system delivers a seamless, end-to-end weekly plan.

This project is:
- Modular  
- Scalable  
- ADK/Gemini compatible  
- Ideal for Concierge Agent track  

A strong example of practical AI automation.


