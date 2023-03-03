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

    @classmethod
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
        # ... to be completed
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        print(cellmates)
        for neighbor in cellmates:
            if type(neighbor) == GrassPatch and neighbor.state == GrassData.FullyGrown:
                neighbor.get_eaten()
                self.eat_grass()
    
    @classmethod
    def reproduce(self, sheep_reproduce) -> None: 
        if self.random.choices([0, 1], weights=[1-self.sheep_reproduce, self.sheep_reproduce], k=1):
            pass
            




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
        if self.model.random.random()>self.model.wolf_reproduce:
            self.model.create_new_wolf()
        # eat :
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, Sheep):
                self.energy+=self.model.wolf_gain_from_food
                #TODO : supprimer le mouton


class GrassData:
    Growing: int = 0
    FullyGrown: int = 1

    MaxAge: int = 3

class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        # ... to be completed
        self.state = GrassData.FullyGrown 
        self.age = 0
    
    def get_eaten(self):
        self.state = GrassData.Growing
        self.age = 0

    def step(self):
        # ... to be completed
        if self.state == GrassData.Growing:
            if self.age == GrassData.MaxAge:
                self.age = 0
                self.state = GrassData.FullyGrown
            else:
                self.age += 1

