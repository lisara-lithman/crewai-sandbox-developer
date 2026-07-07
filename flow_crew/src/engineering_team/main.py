#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

import engineering_team.patch  # noqa: F401 — applies CrewAI MCP monkey-patch on import
from engineering_team.crew import EngineeringTeam
from .tools.sand_box_tool import reset_sandbox
from crewai.flow.flow import Flow, start, listen
from crewai import Crew, Process
from pydantic import BaseModel

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

requirements = """
A personal finance dashboard.
The system should allow users to log income and expenses, selecting a category (e.g., Food, Rent, Entertainment, Savings) and providing the amount.
The system should allow users to set monthly budget limits for each category and trigger a warning/alert in the UI if a new expense exceeds that category's budget.
The system should calculate the total savings rate and identify the top spending category.
The data MUST be managed entirely in active memory (no database or file saving required).
The frontend MUST feature a clean, multi-tab layout:
- Tab 1: Financial Dashboard, displaying a clean table (Dataframe) of all transactions, the current total balance, savings rate, and any active budget alerts. The dashboard must update dynamically whenever transactions are added.
- Tab 2: Transaction Entry, providing interactive forms to Log Income and Log Expense.
- Tab 3: Budget Settings, allowing users to define category budgets.
"""


def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
    }

    try:
        reset_sandbox()
        EngineeringTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "requirements": "Build a simple task manager application."
    }
    try:
        EngineeringTeam().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EngineeringTeam().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "requirements": "Build a simple task manager application."
    }

    try:
        EngineeringTeam().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        'requirements': 'Build a simple task manager application.'
    }

    try:
        result = EngineeringTeam().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


# ==============================================================================
# CrewAI Flow Configuration
# ==============================================================================

class LibraryState(BaseModel):
    requirements: str = ""
    design_spec: str = ""
    code_output: str = ""

class DevelopmentFlow(Flow[LibraryState]):

    @start()
    def plan_and_design(self):
        """Stage 1: Engineering Lead prepares the design doc"""
        print("\n==========================================")
        print("STAGE 1: PLAN & DESIGN (Flow)")
        print("==========================================\n")
        
        self.state.requirements = requirements
        reset_sandbox()
        team = EngineeringTeam()
        
        design_crew = Crew(
            agents=[team.engineering_lead()],
            tasks=[team.design_task()],
            verbose=True
        )
        result = design_crew.kickoff(inputs={"requirements": self.state.requirements})
        self.state.design_spec = result.raw
        return result.raw

    @listen(plan_and_design)
    def write_code(self, design_specs):
        """Stage 2: Backend + Frontend Engineers write the app based on specs"""
        print("\n==========================================")
        print("STAGE 2: DEVELOPMENT & UI (Flow)")
        print("==========================================\n")
        
        team = EngineeringTeam()
        dev_crew = Crew(
            agents=[team.backend_engineer(), team.frontend_engineer()],
            tasks=[team.code_task(), team.frontend_task()],
            verbose=True
        )
        result = dev_crew.kickoff(inputs={"requirements": self.state.requirements})
        self.state.code_output = result.raw
        
        print("\n==========================================")
        print("FLOW COMPLETED SUCCESSFULLY!")
        print("==========================================\n")
        return result.raw

def run_flow():
    """Entrypoint to kickoff the flow."""
    flow = DevelopmentFlow()
    flow.kickoff()


