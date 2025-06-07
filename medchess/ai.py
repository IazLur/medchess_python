import os
import random
import time
from typing import Optional, Tuple

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
    PERSONALITIES = ["Aggressive", "Equilibré", "Défensif"]
    OPENINGS = {
        "Aggressive": [(1, 3, 2, 3)],
        "Equilibré": [(0, 1, 1, 2)],
        "Défensif": [(0, 0, 1, 1)],
    }

    def __init__(self, model_path: str):
        if os.path.exists(model_path):
            self.model = DQN.load(model_path)
        else:
            train(model_path, 1000)
            self.model = DQN.load(model_path)
        self.env = MedChessEnv()
        self.personality = random.choice(self.PERSONALITIES)
        self.turn_count = 0
        print(f"Personnalité de l'IA : {self.personality}")

    def _evaluate(self, board: Board, player: int) -> float:
        values = {
            PieceType.SWORDSMAN: 1,
            PieceType.KNIGHT: 1,
            PieceType.GENERAL: 2.5,
            PieceType.CASTLE: 100,
        }
        score = 0.0
        has_castle = [False, False]
        for r in range(BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                piece = board.get_piece(r, c)
                if piece:
                    if piece.type == PieceType.CASTLE:
                        has_castle[piece.player] = True
                    val = values[piece.type]
                    if piece.type == PieceType.SWORDSMAN:
                        if piece.player == 0:
                            val += (BOARD_HEIGHT - 2 - r) * 0.1
                        else:
                            val += (r - 1) * 0.1
                    if piece.player == player:
                        score += val
                    else:
                        score -= val
        if not has_castle[player]:
            return -1000
        if not has_castle[1 - player]:
            return 1000
        return score

    def _search(
        self,
        board: Board,
        player: int,
        depth: int,
        start: float,
        max_time: Optional[int],
        maximizing: bool,
        root_player: int,
    ) -> Tuple[float, Optional[Move]]:
        if max_time is not None and time.time() - start >= max_time:
            raise TimeoutError
        if depth == 0:
            return self._evaluate(board, root_player), None
        moves = legal_moves(board, player)
        values_capture = {
            PieceType.SWORDSMAN: 1,
            PieceType.KNIGHT: 1,
            PieceType.GENERAL: 2.5,
            PieceType.CASTLE: 100,
        }
        def capture_value(mv: Move) -> float:
            fr, fc, tr, tc = mv
            target = board.get_piece(tr, tc)
            return values_capture.get(target.type, 0) if target else 0
        moves.sort(key=capture_value, reverse=True)
        if not moves:
            return self._evaluate(board, root_player), None
        best_move = None
        if maximizing:
            best_val = -float("inf")
            for mv in moves:
                nb = board.copy()
                nb.move_piece(mv)
                try:
                    val, _ = self._search(nb, 1 - player, depth - 1, start, max_time, False, root_player)
                except TimeoutError:
                    raise
                if val > best_val:
                    best_val = val
                    best_move = mv
            return best_val, best_move
        else:
            best_val = float("inf")
            for mv in moves:
                nb = board.copy()
                nb.move_piece(mv)
                try:
                    val, _ = self._search(nb, 1 - player, depth - 1, start, max_time, True, root_player)
                except TimeoutError:
                    raise
                if val < best_val:
                    best_val = val
                    best_move = mv
            return best_val, best_move

    def choose_move(
        self,
        board: Board,
        player: int,
        power: int = 1,
        max_time: Optional[int] = None,
    ) -> Optional[Move]:
        power = max(1, min(10, power))
        moves = legal_moves(board, player)

        if self.turn_count < len(self.OPENINGS[self.personality]) and len(moves) >= 5:
            opening = self.OPENINGS[self.personality][self.turn_count]
            if opening in moves:
                self.turn_count += 1
                return opening

        start = time.time()
        best_move = None
        for depth in range(1, power + 1):
            try:
                val, move = self._search(board, player, depth, start, max_time, True, player)
                best_move = move if move is not None else best_move
            except TimeoutError:
                break
        if best_move is not None:
            self.turn_count += 1
            return best_move
        if moves:
            self.turn_count += 1
            return random.choice(moves)
        return None

    def choose_move_rl(self, board: Board, player: int) -> Optional[Move]:
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
