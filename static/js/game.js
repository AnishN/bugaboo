const text_style = new PIXI.TextStyle({
    fontFamily: "Fira Sans",
    fontSize: 20,
    fill: "#ffffff",
    stroke: "#769656",
    strokeThickness: 2,
    dropShadow: true,
    dropShadowColor: "#000000",
    dropShadowBlur: 2,
    dropShadowAngle: Math.PI / 4,
    dropShadowDistance: 2,
    wordWrap: true,
    wordWrapWidth: 440,
    lineJoin: "round",
    align: "center",
});

class ChessBoardPocket
{
    constructor(board_size, pocket_size, pocket_color, piece_textures, piece_color)
    {
        this.board_size = board_size;
        this.pocket_size = pocket_size;
        this.pocket_color = pocket_color;
        this.piece_textures = piece_textures;

        this.pawn = new PIXI.Sprite();
        this.knight = new PIXI.Sprite();
        this.bishop = new PIXI.Sprite();
        this.rook = new PIXI.Sprite();
        this.queen = new PIXI.Sprite();
        this.pieces = [this.pawn, this.knight, this.bishop, this.rook, this.queen];
        this.set_color(piece_color);
        this.graphics = new PIXI.Graphics();
    }

    set_color(piece_color)
    {
        this.piece_color = piece_color
        if(this.piece_color == true)//white
        {
            this.pawn.texture = this.piece_textures["P"];
            this.knight.texture = this.piece_textures["N"];
            this.bishop.texture = this.piece_textures["B"];
            this.rook.texture = this.piece_textures["R"];
            this.queen.texture = this.piece_textures["Q"];
        }
        else//black
        {
            this.pawn.texture = this.piece_textures["p"];
            this.knight.texture = this.piece_textures["n"];
            this.bishop.texture = this.piece_textures["b"];
            this.rook.texture = this.piece_textures["r"];
            this.queen.texture = this.piece_textures["q"];
        }
    }

    draw_pocket(piece_pockets, player_time)
    {
        var i;
        var piece;
        var piece_char;
        var piece_chars;
        var piece_count;
        var piece_count_text;
        var white_piece_chars = ["P", "N", "B", "R", "Q"];
        var black_piece_chars = ["p", "n", "b", "r", "q"];
        
        this.graphics.removeChildren();
        this.graphics.beginFill(this.pocket_color);
        this.graphics.drawRect(0, 0, this.board_size, this.pocket_size);
        this.graphics.endFill(this.pocket_color);
        
        if(this.piece_color == true)//white
        {
            piece_chars = white_piece_chars;
        }
        else//black
        {
            piece_chars = black_piece_chars;
        }
        
        for(i = 0; i < piece_chars.length; i++)
        {
            piece_char = piece_chars[i];
            piece = this.pieces[i];
            piece_count = piece_pockets[piece_char];
            if(piece_count == 0)
            {
                piece.alpha = 0.1;
            }
            else
            {
                piece.alpha = 1.0;
            }
            piece.x = i * this.pocket_size;
            piece.y = 0;
            piece.width = this.pocket_size;
            piece.height = this.pocket_size;
            this.graphics.addChild(piece);

            if(piece_count != 0)
            {
                piece_count_text = new PIXI.Text(piece_count, text_style);
                piece_count_text.pivot.set(
                    piece_count_text.width / 2, 
                    piece_count_text.height / 2
                );
                piece_count_text.x = this.pocket_size / 2 + (i * this.pocket_size);
                piece_count_text.y = this.pocket_size / 2;
                this.graphics.addChild(piece_count_text);
            }
        }

        var player_time_text = new PIXI.Text(player_time, text_style);
        player_time_text.pivot.set(
            player_time_text.width / 2, 
            player_time_text.height / 2
        );
        player_time_text.x = this.pocket_size / 2 + (6.5 * this.pocket_size);
        player_time_text.y = this.pocket_size / 2;
        this.graphics.addChild(player_time_text);

        if(this.piece_color == true)
        {
            this.graphics.beginFill(0xFFFFFF);
        }
        else
        {
            this.graphics.beginFill(0x000000);
        }
        this.graphics.drawRoundedRect(
            (this.board_size * 0.8) - (this.pocket_size * 0.2),
            this.pocket_size * 0.1,
            this.board_size * 0.2,
            this.pocket_size * 0.8,
            5
        );
        this.graphics.endFill();
    }
}

