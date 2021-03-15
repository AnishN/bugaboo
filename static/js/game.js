var app = new PIXI.Application({
    width: 400, 
    height: 400, 
    backgroundColor: 0x1099bb, 
    resolution: window.devicePixelRatio || 1,
    antialias: true,
});

document.getElementById("first_game_board").appendChild(app.view);

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

var textures = {};
var key;
var file_path;
for(key in file_paths)
{
    file_path = file_paths[key];
    textures[key] = new PIXI.Texture.from(file_path);
}
var square_size = 50;
var light_color = 0xEEEED2;
var dark_color = 0x769656;
var num_files = 8;
var num_ranks = 8;

function draw_board(app, square_size, light_color, dark_color)
{
    var grid = new PIXI.Graphics();
    var i = 0;
    var j = 0;
    for(i = 0; i < 8; i++)
    {
        for(j = 0; j < 8; j++)
        {
            if(i % 2 == j % 2)
            {
                grid.beginFill(light_color);
            }
            else
            {
                grid.beginFill(dark_color);
            }    
            grid.drawRect(i * square_size, j * square_size, square_size, square_size);
        }
    }
    app.stage.addChild(grid);
}

function draw_piece(app, square_size, piece_type, file, rank)
{
    var sprite = new PIXI.Sprite(textures[piece_type]);
    app.stage.addChild(sprite);
    sprite.x = file * square_size;
    sprite.y = (num_ranks - rank - 1) * square_size;
    sprite.width = square_size;
    sprite.height = square_size;
}

function parse_fen(fen)
{
    var parts = fen.split(" ");
    var position = parts[0];
    var active_color = parts[1];
    var castling = parts[2];
    var en_passant = parts[3];
    var half_move_clock = parts[4];
    var full_move_number = parts[5];

    var pocket = position.split("[")[1].split("]")[0];
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

function draw_position(app, fen)
{
    var piece_pos;
    var i;
    piece_positions = parse_fen(fen);
    console.log(piece_positions);
    draw_board(app, square_size, light_color, dark_color);
    for(i = 0; i < piece_positions.length; i++)
    {
        piece_pos = piece_positions[i];
        console.log(piece_pos);
        draw_piece(app, square_size, piece_pos[2], piece_pos[0], piece_pos[1]);
    }
}

draw_position(app, moves[moves.length - 1].second_board_fen);
