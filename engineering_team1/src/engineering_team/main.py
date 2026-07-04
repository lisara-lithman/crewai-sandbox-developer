#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

import engineering_team.patch  # noqa: F401 — applies CrewAI MCP monkey-patch on import
from engineering_team.crew import EngineeringTeam
from .tools.sand_box_tool import reset_sandbox

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

requirements = """
A smart library and book reservation system.
The system should allow users to manage a catalog of books (adding books, title, author, and availability status) entirely in active memory (no database or file saving required).
The system should allow users to borrow and return books, tracking which member borrowed which book.
The system should prevent a book from being borrowed if it is already checked out, and validate member borrows.
The frontend MUST feature a clean, multi-tab layout:
- Tab 1: Book Catalog View, displaying the complete list of books and their current availability in a clean table (Dataframe) that updates dynamically whenever books are added, borrowed, or returned.
- Tab 2: Circulation, providing interactive forms to Borrow and Return books.
- Tab 3: Admin Actions, allowing users to add new books to the catalog.
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

