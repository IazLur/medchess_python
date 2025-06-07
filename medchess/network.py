import socket
from typing import Tuple

def host_game(port: int) -> socket.socket:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("", port))
    srv.listen(1)
    conn, _ = srv.accept()
    srv.close()
    return conn

def join_game(ip: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock

def send_move(sock: socket.socket, move: Tuple[int, int, int, int]) -> None:
    msg = f"{move[0]} {move[1]} {move[2]} {move[3]}\n"
    sock.sendall(msg.encode())

