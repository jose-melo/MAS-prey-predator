import time
from prey_predator.model import WolfSheep
import optuna
import json
from tqdm import tqdm


GRID_SIZE = 80
MAX_STEPS = 100_000

params={'density_sheep': 0.3832472113176504, 
        'density_wolves': 0.031376098598445666, 
        'sheep_reproduce': 0.19426590364662083, 
        'wolf_reproduce': 0.09233763872015628, 
        'sheep_gain_from_food': 3, 
        'grass_regrowth_time': 12}

model_params = {
    # ... to be completed
    "width": GRID_SIZE,
    "height": GRID_SIZE,
    "grass": True,
    "density_sheep": 0.5,
    "density_wolves": 0.2,
    "sheep_reproduce": 0.04,
    "wolf_reproduce": 0.1,
    "wolf_gain_from_food": 8,
    "sheep_gain_from_food": 5,
    "grass_regrowth_time": 30
}

def objective(trial):

    model_params = {
        "width": GRID_SIZE,
        "height": GRID_SIZE,
        "grass": True, #trial.suggest_categorical("grass", [True, False]),
        "density_sheep": trial.suggest_float("density_sheep", 0.4, 0.5),
        "density_wolves": trial.suggest_float("density_wolves", 0.01, 0.06),
        "sheep_reproduce": trial.suggest_float("sheep_reproduce", 0.15, 0.35),
        "wolf_reproduce": trial.suggest_float("wolf_reproduce", 0, 0.1),
        "wolf_gain_from_food": 10, #trial.suggest_int("wolf_gain_from_food", 0, 15),
        "sheep_gain_from_food": trial.suggest_int("sheep_gain_from_food", 0, 10),
        "grass_regrowth_time": trial.suggest_int("grass_regrowth_time", 0, 15)
    }

    model = WolfSheep(**model_params)

    best = -1
    for i in tqdm(range(MAX_STEPS)):
        eval = model.eval_step()
        if eval == -1: break
        if eval > best: best = eval
    
    with open("best.txt", "a") as file:
        json.dump(model_params, file)
        file.write(f"best eval: {best} \n\n")

    return eval

if __name__ == '__main__':
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=100)
    print(study.best_trial)

