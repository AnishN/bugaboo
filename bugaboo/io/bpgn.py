import re

class BPGN(object):

    def __init__(self):
        self.tags = {}
        self.moves = []
        self.move_times = []
        self.move_numbers = []
        self.end_comment = None

    @staticmethod
    def from_path(bpgn_path):
        in_file = open(bpgn_path, "rb")
        bpgn_data = in_file.read()
        in_file.close()
        games = BPGN.from_bytes(bpgn_data)    
        return games
    
    @staticmethod
    def from_bytes(bpgn_data):
        tokenizer = re.compile(rb"""
            (?P<TAG>\[.*?\]) |
            (?P<MOVE_TIME>\{\d+\.?\d+\}) |
            (?P<END_COMMENT>\{.*?\}\s(1-0|0-1|1\/2\-1\/2|\*))|
            (?P<COMMENT>\{C:.*?\}) | 
            #(?P<VARIATION_START>\() |
            #(?P<VARIATION_END>\)) |
            (?P<MOVE_NUMBER>\d+[ABab]\.) |
            (?P<MOVE>((O\-O\-O)|(O\-O)|([RBQKPN])?([a-h])?([1-8])?([x@])?([a-h])([1-8])([=]?)([QNRB]?)([+#]?)))
        """, re.VERBOSE)
        
        tag_parser = re.compile(rb"(?P<TAG_PART>[A-Za-z0-9\+\-\.\: ]+)")
        end_comment_text_parser = re.compile(rb"\{.+\}")

        in_header = False
        games = []
        game = None

        for match in re.finditer(tokenizer, bpgn_data):
            tag = match.group("TAG")
            move_time = match.group("MOVE_TIME")
            move_number = match.group("MOVE_NUMBER")
            move = match.group("MOVE")
            comment = match.group("COMMENT")
            end_comment = match.group("END_COMMENT")
            
            if tag:
                if not in_header:
                    game = BPGN()
                    games.append(game)
                in_header = True
                tag_matches = re.findall(tag_parser, tag)
                tag_keys = tag_matches[::2]
                tag_values = tag_matches[1::2]
                tag_dict = dict(zip(tag_keys, tag_values))
                game.tags.update(tag_dict)
            else:
                if game == None:
                    raise ValueError("Invalid BPGN file: move text present before header")
                in_header = False
                if move_number:
                    game.move_numbers.append(move_number)
                elif move_time:
                    game.move_times.append(move_time)
                elif move:
                    game.moves.append(move)
                elif comment:
                    contents = comment[3:-1]
                    #if not contents.startswith(b"This is game number"):
                    #    print(len(games), contents)
                elif end_comment:
                    end_comment_text = re.findall(end_comment_text_parser, end_comment)[0][1:-1]
                    game.end_comment = end_comment_text
        return games