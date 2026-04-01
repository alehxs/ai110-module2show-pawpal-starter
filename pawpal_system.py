from dataclasses import dataclass, field


@dataclass
class Pet:
    id: int
    name: str
    species: str
    owner: object = None

    def addName(self, name): pass
    def addSpecies(self, species): pass
    def addOwner(self, owner): pass
    def addPet(self): pass
    def removePet(self): pass


@dataclass
class Task:
    id: int
    name: str
    pet: Pet = None
    priority: str = ""
    duration: int = 0

    def addPriority(self, priority): pass


class Owner:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.pets = []

    def addPet(self, pet): pass


class Scheduler:
    def __init__(self):
        self.tasks = []
        self.schedule = []

    def generateSchedule(self): pass
    def explainSchedule(self): pass