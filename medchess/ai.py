import os
import random
from typing import Optional

import gym
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.dqn import MlpPolicy

from .board import Board, Move, BOARD_HEIGHT, BOARD_WIDTH
from .rules import legal_moves
from .pieces import PieceType

class MedChessEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        super().__init__()
        self.board = Board()
        self.current_player = 0
        self.action_space = gym.spaces.Discrete(BOARD_WIDTH * BOARD_HEIGHT * BOARD_WIDTH * BOARD_HEIGHT)
        self.observation_space = gym.spaces.Box(low=0, high=8, shape=(BOARD_HEIGHT, BOARD_WIDTH), dtype=np.int8)
        self.done = False

    def reset(self):
        self.board.reset()
        self.current_player = 0
        self.done = False
        return self._get_obs()

    def _get_obs(self):
        arr = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=np.int8)
        for r in range(BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                piece = self.board.get_piece(r, c)
                if piece:
                    code = {
                        PieceType.SWORDSMAN: 1,
                        PieceType.KNIGHT: 2,
                        PieceType.GENERAL: 3,
                        PieceType.CASTLE: 4,
                    }[piece.type]
                    arr[r, c] = code if piece.player == 0 else code + 4
        return arr

    def step(self, action: int):
        if self.done:
            return self._get_obs(), 0.0, True, {}
        move = self._decode_action(action)
        if move not in legal_moves(self.board, self.current_player):
            self.done = True
            return self._get_obs(), -1.0, True, {}
        fr, fc, tr, tc = move
        target = self.board.get_piece(tr, tc)
        self.board.move_piece(move)
        reward = 0.0
        if target and target.type == PieceType.CASTLE:
            self.done = True
            reward = 1.0
        self.current_player = 1 - self.current_player
        return self._get_obs(), reward, self.done, {}

    def render(self, mode='human'):
        print(self.board.render())

    def _decode_action(self, action: int) -> Move:
        fr = action // (BOARD_WIDTH * BOARD_WIDTH * BOARD_HEIGHT)
        action %= BOARD_WIDTH * BOARD_WIDTH * BOARD_HEIGHT
        fc = action // (BOARD_WIDTH * BOARD_HEIGHT)
        action %= BOARD_WIDTH * BOARD_HEIGHT
        tr = action // BOARD_WIDTH
        tc = action % BOARD_WIDTH
        return fr, fc, tr, tc


def train(path: str, timesteps: int = 10000) -> None:
    env = MedChessEnv()
    model = DQN(MlpPolicy, env, verbose=0)
    model.learn(total_timesteps=timesteps)
    model.save(path)

class AIPlayer:
    def __init__(self, model_path: str):
        if os.path.exists(model_path):
            self.model = DQN.load(model_path)
        else:
            train(model_path, 1000)
            self.model = DQN.load(model_path)
        self.env = MedChessEnv()

    def choose_move(self, board: Board, player: int) -> Optional[Move]:
        self.env.board = board.copy()
        self.env.current_player = player
        state = self.env._get_obs()
        action, _ = self.model.predict(state, deterministic=True)
        move = self.env._decode_action(int(action))
        if move in legal_moves(board, player):
            return move
        # If the predicted move is illegal, fall back to a random legal move
        moves = legal_moves(board, player)
        if moves:
            return random.choice(moves)
        return None
