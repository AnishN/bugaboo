import re
from enum import Enum
from chess.variant import CrazyhouseBoard, CrazyhousePocket
import chess

BOARD_ID_A = True
BOARD_ID_B = False

"""
B b'1B.' e4
B b'1b.' e6
A b'1A.' d4
B b'2B.' e5
A b'1a.' Nc6
B b'2b.' d6
A b'2A.' Bf4
B b'3B.' Nf3
A b'2a.' e6
B b'3b.' Nc6
A b'3A.' Nf3
A b'3a.' Nf6
B b'4B.' exd6 -> now black A gets pawn
B b'4b.' cxd6 -> now white A gets pawn
A b'4A.' Nc3
A b'4a.' Bb4
B b'5B.' Bb5
B b'5b.' Be7
B b'6B.' Bxc6+ -> now black A gets knight
B b'6b.' bxc6 -> now white A gets bishop
A b'5A.' P@d2 -> now white A only has bishop, no pawn anymore
B b'7B.' d4
B b'7b.' Nf6
B b'8B.' Nc3
B b'8b.' Nd5
B b'9B.' O-O
A b'5a.' Nd5
A b'6A.' Nxd5 -> now black B gets knight
A b'6a.' exd5 -> now white B gets knights
B b'9b.' N@f4 -> should be valid drop for black B...
"""

class BughouseBoard(object):

    def __init__(self):
        self.boards = {
            BOARD_ID_A: CrazyhouseBoard(),
            BOARD_ID_B: CrazyhouseBoard(),
        }

    def set_bpgn(self, bpgn):
        board_a = self.boards[BOARD_ID_A]
        board_b = self.boards[BOARD_ID_B]
        board_a.set_fen(chess.STARTING_FEN)
        board_b.set_fen(chess.STARTING_FEN)
        
        move_data = zip(bpgn.move_numbers, bpgn.moves)
        for move_number, move_bytes in move_data:
            san = move_bytes.decode("utf-8")
            
            board_id = self.get_board_id_from_move_number(move_number)
            #print(move_number, san, board_id)
            other_board_id = not(board_id)
            board = self.boards[board_id]
            other_board = self.boards[other_board_id]

            move = board.parse_san(san)
            is_capture = board.is_capture(move)
            capture_piece_type = None
            if is_capture:
                capture_piece = board.piece_at(move.to_square)
                if capture_piece == None:
                    if board.is_en_passant(move):
                        capture_piece_type = chess.PAWN
                else:
                    capture_piece_type = capture_piece.piece_type
                if board.promoted & (1 << move.to_square):
                    #print("FAKE PIECE")
                    capture_piece_type = chess.PAWN
                board.push(move)
                board.pockets[not(board.turn)].remove(capture_piece_type)#undo crazyhouse pocket rules
                other_board.pockets[board.turn].add(capture_piece_type)#and do bughouse pocket rules
                #print("CAPTURE")
                #print("White A", board_a.pockets[chess.WHITE])
                #print("Black A", board_a.pockets[chess.BLACK])
                #print("White B", board_b.pockets[chess.WHITE])
                #print("Black B", board_b.pockets[chess.BLACK])
                #print("")
            elif move.drop:
                board.push(move)
                #print("DROP")
                #print("White A", board_a.pockets[chess.WHITE])
                #print("Black A", board_a.pockets[chess.BLACK])
                #print("White B", board_b.pockets[chess.WHITE])
                #print("Black B", board_b.pockets[chess.BLACK])
                #print("")
            else:
                board.push(move)
            ##print(board_a)
            ##print(board_b)
            ##print("")

    def get_board_id_from_move_number(self, move_number):
        move_number_char = move_number[-2]
        if chr(move_number_char) in ("A", "a"):
            return BOARD_ID_A
        else:
            return BOARD_ID_B

