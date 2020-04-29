var fen = 'r4r2/p1pb1kPp/b1p2Ppp/3pP2P/1P3P2/3N1QPp/PPPp1P1P/R4K1R[QRNNrppp] b KQ - 0 1';
function init (fen) {
  var board = Chessboard('myBoard', 
	        { position: fen,
		  draggable: true,
		  dropOffBoard: 'trash',
 	   	  sparePieces: true
		});

  $('#startBtn').on('click', board.start);
  $('#clearBtn').on('click', board.clear);
  $('#tailBtn').on('click', function() { fen = board.tail(); });
  $('#headBtn').on('click', function() { fen = board.head(); });
  $('#prevBtn').on('click', function() { fen = board.prev(); console.log(fen);});
  $('#nextBtn').on('click', function() { fen = board.next(); });
  $('#inputFen').on('click', function() { 
    var newFen = $("#fen").val();
    console.log("new fen = " + newFen);
    fen = newFen;
    board.reinit(fen);
  });
}
 

$(document).ready(init(fen))