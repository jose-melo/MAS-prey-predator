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


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    # ... to be completed
    "width": 20,
    "initial_sheep": 20,
    "initial_wolves": 50,
    "sheep_reproduce": 0.04,
    "wolf_reproduce": 0.04,
    "wolf_gain_from_food": 15,
    "grass": True,
    "grass_regrowth_time": 30,
    "sheep_gain_from_food": 5,
    "aging_effect": True
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