"""
class CrazyhouseBoard(chess.Board):

    aliases = ["Crazyhouse", "Crazy House", "House", "ZH"]
    uci_variant = "crazyhouse"
    xboard_variant = "crazyhouse"
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[] w KQkq - 0 1"

    tbw_suffix = None
    tbz_suffix = None
    tbw_magic = None
    tbz_magic = None

    def __init__(self, fen: Optional[str] = starting_fen, chess960: bool = False) -> None:
        self.pockets = [CrazyhousePocket(), CrazyhousePocket()]
        super().__init__(fen, chess960=chess960)

    def reset_board(self) -> None:
        super().reset_board()
        self.pockets[chess.WHITE].reset()
        self.pockets[chess.BLACK].reset()

    def clear_board(self) -> None:
        super().clear_board()
        self.pockets[chess.WHITE].reset()
        self.pockets[chess.BLACK].reset()

    def _board_state(self: CrazyhouseBoardT) -> _CrazyhouseBoardState[CrazyhouseBoardT]:
        return _CrazyhouseBoardState(self)

    def push(self, move: chess.Move) -> None:
        super().push(move)
        if move.drop:
            self.pockets[not self.turn].remove(move.drop)

    def _push_capture(self, move: chess.Move, capture_square: chess.Square, piece_type: chess.PieceType, was_promoted: bool) -> None:
        if was_promoted:
            self.pockets[self.turn].add(chess.PAWN)
        else:
            self.pockets[self.turn].add(piece_type)

    def can_claim_fifty_moves(self) -> bool:
        return False

    def is_seventyfive_moves(self) -> bool:
        return False

    def is_irreversible(self, move: chess.Move) -> bool:
        return self._reduces_castling_rights(move)

    def _transposition_key(self) -> Hashable:
        return (super()._transposition_key(),
                self.promoted,
                str(self.pockets[chess.WHITE]), str(self.pockets[chess.BLACK]))

    def legal_drop_squares_mask(self) -> chess.Bitboard:
        king = self.king(self.turn)
        if king is None:
            return ~self.occupied

        king_attackers = self.attackers_mask(not self.turn, king)

        if not king_attackers:
            return ~self.occupied
        elif chess.popcount(king_attackers) == 1:
            return chess.BB_BETWEEN[king][chess.msb(king_attackers)] & ~self.occupied
        else:
            return chess.BB_EMPTY

    def legal_drop_squares(self) -> chess.SquareSet:
        return chess.SquareSet(self.legal_drop_squares_mask())

    def is_pseudo_legal(self, move: chess.Move) -> bool:
        if move.drop and move.from_square == move.to_square:
            return (
                move.drop != chess.KING and
                not chess.BB_SQUARES[move.to_square] & self.occupied and
                not (move.drop == chess.PAWN and chess.BB_SQUARES[move.to_square] & chess.BB_BACKRANKS) and
                self.pockets[self.turn].count(move.drop) > 0)
        else:
            return super().is_pseudo_legal(move)

    def is_legal(self, move: chess.Move) -> bool:
        if move.drop:
            return self.is_pseudo_legal(move) and bool(self.legal_drop_squares_mask() & chess.BB_SQUARES[move.to_square])
        else:
            return super().is_legal(move)

    def generate_pseudo_legal_drops(self, to_mask: chess.Bitboard = chess.BB_ALL) -> Iterator[chess.Move]:
        for to_square in chess.scan_forward(to_mask & ~self.occupied):
            for pt, count in self.pockets[self.turn].pieces.items():
                if count and (pt != chess.PAWN or not chess.BB_BACKRANKS & chess.BB_SQUARES[to_square]):
                    yield chess.Move(to_square, to_square, drop=pt)

    def generate_legal_drops(self, to_mask: chess.Bitboard = chess.BB_ALL) -> Iterator[chess.Move]:
        return self.generate_pseudo_legal_drops(to_mask=self.legal_drop_squares_mask() & to_mask)

    def generate_legal_moves(self, from_mask: chess.Bitboard = chess.BB_ALL, to_mask: chess.Bitboard = chess.BB_ALL) -> Iterator[chess.Move]:
        return itertools.chain(
            super().generate_legal_moves(from_mask, to_mask),
            self.generate_legal_drops(from_mask & to_mask))

    def parse_san(self, san: str) -> chess.Move:
        if "@" in san:
            uci = san.rstrip("+# ")
            if uci[0] == "@":
                uci = "P" + uci
            move = chess.Move.from_uci(uci)
            if not self.is_legal(move):
                raise ValueError(f"illegal drop san: {san!r} in {self.fen()}")
            return move
        else:
            return super().parse_san(san)

    def has_insufficient_material(self, color: chess.Color) -> bool:
        # In practise no material can leave the game, but this is easy to
        # implement anyway. Note that bishops can be captured and put onto
        # a different color complex.
        return (
            chess.popcount(self.occupied) + sum(len(pocket) for pocket in self.pockets) <= 3 and
            not self.promoted and
            not self.pawns and
            not self.rooks and
            not self.queens and
            not any(pocket.count(chess.PAWN) for pocket in self.pockets) and
            not any(pocket.count(chess.ROOK) for pocket in self.pockets) and
            not any(pocket.count(chess.QUEEN) for pocket in self.pockets))

    def set_fen(self, fen: str) -> None:
        position_part, info_part = fen.split(None, 1)

        # Transform to lichess-style ZH FEN.
        if position_part.endswith("]"):
            if position_part.count("/") != 7:
                raise ValueError(f"expected 8 rows in position part of zh fen: {fen!r}")
            position_part = position_part[:-1].replace("[", "/", 1)

        # Split off pocket part.
        if position_part.count("/") == 8:
            position_part, pocket_part = position_part.rsplit("/", 1)
        else:
            pocket_part = ""

        # Parse pocket.
        white_pocket = CrazyhousePocket(c.lower() for c in pocket_part if c.isupper())
        black_pocket = CrazyhousePocket(c for c in pocket_part if not c.isupper())

        # Set FEN and pockets.
        super().set_fen(position_part + " " + info_part)
        self.pockets[chess.WHITE] = white_pocket
        self.pockets[chess.BLACK] = black_pocket

    def board_fen(self, promoted: Optional[bool] = None) -> str:
        if promoted is None:
            promoted = True
        return super().board_fen(promoted=promoted)

    def epd(self, shredder: bool = False, en_passant: str = "legal", promoted: Optional[bool] = None, **operations: Union[None, str, int, float, chess.Move, Iterable[chess.Move]]) -> str:
        epd = super().epd(shredder=shredder, en_passant=en_passant, promoted=promoted)
        board_part, info_part = epd.split(" ", 1)
        return f"{board_part}[{str(self.pockets[chess.WHITE]).upper()}{self.pockets[chess.BLACK]}] {info_part}"

    def copy(self: CrazyhouseBoardT, stack: Union[bool, int] = True) -> CrazyhouseBoardT:
        board = super().copy(stack=stack)
        board.pockets[chess.WHITE] = self.pockets[chess.WHITE].copy()
        board.pockets[chess.BLACK] = self.pockets[chess.BLACK].copy()
        return board

    def mirror(self: CrazyhouseBoardT) -> CrazyhouseBoardT:
        board = super().mirror()
        board.pockets[chess.WHITE] = self.pockets[chess.BLACK].copy()
        board.pockets[chess.BLACK] = self.pockets[chess.WHITE].copy()
        return board

    def status(self) -> chess.Status:
        status = super().status()

        if chess.popcount(self.pawns) + self.pockets[chess.WHITE].count(chess.PAWN) + self.pockets[chess.BLACK].count(chess.PAWN) <= 16:
            status &= ~chess.STATUS_TOO_MANY_BLACK_PAWNS
            status &= ~chess.STATUS_TOO_MANY_WHITE_PAWNS

        if chess.popcount(self.occupied) + len(self.pockets[chess.WHITE]) + len(self.pockets[chess.BLACK]) <= 32:
            status &= ~chess.STATUS_TOO_MANY_BLACK_PIECES
            status &= ~chess.STATUS_TOO_MANY_WHITE_PIECES

        return status
"""