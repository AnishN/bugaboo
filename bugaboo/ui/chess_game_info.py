from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QFrame

class ChessGameInfoWidget(QTableWidget):

    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame)
    
    def set_bpgn(self):
        pass