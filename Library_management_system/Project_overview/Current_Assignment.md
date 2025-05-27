# ✅ Assignment 7 – Penalty System + Service Architecture Refactor

## 🎯 Goal:
To improve the robustness, modularity, and scalability of your Library Management System by:
- Implementing a complete Penalty Calculation System.
- Refactoring your library logic into modular service classes.
- Preparing the system for future integration with Flask/FastAPI.

---

## 📌 Part 1: Implement the Penalty System

### 🎯 Objectives:
- Add a configurable penalty policy for late returns (e.g., ₹5 per day).
- Automatically calculate penalties when books are returned.
- Track penalties per member.

### ✅ Tasks:
1. **Penalty Rule**: Define the logic (e.g., ₹5 per day after due date).
2. **PenaltyService**:
    - Create a `PenaltyService` class in `services/penalty_service.py`.
    - Method: `calculate_penalty(loan)` — calculates fine based on due date.
    - Method: `get_total_penalty_for_member(member_id)`
3. **Track Penalties**:
    - Option 1: Store penalties in `Loan` objects and summarize.
    - Option 2: Store cumulative penalties per member in a new field or `stats.json`.
4. **CLI Integration**:
    - When returning a book, print penalty if overdue.
    - Add an admin CLI option: **View total penalties for a member**.
5. **Optional Bonus**:
    - Allow waiving penalties via CLI (`waive_penalty(member_id)`).

---

## 📌 Part 2: Refactor Into Modular Service Architecture

### 🎯 Objectives:
- Create clean, testable, reusable service files.
- Keep the `Library` class as a coordinator only.
- Prepare for plug-and-play web API use.

### ✅ Tasks:
1. **Create `services/` directory** (if not already).
2. **Move business logic into the following service files**:
    - `book_service.py` → add/search/remove books
    - `member_service.py` → register/search/update members
    - `loan_service.py` → issue/return books
    - `penalty_service.py` → overdue fine logic
    - `analytics_engine.py` → stats/analysis logic
    - `data_service.py` → import/export json
3. **Each service class**:
    - Should be initialized with a `Library` object or the relevant datasets (`books`, `loans`, etc.)
    - Handle all business logic within methods — keep them dumb, clean, and self-contained.
4. **Update your `library.py`**:
    - Initialize all services inside `Library.__init__()`.
    - Expose services as attributes (e.g., `self.book_service`).
    - Keep `Library` responsible only for coordination and shared state.
5. **Update CLI (if needed)**:
    - Refactor CLI commands to call service methods through the `Library` instance.

---

## 📌 Example Usage After Refactor

```python
library = Library()
library.loan_service.issue_book(member_id="M123", book_id="B456")
library.penalty_service.calculate_penalty(loan)
library.analytics_engine.get_top_borrowed_books(n=5)
