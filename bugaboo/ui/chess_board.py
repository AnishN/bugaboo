import math
import chess
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QRect, QRectF, QPointF

class ChessBoardWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        #NOTE: assume num_ranks and num_files are hard-coded to both equal 8
        self.num_ranks = 8
        self.num_files = 8
        self.color_names = {
            chess.WHITE: "white", 
            chess.BLACK: "black",
        }
        self.piece_names = {
            chess.KING: "king",
            chess.QUEEN: "queen", 
            chess.ROOK: "rook", 
            chess.BISHOP: "bishop", 
            chess.KNIGHT: "knight", 
            chess.PAWN: "pawn",
        }

        #NOTE: do NOT modify these properties directly, as repaint is not called
        self.move_color = QColor(255, 255, 0, 128)
        self.premove_color = QColor(255, 0, 255, 128)
        self.square_black = QColor(130, 162, 205, 255)
        self.square_white = QColor(228, 244, 255, 255)
        self.flip_board = False
        self.set_position(chess.Board())
        
        self.painter = QPainter()
        self.update_piece_icons("./bugaboo/resources/sets/cburnett")

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.draw_board()
        self.draw_pieces()
        self.painter.end()
    
    def resizeEvent(self, event):
        self.update_board_size()
        self.update_piece_icon_pixmaps()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        clicked_board = self.is_point_in_board(x, y)
        if clicked_board:
            square = self.point_to_square(x, y)
            print("press", chess.SQUARE_NAMES[square])
    
    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        clicked_board = self.is_point_in_board(x, y)
        if clicked_board:
            square = self.point_to_square(x, y)
            print("release", chess.SQUARE_NAMES[square])

    def point_to_square(self, x, y):
        #Assumes point is contained within board
        if not self.flip_board:
            f = (x - self.board_rect.left()) // self.square_size
            r = (self.board_rect.bottom() - y) // self.square_size
        else:
            f = (self.board_rect.right() - x) // self.square_size
            r = (y - self.board_rect.top()) // self.square_size
        square = chess.square(int(f), int(r))
        return square
    
    def is_point_in_board(self, x, y):
        if self.board_rect.left() <= x <= self.board_rect.right():
            if self.board_rect.top() <= y <= self.board_rect.bottom():
                return True
        return False
    
    def update_piece_icons(self, icon_base_dir_path):
        base_path = "{0}/{1}/{2}.svg"
        self.piece_icons = {}
        for color in self.color_names:
            self.piece_icons[color] = {}
            for piece in self.piece_names:
                color_name = self.color_names[color]
                piece_name = self.piece_names[piece]
                path = base_path.format(icon_base_dir_path, color_name, piece_name)
                icon = QIcon(path)
                self.piece_icons[color][piece] = icon

    def update_piece_icon_pixmaps(self):
        self.piece_icon_pixmaps = {}
        for color in self.color_names:
            self.piece_icon_pixmaps[color] = {}
            for piece in self.piece_names:
                icon = self.piece_icons[color][piece]
                pixmap = icon.pixmap(self.square_size, self.square_size)
                self.piece_icon_pixmaps[color][piece] = pixmap

    def update_board_size(self):
        aspect_ratio = self.num_files / self.num_ranks
        w = self.width()
        h = self.height()
        min_size = min(w, h)
        w_size = min_size * aspect_ratio
        h_size = min_size
        x = (w / 2.0) - (w_size / 2.0)
        y = (h / 2.0) - (h_size / 2.0)
        self.board_rect = QRectF(x, y, w_size, h_size)
        self.square_size = self.board_rect.width() / self.num_files
    
    def draw_board(self):
        square_color = self.square_black
        for i in range(self.num_files):
            for j in range(self.num_ranks):
                square = chess.square(i, j)
                rect = self.get_square_rect(square)
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    square_color = self.square_black if not self.flip_board else self.square_white
                else:
                    square_color = self.square_white if not self.flip_board else self.square_black
                self.painter.fillRect(rect, square_color)
    
    def get_square_rect(self, square):
        square_rank = square // self.num_ranks
        square_file = square % self.num_files
        if not self.flip_board:
            rect = QRectF(
                self.board_rect.x() + (square_file * self.square_size),
                self.board_rect.bottom() - ((square_rank + 1) * self.square_size), 
                self.square_size,
                self.square_size,
            )
        else:
            rect = QRectF(
                self.board_rect.x() + (square_file * self.square_size),
                self.board_rect.top() + (square_rank * self.square_size), 
                self.square_size,
                self.square_size,
            )
        return rect
    
    def draw_pieces(self):
        piece_map = self.position.piece_map()
        for square, piece in piece_map.items():
            piece_color = piece.color
            piece_type = piece.piece_type
            self.draw_piece(piece_color, piece_type, square)

    def draw_piece(self, color, piece_type, square):
        piece_pixmap = self.piece_icon_pixmaps[color][piece_type]
        piece_rect = self.get_square_rect(square).toRect()
        self.painter.drawPixmap(piece_rect, piece_pixmap)

    def set_flip_board(self, flip_board):
        self.flip_board = flip_board
        self.repaint()

    def set_position(self, position):
        self.position = position
        self.repaint()

    #def set_move(self, move):

    def draw_highlight(self, color, square):
        rect = self.get_square_rect(square)
        self.painter.fillRect(rect, color)
    
    def draw_circle(self, color, square):
        outer_radius_fraction = 0.8
        inner_radius_fraction = 0.55
        rect = self.get_square_rect(square)
        center = rect.center()
        max_radius = rect.width() / 2.0
        outer_radius = max_radius * outer_radius_fraction
        inner_radius = max_radius * inner_radius_fraction
        path = QPainterPath()
        path.addEllipse(center, outer_radius, outer_radius)
        path.addEllipse(center, inner_radius, inner_radius)
        self.painter.fillPath(path, color)

    def draw_cross(self, color, square):
        cross_width_fraction = 0.15

        rect = self.get_square_rect(square)
        center = rect.center()
        h_rect = rect
        h_rect.setHeight(rect.height() * cross_width_fraction)
        h_rect.moveCenter(center)

        rect = self.get_square_rect(square)#copy
        v_rect = rect
        v_rect.setWidth(rect.width() * cross_width_fraction)
        v_rect.moveCenter(center)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRect(h_rect)
        path.addRect(v_rect)
        self.painter.translate(rect.center())
        self.painter.rotate(45)
        self.painter.translate(-rect.center())
        self.painter.fillPath(path, color)
        self.painter.resetTransform()
    
    def draw_arrow(self, color, start_square, end_square):
        arrow_width_fraction = 0.15
        start_rect = self.get_square_rect(start_square)
        end_rect = self.get_square_rect(end_square)
        start_pt = start_rect.center()
        end_pt = end_rect.center()
        
        #determine arrow stem dimensions
        dx = end_pt.x() - start_pt.x()
        dy = end_pt.y() - start_pt.y()
        arrow_length = math.sqrt((dx * dx) + (dy * dy))
        arrow_width = arrow_width_fraction * self.square_size
        arrow_angle = math.degrees(math.atan2(dy, dx))

        #determine arrow tip dimensions
        #3.0 and 6.0 are (BAD!) magic numbers in relation to self.square_size
        tip_length = self.square_size / 3.0
        arrow_tip_end = QPointF(arrow_length, 0)
        arrow_tip_base = QPointF(arrow_length - tip_length, 0)
        arrow_tip_top = arrow_tip_base + QPointF(0, -self.square_size / 6.0)
        arrow_tip_bottom = arrow_tip_base + QPointF(0, self.square_size / 6.0)

        #create arrow stem shape
        arrow_stem = QRectF(
            0,
            -arrow_width / 2.0,
            arrow_length - tip_length,
            arrow_width,
        )

        #create arrow tip shape
        arrow_tip = QPolygonF([
            arrow_tip_end, 
            arrow_tip_top, 
            arrow_tip_bottom,
        ])
        
        #draw arrow
        path = QPainterPath()
        path.addPolygon(arrow_tip)
        self.painter.translate(start_pt)
        self.painter.rotate(arrow_angle)
        self.painter.fillRect(arrow_stem, color)
        self.painter.resetTransform()
        self.painter.translate(start_pt)
        self.painter.rotate(arrow_angle)
        self.painter.fillPath(path, color)
        self.painter.resetTransform()