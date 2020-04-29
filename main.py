import chess
from chess.variant import CrazyhouseBoard, CrazyhousePocket
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
@app.route('/index')
def index():
    print('index')
    return render_template('index.html')

@app.route('/chess', methods=['GET', 'POST'])
def chess():
    print ('in chess()')
    fen = request.get_json().get('fen')
    move = request.get_json().get('move')
    out_fen = bug_single_board_move(fen, move)
    if (out_fen is None): return jsonify('false')
    return jsonify(out_fen)

def bug_single_board_move(fen, san_move):
    board = CrazyhouseBoard()
    board.set_fen(fen)
    try:
        move = board.parse_san(san_move)
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
                capture_piece_type = chess.PAWN
            board.push(move)
            board.pockets[not(board.turn)].remove(capture_piece_type)#undo crazyhouse pocket rules
        else:
            board.push(move)
        out_fen = board.fen()
        return out_fen
    except ValueError:
        return None

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='3000')