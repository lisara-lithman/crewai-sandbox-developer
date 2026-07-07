# CrewAI Orchestration Comparison: Sequential vs. Hierarchical vs. Flows

This repository contains a side-by-side comparison of three different CrewAI orchestration models used to build an **In-Memory Personal Finance Dashboard** with a Gradio frontend:

1. **Sequential Crew (`sequential_crew/`)** - A single crew running tasks in a strict linear pipeline.
2. **Hierarchical Crew (`hierarchical_crew/`)** - A single crew managed by the Engineering Lead agent, who delegates tasks dynamically.
3. **CrewAI Flow (`flow_crew/`)** - A state-driven Python Flow that coordinates multiple smaller, specialized crews in separate stages.

---

## 📊 Summary of Process Differences

| Feature | 📂 Sequential Crew (`sequential_crew`) | 📂 Hierarchical Crew (`hierarchical_crew`) | 📂 CrewAI Flow (`flow_crew`) |
| :--- | :--- | :--- | :--- |
| **Orchestration Model** | **Linear Pipeline:** Lead ➡️ Backend ➡️ Frontend ➡️ Test. | **Manager Delegation:** Engineering Lead agent dynamically assigns tasks to workers. | **State-Driven Flow:** Python state coordinates and runs separate mini-crews sequentially. |
| **Crew Configuration** | All 4 agents and 4 tasks run in a single sequential execution block. | All 4 agents and 4 tasks run in a single hierarchical execution block. | Groups the existing agents dynamically into separate stage-based executions (`Design`, `Development`, `QA`). |
| **State Management** | Shared context passed through sequential task parameters. | Managed dynamically by the manager agent. | Shared state defined in a Pydantic `LibraryState` schema and passed using `@listen` triggers. |

---

## 🛠️ Project Structures

All three folders share the same underlying agents and tasks YAML declarations, but execution is triggered differently:

* **`hierarchical_crew/`** - Configured with `process=Process.hierarchical` and `manager_agent=self.engineering_lead()` in `crew.py`.
* **`sequential_crew/`** - Configured with `process=Process.sequential` in `crew.py`.
* **`flow_crew/`** - Orchestrated using the `DevelopmentFlow` class in `main.py` which triggers mini-crews stage-by-stage.

---

## 🚀 How to Run the Applications

Make sure to configure your `.env` in the root of the respective project directory:
```env
OPENAI_API_KEY=your-key-here
```

### 1. Hierarchical Version (`hierarchical_crew/`)
```bash
cd hierarchical_crew

# Run the crew
crewai run

# Launch the Gradio Web App
uv run --project sandbox python sandbox/app.py
```

### 2. Sequential Version (`sequential_crew/`)
```bash
cd sequential_crew

# Run the crew
crewai run

# Launch the Gradio Web App
uv run --project sandbox python sandbox/app.py
```

### 3. CrewAI Flow Version (`flow_crew/`)
```bash
cd flow_crew

# Run the Flow
uv run run_flow

# Launch the Gradio Web App
uv run --project sandbox python sandbox/app.py
```
*Gradio instances run locally on `http://127.0.0.1:7860`.*
