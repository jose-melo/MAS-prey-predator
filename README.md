# 🐺🐑 Proies et Prédateurs

###  Participants 👥

Ce projet a été réalisé avec passion et dévouement par José Lucas de Melo Costa et Eliott Barbot. 👨‍💻👨‍💻

## Description 📝

Plongez dans l'univers passionnant de Proies et Prédateurs ! Ce projet est une simulation de populations de loups et de moutons qui interagissent dans un même environnement. 🌳 Les agents se déplacent, mangent, se reproduisent et ont des besoins vitaux tels que l'énergie pour survivre. Le modèle de simulation est conçu comme un système multi-agents, avec deux types d'agents : les agents Herbe et les animaux. Les agents Herbe ont des attributs simples tels que le temps de croissance et l'âge, et leur principale fonction est de pousser jusqu'à ce qu'ils soient prêts à être mangés par les animaux. Les animaux ont des attributs supplémentaires tels que leur âge et leur énergie. 🦌🐑🌿

Ce référentiel a la structure de fichier suivante

```
├── df_params.parquet
├── fine_tune_params.py
├── plot_curves.ipynb
├── prey_predator
│   ├── agents.py
│   ├──  __init__.py
│   ├──  model.py
│   ├── random_walk.py
│   ├── schedule.py
│   └──  server.py
├── README.md
├── requirements.txt
└── run.py


```

## Installation 🚀

Vous voulez découvrir Proies et Prédateurs ? Suivez les étapes ci-dessous pour l'installer et l'exécuter :
- Clonez ce dépôt de code en utilisant la commande git clone https://github.com/jose-melo/MAS-prey-predator.git.
- Installez les dépendances en utilisant la commande `pip install -r requirements.txt ` 
- Exécutez le `mesa runserver` ou les notebooks 📓

## Utilisation 🕹️

Une fois le programme lancé, vous pouvez ajuster les paramètres de la simulation en modifiant les valeurs dans le fichier ou dans la page web. 🔧💻 N'hésitez pas à jouer avec les paramètres pour voir comment les populations de loups et de moutons évoluent dans leur environnement ! 🌍
