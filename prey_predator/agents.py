from typing import Tuple
from mesa import Agent
from prey_predator.model import WolfSheep
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id: int, pos: Tuple[int, int], model: WolfSheep, moore: bool, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def eat_grass(self, energy_from_food) -> None:
        """
            Sheep eats the grass and gain energy from it
        """
        self.energy += energy_from_food

    def step(self) -> None:
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for neighbor in cellmates:
            if type(neighbor) == GrassPatch and neighbor.fully_grown:
                self.model.event_sheep_eats_grass(self, neighbor)
     
        self.model.event_reproduces(self)
            
class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # reproduce :
        self.model.event_reproduces()

        # eat :
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, Sheep):
                self.energy+=self.model.wolf_gain_from_food
                self.model.kill_animal(mate)

class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id: int, pos: Tuple[int, int], model: WolfSheep, fully_grown: bool, countdown: int):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown 
        self.age = 0
        self.time_to_grow = countdown
        self.pos = pos
    
    def get_eaten(self):
        self.age = 0
        self.fully_grown=False

    def step(self):
        self.age += 1
        if self.age >= self.countdown:
            self.fully_grown=True
            

