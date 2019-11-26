import copy
import random

class board(object):
    def __init__(self, cells = None, initturn = 1):
        # 0: None, 1: Black, -1: White
        BLACK    = '\033[30m'
        WHITE    = '\033[37m'
        BG_BLACK = '\033[40m'
        BG_WHITE = '\033[47m'
        BOLD     = '\033[1m'
        RESET    = '\033[0m'
        BLINK    = '\033[5m'
        self.__STONE = (
            ('   ', ' B ', ' W '),
            ('   ', WHITE+BG_BLACK+' B '+RESET, BLACK+BG_WHITE+' W '+RESET),
            ('   ', BLINK+WHITE+BG_BLACK+' B '+RESET, BLINK+BLACK+BG_WHITE+' W '+RESET)
        )
        if cells is None:
            self.__cells = [[None for i in range(10)]]\
            + [[None]+[0 for j in range(8)]+[None] for i in range(8)]\
            + [[None for i in range(10)]]
            self.__cells[4][4:6] = [-1, 1]
            self.__cells[5][4:6] = [ 1,-1]
        else:
            self.__cells = cells
        self.__turn = initturn
        self.__count = 0
        self.__direction = (
            (-1,-1), (-1, 0), (-1,+1),
            ( 0,-1),          ( 0,+1),
            (+1,-1), (+1, 0), (+1,+1)
        )
        """
        self.__gain = (
            ( 0,   0,   0,  0,  0,  0,  0,   0,   0,   0),
            ( 0,  45, -11,  4, -1, -1,  4, -11,  45,   0),
            ( 0, -11, -16, -1, -3, -3, -1, -16, -11,   0),
            ( 0,   4,  -1,  2, -1, -1,  2,  -1,   4,   0),
            ( 0,  -1,  -3, -1,  0,  0, -1,  -3,  -1,   0),
            ( 0,  -1,  -3, -1,  0,  0, -1,  -3,  -1,   0),
            ( 0,   4,  -1,  2, -1, -1,  2,  -1,   4,   0),
            ( 0, -11, -16, -1, -3, -3, -1, -16, -11,   0),
            ( 0,  45, -11,  4, -1, -1,  4, -11,  45,   0),
            ( 0,   0,   0,  0,  0,  0,  0,   0,   0,   0)
        )"""
        self.__gain = (
            ( 0,   0,   0,  0,  0,  0,  0,   0,   0,   0),
            ( 0,  30, -12,  0, -1, -1,  0, -12,  30,   0),
            ( 0, -12, -15, -3, -3, -3, -3, -15, -12,   0),
            ( 0,   0,  -3,  0, -1, -1,  0,  -3,   0,   0),
            ( 0,  -1,  -3, -1, -1, -1, -1,  -3,  -1,   0),
            ( 0,  -1,  -3, -1, -1, -1, -1,  -3,  -1,   0),
            ( 0,   0,  -3,  0, -1, -1,  0,  -3,   0,   0),
            ( 0, -12, -15, -3, -3, -3, -3, -15, -12,   0),
            ( 0,  30, -12,  0, -1, -1,  0, -12,  30,   0),
            ( 0,   0,   0,  0,  0,  0,  0,   0,   0,   0)
        )
        self.__passcount = 0
        self.__log = []

    def numstone(self):
        return sum(x == 1 or x == -1 for row in self.__cells for x in row)

    def numblack(self):
        return sum(x == 1 for row in self.__cells for x in row)

    def numwhite(self):
        return sum(x == -1 for row in self.__cells for x in row)

    def score(self):
        result = 0
        for i in range(1,9):
            result += sum(self.__cells[i][1:9])
        return result

    def __countreversible(self, row, col, dirid):
        if self.__cells[row][col] == self.__turn:
            return 0
        elif self.__cells[row][col] == self.__turn*(-1):
            return 1 + self.__countreversible(row + self.__direction[dirid][0],
                                              col + self.__direction[dirid][1],
                                              dirid)
        else:
            # out of board
            return -8

    def countreversibles(self, row, col):
        if self.__cells[row][col] is None:
            return 0
        elif self.__cells[row][col] == 0:
            numrev = 0
            for i in range(8):
                tmp = self.__countreversible(row+self.__direction[i][0], col+self.__direction[i][1], i)
                if tmp < 0:
                    tmp = 0
                numrev += tmp
            return numrev
        else:
            return 0

    def findavailable(self):
        available = []
        for row in range(1,9):
            for col in range(1,9):
                if self.countreversibles(row, col) > 0:
                    available.append((row,col))
        return available

    def __reverse(self, row, col):
        for i in range(8):
            numrev = self.__countreversible(row+self.__direction[i][0], col+self.__direction[i][1], i)
            if numrev > 0:
                for j in range(1,numrev+1):
                    self.__cells[row+self.__direction[i][0]*j][col+self.__direction[i][1]*j] *= -1

    def upass(self):
        # pass
        if len(self.findavailable()) == 0:
            self.__turn *= -1
            self.__count += 1
            self.__passcount += 1
        else:
            raise CanNotPassError()

    def put(self, row, col):
        if row < 1 or row > 8 or col < 1 or col > 8:
            # out of board
            raise CanNotPutStoneError()
        available = self.findavailable()
        if len(available) == 0:
            # cannot put the stone anywhere
            self.__turn *= -1
            self.__count += 1
            self.__passcount += 1
        elif (row, col) in available:
            self.__log.append((self.__turn, row, col))
            self.__reverse(row,col)
            self.__cells[row][col] = self.__turn
            self.__turn *= -1
            self.__count += 1
            self.__passcount = 0
        else:
            raise CanNotPutStoneError()

    def winner(self):
        if not self.goeson():
            win = self.score()
            if win > 0:
                return 1
            elif win < 0:
                return -1
            else:
                return 0

    def goeson(self):
        if self.numstone() == 64:
            return False
        elif self.numblack() == 0:
            return False
        elif self.numwhite() == 0:
            return False
        elif self.__passcount == 2:
            return False
        else:
            return True

    def show(self):
        print("="*36)
        print("Turn Count:", self.__count)
        print("Turn:", self.__STONE[1][self.__turn])
        print("="*36)
        print("     1   2   3   4   5   6   7   8  ")
        for i in range(1,9):
            print("   "+"+---"*8+'+')
            print(" "+str(i)+" |", end='')
            for j in range(1,9):
                if len(self.__log) != 0 and i == self.__log[-1][1] and j == self.__log[-1][2]:
                    print(self.__STONE[2][self.__cells[i][j]], end = '|')
                else:
                    print(self.__STONE[1][self.__cells[i][j]], end = '|')
            print('')
        print("   "+"+---"*8+'+')

    def getcells(self):
        return [[self.__cells[i][j] for j in range(1,9)] for i in range(1,9)]

    def getrawcells(self):
        return copy.deepcopy(self.__cells)

    def turn(self):
        return self.__turn

    def getlog(self):
        return copy.deepcopy(self.__log)

    def count(self):
        return self.__count

    def passcount(self):
        return self.__passcount

    def calcscore(self, player):
        return player*sum([self.__gain[row][col]*self.__cells[row][col] for row in range(1,9) for col in range(1,9)])

