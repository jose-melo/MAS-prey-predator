"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from typing import Tuple, Union
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height: int = 20,
        width: int = 20,
        initial_sheep:int = 100,
        initial_wolves:int = 50,
        sheep_reproduce:float = 0.04,
        wolf_reproduce:float = 0.05,
        wolf_gain_from_food: int = 20,
        grass:bool = False,
        grass_regrowth_time: int = 30,
        sheep_gain_from_food: int = 4,
        aging_effect:bool = False,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
            aging_effect: Whether or not to apply an aging effect to animals
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.aging_effect = aging_effect

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        self.sheep_moore = False
        self.sheep_initial_energy = sheep_gain_from_food
        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.create_sheep((x,y),self.sheep_moore,energy=1, aging_effect=aging_effect)

        self.wolf_moore = False
        self.wolf_initial_energy = wolf_gain_from_food
        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.create_wolf((x,y),self.wolf_moore,energy=1, aging_effect=aging_effect)

        # Create grass patches
        for i in range(width):
            for j in range(height):
                self.create_grass((i, j))
   
    def create_grass(self, pos: Tuple[int, int]): 
        """Create a GrassPatch in the specified position

        Args:
            pos Tuple[int, int]: (x, y) position of the grass in the Grid
        """
        (i, j) = pos
        new_grass = GrassPatch(self.next_id(), (i, j), self, True, self.grass_regrowth_time)
        self.schedule.add(new_grass)
        self.grid.place_agent(new_grass, (i, j))

    def create_sheep(self, pos: Tuple[int, int], moore: bool, energy: int, aging_effect: bool):
        new_sheep = Sheep(self.next_id(), pos, self, moore, energy, aging_effect)
        self.schedule.add(new_sheep)
        self.grid.place_agent(new_sheep, pos)

    def create_wolf(self, pos: Tuple[int, int], moore: bool, energy: int, aging_effect: bool):
        new_wolf = Wolf(self.next_id(), pos, self, moore, energy, aging_effect)
        self.schedule.add(new_wolf)
        self.grid.place_agent(new_wolf, pos)

    def kill_animal(self, animal: Union[Sheep, Wolf]) -> None:
        self.grid.remove_agent(animal)
        self.schedule.remove(animal)

    def step(self):

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed
        self.schedule.step()

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()

    def event_sheep_eats_grass(self, sheep: Sheep, grass: GrassPatch):
        if self.grass:
            grass.get_eaten()
            sheep.eat_grass(self.sheep_gain_from_food)
    
    def event_reproduces(self, animal):
        if type(animal) == Sheep:
            if self.random.random()<=self.sheep_reproduce:
                self.create_sheep(animal.pos, self.sheep_moore, self.sheep_initial_energy, self.aging_effect)
        if type(animal) == Wolf:
            if self.random.random()<=self.wolf_reproduce:
                self.create_wolf(animal.pos, self.wolf_moore, self.wolf_initial_energy, self.aging_effect)
            
    def event_wolf_eats_sheep(self, wolf: Wolf, sheep: Sheep):
        wolf.eat_sheep(self.wolf_gain_from_food)
        self.kill_animal(sheep)
    
    def verify_survivalness(self, animal: Union[Sheep, Wolf]):
        if animal.aging_effect:
            if animal.age == animal.death_age:
                self.kill_animal(animal)
        
        if animal.energy == 0:
            self.kill_animal(animal)
        animal.energy -= 1
            