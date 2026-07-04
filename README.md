# CrewAI Process Model Comparison: Sequential vs. Hierarchical

This repository contains a side-by-side comparison of two CrewAI execution processes—**Sequential** and **Hierarchical**—used to build an **In-Memory Smart Library & Book Reservation System** with a Gradio frontend.

---

## 📊 Summary of Differences

| Feature | 📂 Hierarchical Version (`engineering_team`) | 📂 Sequential Version (`engineering_team1`) |
| :--- | :--- | :--- |
| **Execution Flow** | **Orchestrated by Manager:** The `engineering_lead` acts as the manager, dynamically planning and delegating tasks to workers. | **Strict Linear Pipeline:** Executed sequentially from task to task: Lead ➡️ Backend ➡️ Frontend ➡️ Test. |
| **Backend File** | `library_system.py` | `library.py` |
| **Frontend Setup** | Direct class injection (defines `Book`, `Member`, `Library` directly inside `app.py`). | Modular imports (defines helper functions wrapping methods imported from `library.py`). |
| **Member Management** | Automatic member instantiation during borrows to prevent deadlock. | Automatic member instantiation during borrows to prevent deadlock. |
| **Gradio UI Layout** | Multi-tab Blocks UI with a live catalog table that refreshes on borrowing, returning, and adding books. | Multi-tab Blocks UI with a live catalog table that refreshes on borrowing, returning, and adding books. |
| **Test Suite** | `test_library_system.py` (std unittest) | `test_library.py` (std unittest) |

---

## 🛠️ Project Structures

### 📂 `engineering_team/` (Hierarchical Process)
```text
engineering_team/
├── src/
│   └── engineering_team/
│       ├── config/
│       │   ├── agents.yaml      # Configures gpt-4o-mini agents
│       │   └── tasks.yaml       # Defines tasks
│       ├── main.py              # Main entry point with requirements
│       └── crew.py              # Instantiates Crew with process=Process.hierarchical
└── sandbox/
    ├── app.py                   # Gradio Web Interface (Hierarchical)
    ├── library_system.py        # Backend class
    └── test_library_system.py   # Unit test suite
```

### 📂 `engineering_team1/` (Sequential Process)
```text
engineering_team1/
├── src/
│   └── engineering_team/
│       ├── config/
│       │   ├── agents.yaml      # Configures gpt-4o-mini agents
│       │   └── tasks.yaml       # Defines tasks
│       ├── main.py              # Main entry point with requirements
│       └── crew.py              # Instantiates Crew with process=Process.sequential
└── sandbox/
    ├── app.py                   # Gradio Web Interface (Sequential)
    ├── library.py               # Backend class
    └── test_library.py          # Unit test suite
```

---

## 🚀 How to Run the Applications

Ensure you have your environment keys configured in `.env` in the root of the respective project directory:
```env
OPENAI_API_KEY=your-key-here
```

### 1. Hierarchical Version
To run the hierarchical crew and launch the Gradio UI:
```bash
# Navigate to the hierarchical directory
cd engineering_team

# Run the crew (optional if already run)
crewai run

# Start the Gradio Web Application
uv run --project sandbox python sandbox/app.py
```
*Open your browser and visit: `http://127.0.0.1:7860`*

### 2. Sequential Version
To run the sequential crew and launch the Gradio UI:
```bash
# Navigate to the sequential directory
cd ../engineering_team1

# Run the crew (optional if already run)
crewai run

# Start the Gradio Web Application
uv run --project sandbox python sandbox/app.py
```
*Open your browser and visit: `http://127.0.0.1:7860`*