class game(board):
    def __init__(self, cells=None, initturn=1):
        super().__init__(cells, initturn)

    def minmax(self):
        evalboard = board(self.getrawcells(), self.turn())
        return self.__evalminmax(evalboard, 0)

    def __evalminmax(self, evalboard, depth):
        if depth == 2:
            available = evalboard.findavailable()
            random.shuffle(available)
            if len(available) != 0:
                branch = [board(evalboard.getrawcells(), evalboard.turn()) for i in range(len(available))]
                scores = [0 for i in range(len(available))]
                for i, d in enumerate(available):
                    branch[i].put(d[0],d[1])
                    scores[i] = branch[i].calcscore(-branch[i].turn())
                return max(scores)
            else:
                evalboard.upass()
                return evalboard.calcscore(-evalboard.turn())
        elif depth == 1:
            available = evalboard.findavailable()
            random.shuffle(available)
            if len(available) != 0:
                branch = [board(evalboard.getrawcells(), evalboard.turn()) for i in range(len(available))]
                scores = [0 for i in range(len(available))]
                for i, d in enumerate(available):
                    branch[i].put(d[0],d[1])
                    scores[i] = self.__evalminmax(branch[i], 2)
                return min(scores)
            else:
                evalboard.upass()
                return self.__evalminmax(evalboard, 2)
        else:
            available = evalboard.findavailable()
            random.shuffle(available)
            branch = [board(evalboard.getrawcells(), evalboard.turn()) for i in range(len(available))]
            scores = [0 for i in range(len(available))]
            for i, d in enumerate(available):
                branch[i].put(d[0],d[1])
                scores[i] = self.__evalminmax(branch[i], 1)
            idx = scores.index(max(scores))
            return available[idx], scores[idx]


    def alphabeta(self):
        return self.__evalab()

    def __evalab(self):
        # max
        available = self.findavailable()
        random.shuffle(available)
        branch1 = [board(self.getrawcells(), self.turn()) for i in range(len(available))]
        scores = [0 for i in range(len(available))]
        minscore = -3000
        for i, d in enumerate(available):
            branch1[i].put(d[0],d[1])
            scores[i] = self.__evalab2(branch1[i], minscore)
            if i == 0:
                minscore = scores[i]
        idx = scores.index(max(scores))
        return available[idx], scores[idx]

    def __evalab2(self, evalboard, minscore):
        # min
        available = evalboard.findavailable()
        random.shuffle(available)
        if len(available) != 0:
            branch2 = [board(evalboard.getrawcells(), evalboard.turn()) for i in range(len(available))]
            scores = [0 for i in range(len(available))]
            maxscore = 3000
            for i, d in enumerate(available):
                branch2[i].put(d[0],d[1])
                scores[i] = self.__evalab3(branch2[i], maxscore)
                if i == 0:
                    maxscore = scores[i]
                if scores[i] <= minscore:
                    return scores[i]
            return min(scores)
        else:
            evalboard.upass()
            score = self.__evalab3(evalboard, 3000)
            return score

    def __evalab3(self, evalboard, maxscore):
        # max
        available = evalboard.findavailable()
        random.shuffle(available)
        if len(available) != 0:
            branch3 = [board(evalboard.getrawcells(), evalboard.turn()) for i in range(len(available))]
            scores = [0 for i in range(len(available))]
            for i, d in enumerate(available):
                branch3[i].put(d[0],d[1])
                scores[i] = branch3[i].calcscore(-branch3[i].turn())
                if scores[i] >= maxscore:
                    return scores[i]
            return max(scores)
        else:
            evalboard.upass()
            return evalboard.calcscore(-evalboard.turn())

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class CanNotPutStoneError(Error):
    def __init__(self):
        self.msg = "Can not put the stone."

class CanNotPassError(Error):
    def __init__(self):
        self.msg = "Can not pass."
