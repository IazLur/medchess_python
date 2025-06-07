from enum import Enum

class PieceType(Enum):
    SWORDSMAN = "S"
    KNIGHT = "N"
    GENERAL = "G"
    CASTLE = "C"

class Piece:
    def __init__(self, piece_type: PieceType, player: int):
        self.type = piece_type
        self.player = player  # 0 or 1

    def __repr__(self):
        return f"{self.type.value}{self.player}"
