from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QFrame

class ChessMoveListWidget(QTextEdit):

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFrameStyle(QFrame.NoFrame)
        self.setAlignment(Qt.AlignJustify)
    
    def set_bpgn(self, bpgn):
        move_data = zip(bpgn.move_numbers, bpgn.moves)
        move_str = b""
        moves = []
        moves_str = b""
        for move in move_data:
            move_str = b" ".join(move)
            moves.append(move_str)
        moves_str = b" ".join(moves)
        self.append(moves_str.decode())