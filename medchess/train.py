import argparse
import os
import time

from stable_baselines3 import DQN
from stable_baselines3.dqn import MlpPolicy

from .ai import MedChessEnv


def train_model(max_seconds: int) -> None:
    env = MedChessEnv()
    model_path = os.path.join(os.path.dirname(__file__), "model.zip")
    if os.path.exists(model_path):
        model = DQN.load(model_path, env=env)
    else:
        model = DQN(MlpPolicy, env, verbose=0)
    start = time.time()
    while True:
        model.learn(total_timesteps=1000, reset_num_timesteps=False)
        if time.time() - start >= max_seconds:
            break
    model.save(model_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Entraîne le modèle MedChess")
    parser.add_argument(
        "-max",
        type=int,
        default=30,
        help="Durée maximale d'entraînement en secondes",
    )
    args = parser.parse_args()
    train_model(args.max)


if __name__ == "__main__":
    main()
