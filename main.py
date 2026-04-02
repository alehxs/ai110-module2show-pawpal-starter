from pawpal_system import *

# ── Owner ────────────────────────────────────────────────────────────────────
stuart = Owner(1, "Stuart")

# ── Pets ─────────────────────────────────────────────────────────────────────
tuck     = Pet(1, "Tuck",     "turtle", owner=stuart)
ming_ming = Pet(2, "Ming-Ming", "duck", owner=stuart)

# ── Tasks ─────────────────────────────────────────────────────────────────────
task1 = Task(1, "Feed Tuck",      pet=tuck,      priority=Priority.HIGH,   duration=10)
task2 = Task(2, "Feed Ming-Ming", pet=ming_ming, priority=Priority.HIGH,   duration=10)
task3 = Task(3, "Clean tank",     pet=tuck,      priority=Priority.MEDIUM, duration=30)

# ── Wire up relationships ─────────────────────────────────────────────────────
tuck.tasks.extend([task1, task3])
ming_ming.tasks.append(task2)

stuart.add_pet(tuck)
stuart.add_pet(ming_ming)

# ── Generate schedule ─────────────────────────────────────────────────────────
scheduler = Scheduler()
scheduler.load_from_owner(stuart)
scheduler.generate_schedule()

# ── Output ────────────────────────────────────────────────────────────────────
print()
print("╔══════════════════════════════════════╗")
print("║       🐾  PawPal+ Daily Planner      ║")
print("╚══════════════════════════════════════╝")
print(f"  Owner : {stuart.name}")
print(f"  Pets  : {', '.join(p.name for p in stuart.pets)}")
print()
print("─" * 40)
print(scheduler.explain_schedule())
print("─" * 40)