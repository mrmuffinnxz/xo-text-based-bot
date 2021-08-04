import numpy as np
import random

# game system

win = [[1,2,3],[4,5,6],[7,8,9],[1,5,9],[3,5,7],[1,4,7],[2,5,8],[3,6,9]]
X = []
O = []

def displayBoard():
    board = np.array([' '] * 9)
    board[X] = ['X']
    board[O] = ['O']
    print(board.reshape([3,3]))

def checkwin(player):
    for w in win:
        if all(i-1 in player for i in w):
            return True
    return False

# AI

def ai(player,opponent):
    valid_move = list(set(range(9)) - set(player+opponent))
    move_score = [-100] * 9
    for m in valid_move:
        tmp = player + [m]
        move_score[m], critical_move = eval_score(tmp, opponent)
        if len(critical_move) > 0:
            move = [i-1 for i in random.choice(critical_move) if i-1 in valid_move]
            return random.choice(move)
    max_score = max(move_score)
    max_score_move = [i for i,j in enumerate(move_score) if j == max_score]
    return random.choice(max_score_move)

def eval_score(player,opponent):
    score_player, score_opponent, critical_move = cal_score(player,opponent)
    return 1 + score_player - score_opponent, critical_move

def cal_score(player,opponent):
    score_player = score_opponent = 0
    critical_move = []
    for w in win:
        board_player = [i-1 in player for i in w]
        board_opponent = [i-1 in opponent for i in w]
        if not any(board_player):
            tmp_score_opponent = board_opponent.count(True)
            score_opponent += tmp_score_opponent
            if tmp_score_opponent == 2:
                critical_move.append(w)
        if not any(board_opponent):
            score_player += board_player.count(True)
    return score_player, score_opponent, critical_move

# mini max AI

def mini_max_ai(player, opponent):
    valid_move = list(set(range(9)) - set(player + opponent))
    move_score = [-100] * 9
    for m in valid_move:
        tmp = player + [m]
        move_score[m] = cal_score_minimax(tmp, opponent, False)
    print(move_score)
    max_score = max(move_score)
    max_score_move = [i for i, j in enumerate(move_score) if j == max_score]
    return random.choice(max_score_move)

def cal_score_minimax(player, opponent, is_player_turn):
    if checkwin(player):
        return 1
    elif checkwin(opponent):
        return -1
    valid_move = list(set(range(9)) - set(player + opponent))
    if len(valid_move) == 0:
        return 0
    if is_player_turn:
        max_score = -100
        for m in valid_move:
            tmp = player + [m]
            score = cal_score_minimax(tmp, opponent, False)
            max_score = max(max_score, score)
        return max_score
    else:
        min_score = 100
        for m in valid_move:
            tmp = opponent + [m]
            score = cal_score_minimax(player, tmp, True)
            min_score = min(min_score, score)
        return min_score

# human input

def human_input():
    move = int(input("Enter your move [1-9] : ")) - 1
    while move in X + O or move < 0 or move > 8:
        move = int(input("Invalid move!, Enter your move [1-9] : ")) - 1
    return move

# main

winner = 0

for turn in range(9):
    if turn % 2 == 0:
        X.append(human_input())
    else:
        O.append(mini_max_ai(O, X))

    displayBoard()

    if checkwin(X):
        winner = 1
        break
    elif checkwin(O):
        winner = -1
        break

if winner == 0:
    print("Draw")
elif winner == 1:
    print("X win!")
else:
    print("O win!")