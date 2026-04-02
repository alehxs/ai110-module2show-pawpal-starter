# PawPal+ Project Reflection

## 1. System Design

### 3 Core Actions
- Add a pet
- Add task for each pet (feed, meds, etc.)
- Set priority (High, Medium, Low)

**a. Initial design**

4 classes: `Pet`, `Owner`, `Task`, and `Scheduler`.

| Class | Responsibility |
|-------|---------------|
| `Pet` | Stores name, species, and owner reference |
| `Owner` | Holds a list of pets; entry point for adding them |
| `Task` | Represents one care activity with a priority and duration; linked to a pet |
| `Scheduler` | Takes the task list and produces an ordered daily plan with explanations |

**b. Design changes**

Several changes were made after reviewing the initial design:

- `addPet()` / `removePet()` moved from `Pet` to `Owner` — a pet shouldn't manage itself
- `Owner` gained a `tasks` list and `addTask()` method to represent the missing owner→task relationship
- `Pet` gained a `tasks` list so the pet→task relationship is bidirectional
- `Task.priority` changed from a plain `str` to a `Priority` enum to prevent invalid values
- `Scheduler` gained a `total_minutes` field (default 480) so it can enforce a time budget

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
