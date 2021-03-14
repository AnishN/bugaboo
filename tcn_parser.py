import math
#1:1 port of chess-tcn npm library that chess.com uses
#this is used to encode the moveList into a string

def decode_tcn(n):
    tcn_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?{~}(^)[_]@#$,./&-*++="
    piece_chars = "qnrbkp"
    o = 0
    s = 0
    u = 0
    w = len(n)
    c = []
    for i in range(0, w, 2):
        u = {
            "from": None,
            "to": None,
            "drop": None,
            "promotion": None,
        }
        o = tcn_chars.index(n[i])
        s = tcn_chars.index(n[i + 1])
        if s > 63:
            u["promotion"] = piece_chars[math.floor((s - 64) / 3)]
            s = o + (-8 if o < 16 else 8) + ((s - 1) % 3) - 1
        if o > 75:
            u["drop"] = piece_chars[o - 79]
        else:
            u["from"] = tcn_chars[o % 8] + str(math.floor(o / 8) + 1)
        u["to"] = tcn_chars[s % 8] + str(math.floor(s / 8) + 1)
        c.append(u)
    return c

def encode_tcn(n):
    tcn_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?{~}(^)[_]@#$,./&-*++="
    piece_chars = "qnrbkp"
    o = len(n)
    s = 0
    u = 0
    w = ""
    for i in range(o):
        if n[i]["drop"]:
            s = 79 + piece_chars.index(n[i]["drop"])
        else: 
            s = tcn_chars.index(n[i]["from"][0]) + 8 * (int(n[i]["from"][1]) - 1)
        u = tcn_chars.index(n[i]["to"][0]) + 8 * (int(n[i]["to"][1]) - 1)
        if n[i]["promotion"]:
            add_u = (9 + u - s if u < s else u - s - 7)
            u = 3 * piece_chars.index(n[i]["promotion"]) + 64 + add_u
        w += tcn_chars[s]
        w += tcn_chars[u]
    return w