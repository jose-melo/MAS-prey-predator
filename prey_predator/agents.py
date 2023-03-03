from typing import Tuple
from mesa import Agent, Model
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None
    death_age = 15

    def __init__(self, unique_id: int, pos: Tuple[int, int], model: Model, moore: bool, energy=None, aging_effect=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0
        self.aging_effect = aging_effect


    def eat_grass(self, energy_from_food) -> None:
        """
            Sheep eats the grass and gain energy from it
        """
        self.energy += energy_from_food

    def step(self) -> None:
        """
        A model step. Move, then eat grass and reproduce.
        """
        # move : 
        self.random_move()
        
        # eat :
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for neighbor in cellmates:
            if type(neighbor) == GrassPatch and neighbor.fully_grown:
                self.model.event_sheep_eats_grass(self, neighbor)
     
        # reproduces :
        self.model.event_reproduces(self)

        # Check energy, if zero --> die
        self.model.verify_survivalness(self)

            
class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None
    death_age = 15

    def __init__(self, unique_id: int, pos: Tuple[int, int], model: Model, moore: bool, energy:bool = None, aging_effect:bool = False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.aging_effect = aging_effect
        self.age = 0

    def eat_sheep(self, energy_from_sheep: int): 
        """Wolf eats a sheep and gain energy from it

        Args:
            energy_from_sheep (int): amount of energy of each sheep
        """
        self.energy += energy_from_sheep

    def step(self):
        # move :
        self.random_move()

        # reproduce :
        self.model.event_reproduces(self)

        # eat :
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            # TODO: Decide if we eat all sheeps or just some of them
            # For me it doesn't make sense to eat all sheeps in the square
            if isinstance(mate, Sheep):
                self.model.event_wolf_eats_sheep(self, mate)
    
        # Check energy, if zero --> die
        self.model.verify_survivalness(self)

class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id: int, pos: Tuple[int, int], model: Model, fully_grown: bool, countdown: int):
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
        self.countdown = countdown
    
    def get_eaten(self):
        # reset variables
        self.age = 0
        self.fully_grown = False

    def step(self):
        # age
        if not self.fully_grown: 
            self.age += 1

        # Check if is fully grown
        if self.age >= self.countdown:
            self.fully_grown=True
            

