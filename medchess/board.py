from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from .pieces import Piece, PieceType

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

Move = Tuple[int, int, int, int]  # from_row, from_col, to_row, to_col

@dataclass
class Cell:
    piece: Optional[Piece] = None

class Board:
    def __init__(self) -> None:
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)
        ]
        self.reset()

    def reset(self) -> None:
        # Clear board
        for row in self.grid:
            for cell in row:
                cell.piece = None
        # Setup initial pieces
        setup = [
            Piece(PieceType.SWORDSMAN, 0),
            Piece(PieceType.SWORDSMAN, 0),
            Piece(PieceType.GENERAL, 0),
            Piece(PieceType.CASTLE, 0),
            Piece(PieceType.GENERAL, 0),
            Piece(PieceType.SWORDSMAN, 0),
            Piece(PieceType.SWORDSMAN, 0),
        ]
        for c, piece in enumerate(setup):
            self.grid[0][c].piece = piece
            self.grid[BOARD_HEIGHT - 1][c].piece = Piece(piece.type, 1)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < BOARD_HEIGHT and 0 <= c < BOARD_WIDTH

    def get_piece(self, r: int, c: int) -> Optional[Piece]:
        return self.grid[r][c].piece if self.in_bounds(r, c) else None

    def move_piece(self, move: Move) -> bool:
        fr, fc, tr, tc = move
        if not (self.in_bounds(fr, fc) and self.in_bounds(tr, tc)):
            return False
        piece = self.get_piece(fr, fc)
        if not piece:
            return False
        target = self.get_piece(tr, tc)
        if target and target.player == piece.player:
            return False
        self.grid[tr][tc].piece = piece
        self.grid[fr][fc].piece = None
        return True

    def copy(self) -> "Board":
        b = Board()
        for r in range(BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                piece = self.get_piece(r, c)
                if piece:
                    b.grid[r][c].piece = Piece(piece.type, piece.player)
                else:
                    b.grid[r][c].piece = None
        return b

    def render(self) -> str:
        rows = []
        for r in range(BOARD_HEIGHT):
            row = []
            for c in range(BOARD_WIDTH):
                piece = self.get_piece(r, c)
                row.append(piece.__repr__() if piece else "..")
            rows.append(" ".join(row))
        return "\n".join(rows)
