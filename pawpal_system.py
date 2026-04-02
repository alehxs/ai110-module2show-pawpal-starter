from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Pet:
    id: int
    name: str
    species: str
    owner: "Owner" = None
    tasks: list = field(default_factory=list)

    def register_with_owner(self):
        """Add this pet to its owner's pet list if not already present."""
        if self.owner and self not in self.owner.pets:
            self.owner.pets.append(self)

    def unregister_from_owner(self):
        """Remove this pet from its owner's pet list if present."""
        if self.owner and self in self.owner.pets:
            self.owner.pets.remove(self)


@dataclass
class Task:
    id: int
    name: str
    pet: Pet = None
    priority: Priority = Priority.LOW
    duration: int = 0
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


class Owner:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def add_task(self, task: Task):
        """Add a task to this owner's task list."""
        self.tasks.append(task)


class Scheduler:

    def __init__(self, total_minutes: int = 480, start_hour: int = 8):
        self.tasks: list[Task] = []
        self.total_minutes = total_minutes
        self.start_hour = start_hour
        self._schedule: list[Task] = []

    def load_from_owner(self, owner: Owner):
        """Collect all tasks from each of the owner's pets."""
        for pet in owner.pets:
            self.tasks.extend(pet.tasks)

    def generate_schedule(self) -> list[Task]:
        """Sort tasks by priority and greedily fit them within the time budget."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority.value, reverse=True)

        remaining = self.total_minutes
        self._schedule = []

        for task in sorted_tasks:
            if task.duration <= remaining:
                self._schedule.append(task)
                remaining -= task.duration

        return self._schedule

    def explain_schedule(self) -> str:
        """Return a human-readable summary of the scheduled tasks with start times."""
        if not self._schedule:
            return "No schedule generated. Call generate_schedule() first."

        elapsed = 0
        lines = []

        for task in self._schedule:
            pet_name = task.pet.name if task.pet else "unknown"
            start_hour, start_min = divmod(self.start_hour * 60 + elapsed, 60)
            time_str = f"{start_hour % 12 or 12}:{start_min:02d} {'AM' if start_hour < 12 else 'PM'}"
            lines.append(
                f"- {time_str}  {task.name} ({pet_name})"
                f"  [{task.duration} min, {task.priority.name}]"
            )
            elapsed += task.duration

        return "\n".join(lines)