const WHITE = true;
const BLACK = false;

const PIECE_TYPES = Object.freeze(
{
    "PAWN": 1,
    "KNIGHT": 2,
    "BISHOP": 3,
    "ROOK": 4,
    "QUEEN": 5,
    "KING": 6,
});

const PIECE_SYMBOLS = Object.freeze(["p", "n", "b", "r", "q", "k"]);
function get_piece_symbol(piece_type)
{
    return PIECE_SYMBOLS[piece_type -1];
}

const NUM_FILES = 8;
const FILE_NAMES = Object.freeze(
{
    "A": 0, 
    "B": 1, 
    "C": 2, 
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
});

const NUM_RANKS = 8;
const RANK_NAMES = Object.freeze(
{    
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
});

const NUM_SQUARES = 64;
const SQUARE_NAMES = {};
for(var i = 0; i < NUM_FILES; i++)
{
    for(var j = 0; j < NUM_RANKS; j++)
    {
        var square_name = Object.keys(FILE_NAMES)[i].concat(Object.keys(RANK_NAMES)[j]);
        SQUARE_NAMES[square_name] = i * NUM_FILES + j;
    }
}
Object.freeze(SQUARE_NAMES);

