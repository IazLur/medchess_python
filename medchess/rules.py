from typing import List

from .board import Board, Move, BOARD_HEIGHT, BOARD_WIDTH
from .pieces import PieceType

# Directions for swordsman (orthogonal)
ORTHO_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# Directions for knight (diagonal one step)
DIAG_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def legal_moves(board: Board, player: int) -> List[Move]:
    moves: List[Move] = []
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            piece = board.get_piece(r, c)
            if piece is None or piece.player != player:
                continue
            if piece.type == PieceType.SWORDSMAN:
                moves.extend(_orthogonal_moves(board, r, c, 1))
            elif piece.type == PieceType.KNIGHT:
                moves.extend(_diagonal_moves(board, r, c, 1))
            elif piece.type == PieceType.GENERAL:
                moves.extend(_orthogonal_moves(board, r, c, 2))
                moves.extend(_diagonal_moves(board, r, c, 1))
            elif piece.type == PieceType.CASTLE:
                continue
    return moves

def _orthogonal_moves(board: Board, r: int, c: int, distance: int) -> List[Move]:
    moves = []
    for dr, dc in ORTHO_DIRS:
        for i in range(1, distance + 1):
            tr, tc = r + dr * i, c + dc * i
            if not board.in_bounds(tr, tc):
                break
            target = board.get_piece(tr, tc)
            if target is None:
                moves.append((r, c, tr, tc))
            elif target.player != board.get_piece(r, c).player:
                moves.append((r, c, tr, tc))
                break
            else:
                break
    return moves

def _diagonal_moves(board: Board, r: int, c: int, distance: int) -> List[Move]:
    moves = []
    for dr, dc in DIAG_DIRS:
        for i in range(1, distance + 1):
            tr, tc = r + dr * i, c + dc * i
            if not board.in_bounds(tr, tc):
                break
            target = board.get_piece(tr, tc)
            if target is None:
                moves.append((r, c, tr, tc))
            elif target.player != board.get_piece(r, c).player:
                moves.append((r, c, tr, tc))
                break
            else:
                break
    return moves
