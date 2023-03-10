from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return
    
    if agent.pos is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        # ... to be completed
        portrayal = {
                "Shape": "circle",
                "Color": "blue",
                "Filled": "true",
                "Layer": 1,
                "r": 0.5}

    elif type(agent) is Wolf:
        # ... to be completed
        portrayal = {"Shape": "circle",
                "Color": "red",
                "Filled": "true",
                "Layer": 1,
                "r": 0.7}

    elif type(agent) is GrassPatch:
        # ... to be completed
        if agent.fully_grown:
            portrayal = {"Shape": "rect",
                    "Color": "green",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1 }
        else:
            portrayal = {"Shape": "rect",
                    "Color": "gray",
                    "Filled": "false",
                    "Layer": 0,
                    "w": 1,
                    "h": 1 }

    return portrayal


GRID_SIZE = 20

canvas_element = CanvasGrid(wolf_sheep_portrayal, GRID_SIZE, GRID_SIZE , 50*GRID_SIZE, 50*GRID_SIZE)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    # ... to be completed
    "width": GRID_SIZE,
    "height": GRID_SIZE,
    "grass": UserSettableParameter("checkbox", "Grass", True),
    "density_sheep": UserSettableParameter("slider", "Initial sheep density", 0.5, 0, 1, 0.01),
    "density_wolves": UserSettableParameter("slider", "Initial wolf density", 0.5, 0, 1, 0.01),
    "sheep_reproduce": UserSettableParameter("slider", "Sheep reproduction", 0.04, 0.01, 1, 0.01),
    "wolf_reproduce":  UserSettableParameter("slider", "Wolf reproduction", 0.10, 0.01, 1, 0.01),
    "wolf_gain_from_food":  UserSettableParameter("slider", "Wolf gain from food", 8, 0, 100, 1),
    "sheep_gain_from_food": UserSettableParameter("slider", "Sheep gain from food", 5, 0, 100, 1),
    "grass_regrowth_time": UserSettableParameter("slider", "Grass regrowth time", 30, 0, 100, 1),
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
