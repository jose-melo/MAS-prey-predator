from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        # ... to be completed
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        print(cellmates)
        for neighbor in cellmates:
            if type(neighbor) == GrassPatch:
                neighbor.get_eaten()




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
        # ... to be completedpass
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        print(cellmates)


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

