from flask import Flask, render_template, escape, request, redirect
import chess_com
import tcn_parser

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game", methods=["POST"])
def load_game():
    first_game_id = request.form["first_game_id"]
    first_game_data = chess_com.fetch_game(first_game_id)
    first_game_moves = tcn_parser.decode_tcn(first_game_data["game"]["moveList"])
    second_game_id = request.form["second_game_id"]
    second_game_data = chess_com.fetch_game(second_game_id)
    second_game_moves = tcn_parser.decode_tcn(second_game_data["game"]["moveList"])
    data = {
        "first_game_id": first_game_id,
        "first_game_data": first_game_data,
        "first_game_moves": first_game_moves,
        "second_game_id": second_game_id,
        "second_game_data": second_game_data,
        "second_game_moves": second_game_moves,
    }
    return render_template("game.html", data=data)

if __name__ == "__main__": 
    app.run(debug=True)