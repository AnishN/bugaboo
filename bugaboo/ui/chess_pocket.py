from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QRect

class ChessPocketWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.piece_count_color = QColor(255, 0, 0, 255)
        self.piece_missing_opacity = 0.5

    def paintEvent(self, event):
        pass
    
    def resizeEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass