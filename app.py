import operator as op
from flask import Flask, render_template, escape, request, redirect
from bughouse import BughouseBoard
import chess
import chess_com
import tcn_parser

app = Flask(__name__)

#game 1: 9494798777
#game 2: 9494798775

@app.route("/")
def index():
    return render_template("index.html")

def process_game_data(board_num, game_data):
    raw_game_moves = game_data["game"]["moveList"]
    game_moves = tcn_parser.decode_tcn(raw_game_moves)
    raw_game_move_times = game_data["game"]["moveTimestamps"]
    game_move_times = [int(move_time) for move_time in raw_game_move_times.split(",")]
    
    prev_lost_time = 0
    total_time = 0
    processed_moves = []
    for i, move_data in enumerate(zip(game_moves, game_move_times)):
        move, move_time = move_data
        curr_lost_time = 1800 - move_time
        total_time = prev_lost_time + curr_lost_time
        prev_lost_time = curr_lost_time
        moving_player = chess.WHITE if i % 2 == 0 else chess.BLACK
        processed_move = (board_num, moving_player, move, move_time, total_time)
        processed_moves.append(processed_move)
    return processed_moves

def merge_processed_moves(first_moves, second_moves):
    bug_board = BughouseBoard()
    all_raw_moves = first_moves + second_moves
    all_raw_moves.sort(key=op.itemgetter(-1))
    all_moves = []
    times = [
        {
            chess.WHITE: 1800,
            chess.BLACK: 1800,
        },
        {
            chess.WHITE: 1800,
            chess.BLACK: 1800,
        },
    ]
    moving_players = [chess.WHITE, chess.WHITE]
    for raw_move in all_raw_moves:
        board_num, moving_player, move, move_time, total_time = raw_move
        print(raw_move)

        prev_move_time = times[board_num][moving_player]
        delta_move_time = prev_move_time - move_time
        other_moving_player = moving_players[not board_num]
        times[board_num][moving_player] = move_time
        #times[not board_num][other_moving_player] -= delta_move_time

        #print(board_num, moving_player, move)
        move_obj = chess.Move(
            from_square=chess.parse_square(move["from"]) if move["from"] != None else chess.A1,
            to_square=chess.parse_square(move["to"]),
            promotion=chess.Piece.from_symbol(move["promotion"]).piece_type if move["promotion"] != None else None,
            drop=chess.Piece.from_symbol(move["drop"]).piece_type if move["drop"] != None else None,
        )
        #print(move)
        bug_board.move(board_num, move_obj)
        fens = bug_board.get_fens()
        first_board_fen, second_board_fen = fens
        #print(fens)

        processed_move = {
            "board_num": board_num,
            "moving_player": moving_player,
            "from": move["from"],
            "to": move["to"],
            "drop": move["drop"],
            "promotion": move["promotion"],
            "first_white_time": times[0][chess.WHITE],
            "first_black_time": times[0][chess.BLACK],
            "second_white_time": times[1][chess.WHITE],
            "second_black_time": times[1][chess.BLACK],
            "first_board_fen": first_board_fen,
            "second_board_fen": second_board_fen,
        }
        all_moves.append(processed_move)
    return all_moves

def handle_user_input(user_input):
    if type(user_input) == int:
        return user_input
    elif type(user_input) == str:
        after_slash = user_input.split("/")[-1]
        if after_slash.startswith("live#g="):
            return int(after_slash.replace("live#g=", ""))
        else:
            return int(after_slash)

@app.route("/game", methods=["POST"])
def load_game():
    first_game_raw_id = request.form["first_game_id"]
    first_game_id = handle_user_input(first_game_raw_id)
    first_game_data = chess_com.fetch_game(first_game_id)
    second_game_id = int(first_game_data["game"]["partnerGameId"])
    second_game_data = chess_com.fetch_game(second_game_id)
    first_moves = process_game_data(0, first_game_data)
    second_moves = process_game_data(1, second_game_data)
    moves = merge_processed_moves(first_moves, second_moves)
    data = {
        "moves": moves,
    }
    return render_template("game.html", data=data)

if __name__ == "__main__": 
    app.run(debug=True)