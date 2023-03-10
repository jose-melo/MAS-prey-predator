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
from scipy.signal import find_peaks 


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
        density_sheep:float = 0.5,
        density_wolves:float = 0.5,
        sheep_reproduce:float = 0.04,
        wolf_reproduce:float = 0.05,
        wolf_gain_from_food: int = 20,
        grass:bool = False,
        grass_regrowth_time: int = 30,
        sheep_gain_from_food: int = 4,
        aging_effect:bool = False,
        death_age_wolf:int = 15,
        death_age_sheep:int = 15,
        sheep_energy_decay: float = 1,
        wolf_energy_decay: float = 1,
        moore: bool = False,
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
        self.initial_sheep = int(width * height * density_sheep)
        self.initial_wolves = int(width * height * density_wolves)
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.aging_effect = aging_effect
        self.moore = moore

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            model_reporters=
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            },
            tables={
                "Count": ["Wolves", "Sheep"],
            }
        )

        self.sheep_initial_energy = sheep_gain_from_food
        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.create_sheep(pos = (x,y),
                              moore = self.moore,
                              energy = 1, 
                              aging_effect = aging_effect,
                              death_age = death_age_sheep,
                              energy_decay=sheep_energy_decay
                              )

        self.wolf_initial_energy = wolf_gain_from_food
        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.create_wolf(pos = (x,y),
                             moore = self.moore,
                             energy=1, 
                             aging_effect=aging_effect,  
                             death_age=death_age_wolf,
                             energy_decay=wolf_energy_decay )

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

    def create_sheep(self, pos: Tuple[int, int], moore: bool, energy: int, aging_effect: bool, death_age: int, energy_decay: float):
        new_sheep = Sheep(self.next_id(), pos, self, moore, energy, aging_effect, death_age, energy_decay_rate=energy_decay)
        self.schedule.add(new_sheep)
        self.grid.place_agent(new_sheep, pos)

    def create_wolf(self, pos: Tuple[int, int], moore: bool, energy: int, aging_effect: bool, death_age: int, energy_decay: float):
        new_wolf = Wolf(self.next_id(), pos, self, moore, energy, aging_effect, death_age, energy_decay_rate=energy_decay)
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
    
    def eval_step(self) -> int:
        self.step()

        df = self.datacollector.get_model_vars_dataframe()
        #print(df["Wolves"].iloc[-1], df["Sheep"].iloc[-1])

        #if df["Wolves"].iloc[-1]/df["Sheep"].iloc[-1] >= 1000 or df["Sheep"].iloc[-1]/df["Wolves"].iloc[-1] >= 1000 :
            #return -1

        if df['Wolves'].iloc[-1] == 0 or df["Sheep"].iloc[-1] == 0:
            return -1
        
        num_maxima_sheep = find_peaks(df['Sheep'][-100:])[0].shape[0]
        num_maxima_wolf = find_peaks(df['Sheep'][-100:])[0].shape[0]
    
        return num_maxima_wolf  + num_maxima_sheep
        

    def run_model(self, step_count=200) -> None:
        for _ in range(step_count):
            self.step()

    def event_sheep_eats_grass(self, sheep: Sheep, grass: GrassPatch) -> None:
        if self.grass:
            grass.get_eaten()
            sheep.eat_grass(self.sheep_gain_from_food)
        else:
            sheep.eat_grass(1)
    
    def event_reproduces(self, animal: Union[Sheep, Wolf]) -> None:
        # Here we try to "conserve" the energy
        # Otherwise sheeps could live forever given sufficient reproduction rate

        child_energy = animal.energy//2

        if isinstance(animal, Sheep):
            if self.random.random()<=self.sheep_reproduce:
                self.create_sheep(pos = animal.pos,
                                  moore = self.moore,
                                  energy = child_energy,
                                  aging_effect = self.aging_effect,
                                  death_age = animal.death_age,
                                  energy_decay=animal.energy_decay_rate)

        if isinstance(animal, Wolf):
            if self.random.random()<=self.wolf_reproduce:
                self.create_wolf(pos = animal.pos,
                                 moore = self.moore,
                                 energy = child_energy,
                                 aging_effect = self.aging_effect,
                                 death_age = animal.death_age,
                                 energy_decay=animal.energy_decay_rate)

    def event_wolf_eats_sheep(self, wolf: Wolf, sheep: Sheep) -> None:
        """Wolf eats sheep and gets energy from it"""
        wolf.eat_sheep(self.wolf_gain_from_food)
        self.kill_animal(sheep)
    
    def verify_survivalness(self, animal: Union[Sheep, Wolf], energy_decay_rate: float = 1) -> None:
        """ Verify if animal is still alive

        Args:
            animal (Union[Sheep, Wolf]): Animal to verify 
            energy_decay_rate (float, optional). Defaults to 1.
        """
        if animal.energy == 0:
            self.kill_animal(animal)
            return

        if animal.aging_effect:
            animal.age += 1
            if animal.age == animal.death_age:
                self.kill_animal(animal)
                return 
        
        animal.energy -= energy_decay_rate
            