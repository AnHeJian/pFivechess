# coding: utf-8

FourBlack = 200
ThreeBlackNoW = 100
FourWhite = 250
ThreeWhiteNoB = 150

MAX_PIECE = 5
MAX_LINE = 16

max_score = 0
best_x = best_y = 0


def scoreOfFive(numOfBlack, numOfWhite, numOfEmpty):
    if numOfEmpty + numOfBlack + numOfWhite < 5:
        return 0
    if numOfBlack == 0:
        if numOfWhite == 1:
            return 15
        if numOfWhite == 2:
            return 400
        if numOfWhite == 3:
            return 1800
        if numOfWhite == 4:
            return 8000000

    elif numOfWhite == 0:
        if numOfBlack == 1:
            return 35
        if numOfBlack == 2:
            return 800
        if numOfBlack == 3:
            return 15000
        if numOfBlack == 4:
            return 1000000

    return 0


def calcuScore(x, y, mW, mB):
    scoreOfXY = 0
    numOfBlack = 0  # 五元组中黑棋数量
    numOfWhite = 0  # 五元组中白棋数量
    numOfEmpty = 0  # 五元组中空棋数量

    # 统计 “-----”方向
    for i in range(5):
        hb = 0 if x - i < 0 else x - i
        for j in range(min(5, 16 - hb)):
            if mW[hb + j][y] == 1:
                numOfWhite = numOfWhite + 1
            elif mB[hb + j][y] == 1:
                numOfBlack = numOfBlack + 1
            else:
                numOfEmpty = numOfEmpty + 1
        scoreOfXY = scoreOfXY + scoreOfFive(numOfBlack, numOfWhite, numOfEmpty)
        numOfBlack = numOfWhite = numOfEmpty = 0

    # 统计 “|”方向
    for i in range(5):
        vb = 0 if y - i < 0 else y - i
        for j in range(min(5, 16 - vb)):
            if mW[x][vb + j] == 1:
                numOfWhite = numOfWhite + 1
            elif mB[x][vb + j] == 1:
                numOfBlack = numOfBlack + 1
            else:
                numOfEmpty = numOfEmpty + 1
        scoreOfXY = scoreOfXY + scoreOfFive(numOfBlack, numOfWhite, numOfEmpty)
        numOfBlack = numOfWhite = numOfEmpty = 0

    # 统计 “/”方向
    for i in range(5):
        if x - i < 0 and y + i <= 15:
            r_bx = 0
            r_by = y + x
        elif y + i > 15 and x - i >= 0:
            r_bx = x - (15 - y)
            r_by = 15
        elif x - i >= 0 and y + i <= 15:
            r_bx = x - i
            r_by = y + i

        for j in range(min(5, r_by + 1, 16 - r_bx)):
            if mW[r_bx + j][r_by - j] == 1:
                numOfWhite = numOfWhite + 1
            elif mB[r_bx + j][r_by - j] == 1:
                numOfBlack = numOfBlack + 1
            else:
                numOfEmpty = numOfEmpty + 1
        scoreOfXY = scoreOfXY + scoreOfFive(numOfBlack, numOfWhite, numOfEmpty)
        numOfBlack = numOfWhite = numOfEmpty = 0

    # 统计 “\”方向
    for i in range(5):
        if x - i < 0:
            l_bx = 0
            l_by = y - x
        elif y - i < 0:
            l_bx = x - y
            l_by = 0
        else:
            l_bx = x - i
            l_by = y - i

        for j in range(min(5, 16 - l_by, 16 - l_bx)):
            if mW[l_bx + j][l_by + j] == 1:
                numOfWhite = numOfWhite + 1
            elif mB[l_bx + j][l_by + j] == 1:
                numOfBlack = numOfBlack + 1
            else:
                numOfEmpty = numOfEmpty + 1
        scoreOfXY = scoreOfXY + scoreOfFive(numOfBlack, numOfWhite, numOfEmpty)
        numOfBlack = numOfWhite = numOfEmpty = 0

    return scoreOfXY


def calcuMaxPoint(mW, mB):
    max_score = score = best_x = best_y = 0
    for i in range(MAX_LINE):
        for j in range(MAX_LINE):
            if mW[i][j] != 1 and mB[i][j] != 1:
                score = calcuScore(i, j, mW, mB)
                if score > max_score:
                    best_x = i
                    best_y = j
                    max_score = score

    print max_score
    return best_x, best_y, max_score