import pytest
from pawpal_system import *


def test_canary():
    assert True


# ── Priority ──────────────────────────────────────────────────────────────────

def test_priority_values_are_ordered():
    assert Priority.LOW.value < Priority.MEDIUM.value < Priority.HIGH.value

def test_priority_high_is_sortable_above_low():
    priorities = [Priority.LOW, Priority.HIGH, Priority.MEDIUM]
    result = sorted(priorities, key=lambda p: p.value, reverse=True)
    assert result[0] == Priority.HIGH

def test_priority_invalid_value_raises():
    with pytest.raises(ValueError):
        Priority("urgent")


# ── Pet ───────────────────────────────────────────────────────────────────────

def test_pet_stores_name_and_species():
    pet = Pet(1, "Tuck", "turtle")
    assert pet.name == "Tuck"
    assert pet.species == "turtle"

def test_pet_tasks_starts_empty():
    pet = Pet(1, "Tuck", "turtle")
    assert pet.tasks == []

def test_pet_register_adds_to_owner():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)
    pet.register_with_owner()
    assert pet in owner.pets

def test_pet_register_does_not_duplicate():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)
    pet.register_with_owner()
    pet.register_with_owner()
    assert owner.pets.count(pet) == 1

def test_pet_unregister_removes_from_owner():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)
    pet.register_with_owner()
    pet.unregister_from_owner()
    assert pet not in owner.pets

def test_pet_unregister_without_owner_does_nothing():
    pet = Pet(1, "Tuck", "turtle")
    pet.unregister_from_owner()  # should not raise


# ── Task ──────────────────────────────────────────────────────────────────────

def test_task_defaults_to_low_priority():
    task = Task(1, "Feed Tuck")
    assert task.priority == Priority.LOW

def test_task_defaults_duration_to_zero():
    task = Task(1, "Feed Tuck")
    assert task.duration == 0

def test_task_stores_pet_reference():
    pet = Pet(1, "Tuck", "turtle")
    task = Task(1, "Feed Tuck", pet=pet)
    assert task.pet.name == "Tuck"

def test_task_accepts_high_priority():
    task = Task(1, "Meds", priority=Priority.HIGH, duration=5)
    assert task.priority == Priority.HIGH

def test_mark_complete_changes_status():
    task = Task(1, "Feed Tuck")
    task.mark_complete()
    assert task.completed == True

def test_adding_task_to_pet_increases_count():
    pet = Pet(1, "Tuck", "turtle")
    task = Task(1, "Feed Tuck")
    pet.tasks.append(task)
    assert len(pet.tasks) == 1


# ── Owner ─────────────────────────────────────────────────────────────────────

def test_owner_starts_with_no_pets():
    owner = Owner(1, "Stuart")
    assert owner.pets == []

def test_owner_starts_with_no_tasks():
    owner = Owner(1, "Stuart")
    assert owner.tasks == []

def test_owner_add_pet():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle")
    owner.add_pet(pet)
    assert pet in owner.pets

def test_owner_add_multiple_pets():
    owner = Owner(1, "Stuart")
    tuck = Pet(1, "Tuck", "turtle")
    ming = Pet(2, "Ming-Ming", "duck")
    owner.add_pet(tuck)
    owner.add_pet(ming)
    assert len(owner.pets) == 2

def test_owner_add_task():
    owner = Owner(1, "Stuart")
    task = Task(1, "Feed Tuck")
    owner.add_task(task)
    assert task in owner.tasks


# ── Scheduler ─────────────────────────────────────────────────────────────────

def test_scheduler_starts_empty():
    s = Scheduler()
    assert s.tasks == []
    assert s._schedule == []

def test_scheduler_default_time_budget():
    s = Scheduler()
    assert s.total_minutes == 480

def test_scheduler_load_from_owner_collects_pet_tasks():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)
    task = Task(1, "Feed Tuck", pet=pet, priority=Priority.HIGH, duration=10)
    pet.tasks.append(task)
    owner.add_pet(pet)

    s = Scheduler()
    s.load_from_owner(owner)
    assert task in s.tasks

def test_scheduler_generate_orders_by_priority():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)

    low  = Task(1, "Low task",  pet=pet, priority=Priority.LOW,  duration=10)
    high = Task(2, "High task", pet=pet, priority=Priority.HIGH, duration=10)
    pet.tasks.extend([low, high])
    owner.add_pet(pet)

    s = Scheduler()
    s.load_from_owner(owner)
    s.generate_schedule()

    assert s._schedule[0].priority == Priority.HIGH

def test_scheduler_skips_tasks_that_exceed_budget():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)

    big   = Task(1, "Long task",  pet=pet, priority=Priority.HIGH, duration=300)
    small = Task(2, "Short task", pet=pet, priority=Priority.LOW,  duration=10)
    pet.tasks.extend([big, small])
    owner.add_pet(pet)

    s = Scheduler(total_minutes=15)
    s.load_from_owner(owner)
    s.generate_schedule()

    assert big not in s._schedule
    assert small in s._schedule

def test_scheduler_total_duration_never_exceeds_budget():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)
    for i in range(10):
        pet.tasks.append(Task(i, f"Task {i}", pet=pet, priority=Priority.MEDIUM, duration=60))
    owner.add_pet(pet)

    s = Scheduler(total_minutes=180)
    s.load_from_owner(owner)
    s.generate_schedule()

    total = sum(t.duration for t in s._schedule)
    assert total <= 180

def test_explain_schedule_before_generate_returns_prompt():
    s = Scheduler()
    assert "generate_schedule" in s.explain_schedule()

def test_explain_schedule_contains_task_names():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)
    task = Task(1, "Feed Tuck", pet=pet, priority=Priority.HIGH, duration=10)
    pet.tasks.append(task)
    owner.add_pet(pet)

    s = Scheduler()
    s.load_from_owner(owner)
    s.generate_schedule()

    assert "Feed Tuck" in s.explain_schedule()

def test_explain_schedule_shows_am_time():
    owner = Owner(1, "Stuart")
    pet = Pet(1, "Tuck", "turtle", owner=owner)
    task = Task(1, "Feed Tuck", pet=pet, priority=Priority.HIGH, duration=10)
    pet.tasks.append(task)
    owner.add_pet(pet)

    s = Scheduler(start_hour=8)
    s.load_from_owner(owner)
    s.generate_schedule()

    assert "AM" in s.explain_schedule()