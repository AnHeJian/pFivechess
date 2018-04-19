# coding: utf-8
import pygame
import sys
from pygame.locals import *

class Rule(object):
    def __init__(self):
        self.blist = [([0] * 16) for i in range(16)]
        self.wlist = [([0] * 16) for i in range(16)]
        self.gg = False
        self.new_bchess = self.new_wchess = (0, 0)

    def ListAppend(self, order, x, y):
        if order:
            self.blist[x][y] = 1
        else:
            self.wlist[x][y] = 1


    def GetBlist(self):
        return self.blist

    def SetBlist(self, list):
        self.blist = list

    def GetWlist(self):
        return self.wlist

    def SetWlist(self, list):
        self.wlist = list

    def GetGameState(self):
        return self.gg

    def GameOverdialog(self):
        dialog = pygame.display.set_mode((100, 60))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                pygame.display.flip()

    def IsGameOver(self, order, x, y):  # 判断是否连成五子
        list = self.blist if order else self.wlist

        for i in range(5):

            hb = 0 if x - i < 0 else x - i  # -----
            ht = 0
            for j in range(min(5, 16 - hb)):
                ht = ht + list[hb + j][y]
                if ht == 5:
                    self.gg = True
                    return True

            vb = 0 if y - i < 0 else y - i  # |||||
            vt = 0
            for j in range(min(5, 16 - vb)):
                vt = vt + list[x][vb + j]
                if vt == 5:
                    self.gg = True
                    return True

            # /////
            if x - i < 0 and y + i <= 15:
                r_bx = 0
                r_by = y + x
            elif y + i > 15 and  x - i >= 0:
                r_bx = x - (15 - y)
                r_by = 15
            elif x - i >= 0 and y + i <= 15:
                r_bx = x - i
                r_by = y + i

            rt = 0
            for j in range(min(5, r_by + 1, 16 - r_bx)):
                rt = rt + list[r_bx + j][r_by - j]
                if rt == 5:
                    self.gg = True
                    return True

            # \\\\\
            if x - i < 0:
                l_bx = 0
                l_by = y - x
            elif y - i < 0:
                l_bx = x - y
                l_by = 0
            else:
                l_bx = x - i
                l_by = y - i

            lt = 0
            for j in range(min(5, 16 - l_by, 16 - l_bx)):
                lt = lt + list[l_bx + j][l_by + j]
                if lt == 5:
                    self.gg = True
                    return True