class ChessBoard
{
    constructor(board_size, light_color, dark_color, piece_textures, flip, pocket_size, pocket_color)
    {
        this.board_size = board_size;
        this.light_color = light_color;
        this.dark_color = dark_color;
        this.flip = flip;
        this.pocket_size = pocket_size;
        this.pocket_color = pocket_color;
        this.graphics = new PIXI.Graphics();
        this.piece_textures = piece_textures;
        this.top_pocket = new ChessBoardPocket(board_size, pocket_size, pocket_color, piece_textures, !flip);
        this.bottom_pocket = new ChessBoardPocket(board_size, pocket_size, pocket_color, piece_textures, flip);
    }

    parse_fen_piece_positions(fen)
    {
        var parts = fen.split(" ");
        var position = parts[0];
        /*
        var active_color = parts[1];
        var castling = parts[2];
        var en_passant = parts[3];
        var half_move_clock = parts[4];
        var full_move_number = parts[5];
        */

        var ranks = position.split("[")[0].split("/")
        var piece_positions = []
        var rank;
        var rank_char_index;
        var rank_char;
        var rank_pos;
        var file_pos;
        var rank_char_shift;
        var square = {};
        var piece_pos;
        for(rank_pos = 0; rank_pos < ranks.length; rank_pos++)
        {
            file_pos = 0;
            rank = ranks[rank_pos].split("");
            for(rank_char_index = 0; rank_char_index < rank.length; rank_char_index++)
            {
                rank_char = rank[rank_char_index];
                rank_char_shift = parseInt(rank_char)
                if(!isNaN(rank_char_shift))
                {
                    file_pos += rank_char_shift;
                }
                else
                {
                    piece_pos = [file_pos, ranks.length - rank_pos - 1, rank_char];
                    piece_positions.push(piece_pos);
                    file_pos += 1;
                }
            }
        }
        return piece_positions;
    }

    parse_fen_piece_pockets(fen)
    {
        var parts = fen.split(" ");
        var position = parts[0];
        var pocket = position.split("[")[1].split("]")[0];
        var piece_pockets = {
            "P": 0,
            "N": 0,
            "B": 0,
            "R": 0,
            "Q": 0,
            "p": 0,
            "n": 0,
            "b": 0,
            "r": 0,
            "q": 0,
        }
        var piece_char;
        var pocket_pos;
        for(pocket_pos = 0; pocket_pos < pocket.length; pocket_pos++)
        {
            piece_char = pocket[pocket_pos];
            piece_pockets[piece_char] += 1;
        }
        return piece_pockets;
    }

    draw_squares()
    {
        var i = 0;
        var j = 0;
        var square_size = this.board_size / 8;

        if(this.flip == false)
        {
            for(i = 0; i < 8; i++)
            {
                for(j = 0; j < 8; j++)
                {
                    if(i % 2 == j % 2)
                    {
                        this.graphics.beginFill(this.light_color);
                    }
                    else
                    {
                        this.graphics.beginFill(this.dark_color);
                    }    
                    this.graphics.drawRect(
                        i * square_size, 
                        j * square_size + this.pocket_size, 
                        square_size, 
                        square_size
                    );
                }
            }
        }
        else
        {
            for(i = 0; i < 8; i++)
            {
                for(j = 0; j < 8; j++)
                {
                    if(i % 2 != j % 2)
                    {
                        this.graphics.beginFill(this.light_color);
                    }
                    else
                    {
                        this.graphics.beginFill(this.dark_color);
                    }    
                    this.graphics.drawRect(
                        i * square_size, 
                        j * square_size + this.pocket_size, 
                        square_size, 
                        square_size
                    );
                }
            }
        }
    }
    
    draw_piece(piece_type, file, rank)
    {
        var sprite = new PIXI.Sprite(this.piece_textures[piece_type]);
        var square_size = this.board_size / 8;
        this.graphics.addChild(sprite);
        sprite.x = file * square_size;
        if(this.flip == false)
        {
            sprite.y = (num_ranks - rank - 1) * square_size;
        }
        else
        {
            sprite.y = rank * square_size;
        }
        sprite.y += this.pocket_size;
        sprite.width = square_size;
        sprite.height = square_size;
    }

