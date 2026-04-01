# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup (first time)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_scheduler.py

# Run a specific test
pytest tests/test_scheduler.py::test_function_name
```

## Architecture

This is a **student project** (CodePath Module 2). The app is intentionally incomplete — the starter code provides only a thin Streamlit shell. The student's job is to design and implement the scheduling logic, then wire it into the UI.

**Core layers to build:**

- **Domain classes** (e.g., `Pet`, `Owner`, `Task`) — typically in a separate module like `pawpal_system.py`
- **Scheduler** — a class or function that takes tasks + constraints and produces an ordered daily plan
- **Streamlit UI** (`app.py`) — connects user inputs to the scheduler and displays results

**Key design constraints:**
- Tasks have at minimum: title, duration (minutes), priority (low/medium/high)
- The scheduler must consider time availability and priority to produce a ranked/ordered plan
- The plan should include an explanation of why each task was chosen/ordered

**`app.py`** currently holds demo UI with hardcoded inputs. The "Generate schedule" button is a stub — it should be replaced with a call to the real scheduler once implemented.

**`reflection.md`** is a required project deliverable (not code) — it documents design decisions, tradeoffs, and AI collaboration.
