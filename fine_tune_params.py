import time
from prey_predator.model import WolfSheep
import optuna
import json
from tqdm import tqdm


GRID_SIZE = 20
MAX_STEPS = 10_000

def objective(trial):

    model_params = {
        "width": GRID_SIZE,
        "height": GRID_SIZE,
        "grass": True, 
        "moore": trial.suggest_categorical("moore", [True, False]),
        "aging_effect": trial.suggest_categorical("aging_effect", [True, False]),
        "density_sheep": trial.suggest_float("density_sheep", 0.4, 0.5),
        "density_wolves": trial.suggest_float("density_wolves", 0.4, 0.5),
        "sheep_reproduce": trial.suggest_float("sheep_reproduce", 0.15, 0.35),
        "wolf_reproduce": trial.suggest_float("wolf_reproduce", 0, 0.1),
        "wolf_gain_from_food": trial.suggest_int("wolf_gain_from_food", 0, 15),
        "sheep_gain_from_food": trial.suggest_int("sheep_gain_from_food", 0, 10),
        "grass_regrowth_time": trial.suggest_int("grass_regrowth_time", 0, 15),
        "death_age_wolf": trial.suggest_int("death_age_wolf", 0, 15),
        "death_age_sheep": trial.suggest_int("death_age_sheep", 0, 15),
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