    draw_pockets(piece_pockets, top_time, bottom_time)
    {
        this.graphics.addChild(this.top_pocket.graphics);
        this.top_pocket.graphics.x = 0;
        this.top_pocket.graphics.y = this.pocket_size + this.board_size;
        this.top_pocket.draw_pocket(piece_pockets, top_time);

        this.graphics.addChild(this.bottom_pocket.graphics);
        this.bottom_pocket.graphics.x = 0;
        this.bottom_pocket.graphics.y = 0;//this.pocket_size + this.board_size;
        this.bottom_pocket.draw_pocket(piece_pockets, bottom_time);
    }

    draw_position(fen, top_time, bottom_time)
    {
        var piece_positions = this.parse_fen_piece_positions(fen);
        var piece_pockets = this.parse_fen_piece_pockets(fen);
        var piece_pos;
        var i;

        this.graphics.removeChildren();
        this.draw_squares();
        for(i = 0; i < piece_positions.length; i++)
        {
            piece_pos = piece_positions[i];
            this.draw_piece(piece_pos[2], piece_pos[0], piece_pos[1]);
        }
        
        this.draw_pockets(piece_pockets, top_time, bottom_time);
    }
}

function update_nav_buttons()
{
    if(curr_move_index == 0)
    {
        document.getElementById("head_button").disabled = true;
    }
    else
    {
        document.getElementById("head_button").disabled = false;
    }

    if(curr_move_index == moves.length - 1)
    {
        document.getElementById("tail_button").disabled = true;
    }
    else
    {
        document.getElementById("tail_button").disabled = false;
    }
}

function redraw_boards()
{
    var curr_move = moves[curr_move_index];
    first_board.draw_position(curr_move.first_board_fen, curr_move.first_white_time, curr_move.first_black_time);
    second_board.draw_position(curr_move.second_board_fen, curr_move.second_black_time, curr_move.second_white_time);
}

document.getElementById("head_button").addEventListener("click", function() {
    curr_move_index = 0;
    redraw_boards();
    update_nav_buttons();
});

document.getElementById("prev_button").addEventListener("click", function() {
    curr_move_index -= 1;
    if(curr_move_index < 0)
    {
        curr_move_index = 0;
    }
    redraw_boards();
    update_nav_buttons();
});

document.getElementById("next_button").addEventListener("click", function() {
    curr_move_index += 1;
    if(curr_move_index == moves.length)
    {
        curr_move_index = moves.length - 1;
    }
    redraw_boards();
    update_nav_buttons();
}); 

document.getElementById("tail_button").addEventListener("click", function() {
    curr_move_index = moves.length - 1;
    redraw_boards();
    update_nav_buttons();
});

var light_color = 0xEEEED2;
var dark_color = 0x769656;
var num_files = 8;
var num_ranks = 8;
var padding = 10;
var pocket_size = 380/8;
var pocket_color = 0x777777;

const app = new PIXI.Application({
    width: 800, 
    height: 500, 
    backgroundColor: 0x4D4D4D, 
    resolution: window.devicePixelRatio || 1,
    antialias: true,
});

document.getElementById("game").appendChild(app.view);

var file_paths = {
    "p": "static/img/chesspieces/alpha/bP.png",
    "n": "static/img/chesspieces/alpha/bN.png",
    "b": "static/img/chesspieces/alpha/bB.png",
    "r": "static/img/chesspieces/alpha/bR.png",
    "q": "static/img/chesspieces/alpha/bQ.png",
    "k": "static/img/chesspieces/alpha/bK.png",
    "P": "static/img/chesspieces/alpha/wP.png",
    "N": "static/img/chesspieces/alpha/wN.png",
    "B": "static/img/chesspieces/alpha/wB.png",
    "R": "static/img/chesspieces/alpha/wR.png",
    "Q": "static/img/chesspieces/alpha/wQ.png",
    "K": "static/img/chesspieces/alpha/wK.png",
}

var piece_textures = {};
var key;
var file_path;
for(key in file_paths)
{
    file_path = file_paths[key];
    piece_textures[key] = new PIXI.Texture.from(file_path);
}

var curr_move_index = moves.length - 1;
var board_size = (app.screen.width / 2) - (2 * padding);
var first_board = new ChessBoard(board_size, light_color, dark_color, piece_textures, false, pocket_size, pocket_color);
var second_board = new ChessBoard(board_size, light_color, dark_color, piece_textures, true, pocket_size, pocket_color);
first_board.graphics.x = padding;
first_board.graphics.y = padding;
second_board.graphics.x = board_size + (3 * padding);
second_board.graphics.y = padding;
app.stage.addChild(first_board.graphics);
app.stage.addChild(second_board.graphics);
update_nav_buttons();
redraw_boards();