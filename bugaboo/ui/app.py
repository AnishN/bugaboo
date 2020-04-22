import os
os.environ["QT_LOGGING_RULES"] = "qt5ct.debug=false"
import sys
import time
import chess
import random

from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtWidgets import QTabWidget

from bugaboo.core.bughouse_board import *
from bugaboo.io.bpgn import *
from bugaboo.ui.chess_board import *
from bugaboo.ui.chess_game_info import *
from bugaboo.ui.chess_move_list import *

class App(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
        self.setup_window()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_boards()
        self.setup_side_bar()
        self.setup_control_bar()
        self.setup_layout()

    def setup_window(self):
        self.window = QMainWindow()
        self.window.resize(800, 600)
        self.window.setWindowTitle("Bugaboo")
        self.window.show()

    def setup_layout(self):
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.board_a)
        main_layout.addWidget(self.board_b)

        self.full_side_bar = QWidget()
        self.full_side_bar_layout = QVBoxLayout()
        self.full_side_bar_layout.addWidget(self.side_bar)
        self.full_side_bar_layout.addWidget(self.control_bar)
        self.full_side_bar.setLayout(self.full_side_bar_layout)
        main_layout.addWidget(self.full_side_bar)

        self.widget = QWidget()
        self.window.setCentralWidget(self.widget)
        self.widget.setLayout(main_layout)

    def setup_menu_bar(self):
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit the application")
        quit_action.triggered.connect(sys.exit)

        open_bpgn_action = QAction("Open BPGN", self)
        open_bpgn_action.setShortcut("Ctrl+O")
        open_bpgn_action.setStatusTip("Open a .BPGN bughouse game file")
        open_bpgn_action.triggered.connect(self.open_bpgn_file)

        self.menu_bar = self.window.menuBar()
        file_menu = self.menu_bar.addMenu("File")
        actions = [
            open_bpgn_action,
            quit_action,
        ]
        file_menu.addActions(actions)

    def setup_status_bar(self):
        self.status_bar = self.window.statusBar()
        self.status_bar.showMessage("Welcome to Bugaboo!", msecs=5000)

    def setup_boards(self):
        self.board_a = ChessBoardWidget()
        self.board_b = ChessBoardWidget()
        self.board_b.set_flip_board(True)
        self.game = BughouseBoard()

    def setup_side_bar(self):
        self.game_list = QWidget()
        self.game_info = ChessGameInfoWidget()
        self.move_list = ChessMoveListWidget()
        self.side_bar = QTabWidget()
        self.side_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.side_bar.addTab(self.game_list, "Game List")
        self.side_bar.addTab(self.game_info, "Game Info")
        self.side_bar.addTab(self.move_list, "Game Text")

    def setup_control_bar(self):
        self.first_button = QPushButton()
        self.first_button_icon = QIcon("./bugaboo/resources/icons/first_move.png")
        self.first_button.setIcon(self.first_button_icon)
        #self.first_button.clicked.connect(self.go_to_first_move)

        self.previous_button = QPushButton()
        self.previous_button_icon = QIcon("./bugaboo/resources/icons/previous_move.png")
        self.previous_button.setIcon(self.previous_button_icon)

        self.next_button = QPushButton()
        self.next_button_icon = QIcon("./bugaboo/resources/icons/next_move.png")
        self.next_button.setIcon(self.next_button_icon)

        self.last_button = QPushButton()
        self.last_button_icon = QIcon("./bugaboo/resources/icons/last_move.png")
        self.last_button.setIcon(self.last_button_icon)

        self.control_bar = QWidget()
        self.control_bar_layout = QHBoxLayout()
        self.control_bar_layout.addWidget(self.first_button)
        self.control_bar_layout.addWidget(self.previous_button)
        self.control_bar_layout.addWidget(self.next_button)
        self.control_bar_layout.addWidget(self.last_button)
        self.control_bar.setLayout(self.control_bar_layout)

    def open_bpgn_file(self):
        file_path, file_type = QFileDialog.getOpenFileName(self.window, "Open BPGN", None, "Bughouse Games (*.bpgn)")
        self.status_bar.showMessage("Opening BPGN: {0}".format(file_path))
        bpgns = BPGN.from_path(file_path)
        bpgn = bpgns[0]
        self.move_list.set_bpgn(bpgn)
        self.game.set_bpgn(bpgn)
        self.update_boards()
        self.status_bar.clearMessage()

    def update_boards(self):
        self.board_a.set_position(self.game.boards[BOARD_ID_A])
        self.board_b.set_position(self.game.boards[BOARD_ID_B])