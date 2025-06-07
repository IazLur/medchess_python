# GUI for MedChess
import os
import tkinter as tk
from tkinter import messagebox

from .board import Board, BOARD_WIDTH, BOARD_HEIGHT
from .rules import legal_moves
from .ai import AIPlayer

CELL_SIZE = 60

class GameGUI(tk.Tk):
    def __init__(self, power: int = 1, max_time: int = 30) -> None:
        super().__init__()
        self.title("MedChess")
        self.resizable(False, False)

        self.board = Board()
        model_path = os.path.join(os.path.dirname(__file__), 'model.zip')
        self.ai = AIPlayer(model_path)
        self.power = power
        self.max_time = max_time
        self.current_player = 0
        self.selected = None

        canvas_width = BOARD_WIDTH * CELL_SIZE
        canvas_height = BOARD_HEIGHT * CELL_SIZE
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    def draw_board(self) -> None:
        self.canvas.delete("all")
        for r in range(BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                fill = "#EEE" if (r + c) % 2 else "#AAA"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
                piece = self.board.get_piece(r, c)
                if piece:
                    color = "black" if piece.player == 0 else "red"
                    self.canvas.create_text(
                        x1 + CELL_SIZE / 2,
                        y1 + CELL_SIZE / 2,
                        text=piece.type.value,
                        fill=color,
                        font=("Arial", int(CELL_SIZE / 2)),
                    )
        if self.selected:
            r, c = self.selected
            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=3)

    def on_click(self, event) -> None:
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if not self.board.in_bounds(r, c):
            return
        if self.current_player == 0:
            if self.selected is None:
                piece = self.board.get_piece(r, c)
                if piece and piece.player == 0:
                    self.selected = (r, c)
            else:
                fr, fc = self.selected
                move = (fr, fc, r, c)
                if move in legal_moves(self.board, 0):
                    target = self.board.get_piece(r, c)
                    self.board.move_piece(move)
                    self.selected = None
                    if target and target.type.value == 'C':
                        messagebox.showinfo("Victoire", "Vous avez capturé le chateau adverse.")
                        self.destroy()
                        return
                    self.current_player = 1
                    self.draw_board()
                    self.after(500, self.ai_move)
                    return
                else:
                    self.selected = None
        self.draw_board()

    def ai_move(self) -> None:
        move = self.ai.choose_move(self.board, 1, power=self.power, max_time=self.max_time)
        if move is None:
            messagebox.showinfo("Victoire", "Le bot ne peut jouer. Vous gagnez !")
            self.destroy()
            return
        fr, fc, tr, tc = move
        target = self.board.get_piece(tr, tc)
        self.board.move_piece(move)
        if target and target.type.value == 'C':
            messagebox.showinfo("Défaite", "Le bot capture votre chateau.")
            self.destroy()
            return
        self.current_player = 0
        self.draw_board()


def play_gui(power: int = 1, max_time: int = 30) -> None:
    app = GameGUI(power=power, max_time=max_time)
    app.mainloop()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Interface graphique de MedChess")
    parser.add_argument("-power", type=int, default=1, help="Profondeur de recherche de l'IA (1-10)")
    parser.add_argument("-max", type=int, default=30, help="Temps de réflexion maximum en secondes")
    args = parser.parse_args()

    play_gui(power=args.power, max_time=args.max)

