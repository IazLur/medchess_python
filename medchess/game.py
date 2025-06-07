import os
import signal
from typing import Optional

from .board import Board
from .rules import legal_moves
from .ai import AIPlayer

TIME_LIMIT = 30

class TimeoutException(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutException()

def timed_input(prompt: str, timeout: int) -> str:
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)
    try:
        return input(prompt)
    finally:
        signal.alarm(0)

def parse_move(text: str) -> Optional[tuple[int, int, int, int]]:
    try:
        fr, fc, tr, tc = map(int, text.strip().split())
        return fr, fc, tr, tc
    except Exception:
        return None

def play(power: int = 1, max_time: int = TIME_LIMIT) -> None:
    board = Board()
    ai = AIPlayer(os.path.join(os.path.dirname(__file__), 'model.zip'))
    current_player = 0
    while True:
        print(board.render())
        if current_player == 0:
            try:
                user_move = timed_input('Votre coup (fr fc tr tc): ', max_time)
            except TimeoutException:
                print('Temps écoulé ! Vous avez perdu.')
                return
            move = parse_move(user_move)
            if move is None or move not in legal_moves(board, current_player):
                print('Coup invalide, vous avez perdu.')
                return
            fr, fc, tr, tc = move
            target = board.get_piece(tr, tc)
            board.move_piece(move)
            if target and target.type.value == 'C':
                print('Vous avez capturé le chateau adverse. Vous gagnez !')
                return
        else:
            move = ai.choose_move(board, current_player, power=power, max_time=max_time)
            if move is None:
                print('Le bot ne peut jouer. Vous gagnez !')
                return
            fr, fc, tr, tc = move
            print(f'Bot joue: {fr} {fc} {tr} {tc}')
            target = board.get_piece(tr, tc)
            board.move_piece(move)
            if target and target.type.value == 'C':
                print('Le bot capture votre chateau. Vous perdez !')
                return
        current_player = 1 - current_player

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Play MedChess in the terminal")
    parser.add_argument("-power", type=int, default=1, help="Profondeur de recherche de l'IA (1-10)")
    parser.add_argument("-max", type=int, default=TIME_LIMIT, help="Temps de réflexion maximum en secondes")
    args = parser.parse_args()

    play(power=args.power, max_time=args.max)
