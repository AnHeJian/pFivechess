#! python2
# coding: utf-8
import os
import numpy
import time

from rule import *
import computer

pygame.init()  # 初始化

length = 800
height = 600
screen = pygame.display.set_mode((length, height))  # 屏幕对象
pygame.display.set_caption('FiveChess')
pygame.display.set_gamma(1)
#pygame.display.set_icon(pygame.image.load('res' + os.sep + 'icon.png').convert_alpha())


class Panel(object): 
    def __init__(self, panellength, chesslength):
        self.panellength = panellength
        self.chesslength = chesslength
        self.inteval = self.panellength / 16

        self.order = True  # True:Black    False:White
        blackchess = pygame.image.load('res' + os.sep + 'black.png').convert_alpha()
        self.blackchess = pygame.transform.smoothscale(blackchess, (chesslength, chesslength))

        whitechess = pygame.image.load('res' + os.sep + 'white.png').convert_alpha()
        self.whitechess = pygame.transform.smoothscale(whitechess, (chesslength, chesslength))

        newblackchess = pygame.image.load('res' + os.sep + 'blacknew.png').convert_alpha()
        self.newblackchess = pygame.transform.smoothscale(newblackchess, (chesslength, chesslength))

        newwhitechess = pygame.image.load('res' + os.sep + 'whitenew.png').convert_alpha()
        self.newwhitechess = pygame.transform.smoothscale(newwhitechess, (chesslength, chesslength))

        self.lx = length / 2 - panellength / 2
        self.rx = length / 2 + panellength / 2 - chesslength
        self.uy = height / 2 - panellength / 2
        self.dy = height / 2 + panellength / 2 - chesslength

    def Background(self):
        bg = pygame.image.load('res' + os.sep + 'bg.jpg').convert()
        bgsurf = pygame.Surface((1440, 1080))
        bgsurf.blit(bg, (0, 0))
        bgsurf = pygame.transform.smoothscale(bgsurf, (length, height))
        screen.blit(bgsurf, (0, 0))

    def ChessPanel(self):
        panellength = self.panellength
        inteval = self.inteval
        surf = pygame.Surface((panellength, panellength))  # 长宽
        surf.fill((136, 210, 174))  # 颜色，默认为黑色
        #surf.set_alpha(183)  # 设置透明色
        # 画线
        linecolor = (0, 0, 0)
        for i in range(16):
            pygame.draw.line(surf, linecolor, (inteval / 2, inteval / 2 + i * inteval),
                             (panellength - inteval / 2, inteval / 2 + i * inteval))
            pygame.draw.line(surf, linecolor, (inteval / 2 + i * inteval, inteval / 2),
                             (inteval / 2 + i * inteval, panellength - inteval / 2))

        screen.blit(surf, (length / 2 - panellength / 2, height / 2 - panellength / 2))
        return surf

    def UpdatePanel(self):
        pygame.display.update(
            pygame.Rect(length / 2 - panellength / 2, height / 2 - panellength / 2, panellength, panellength))

    def UpdateAllChess(self):
        pygame.display.init()
        chesslength = self.chesslength
        panellength = self.panellength
        screen.blit(self.ChessPanel(), (length / 2 - panellength / 2, height / 2 - panellength / 2))

        inteval = self.inteval
        for i in range(16):
            for j in range(16):
                px = (2 * i + 1) * (inteval / 2) - chesslength / 2 + self.lx
                py = (2 * j + 1) * (inteval / 2) - chesslength / 2 + self.uy
                if rule.GetBlist()[i][j] != 0:
                    screen.blit(self.blackchess, (px, py))
                if rule.GetWlist()[i][j] != 0:
                    screen.blit(self.whitechess, (px, py))
        self.UpdatePanel()

    def DrawChess(self, i, j):
        lx = self.lx
        rx = self.rx
        uy = self.uy
        dy = self.dy
        chesslength = self.chesslength
        inteval = self.inteval

        '''vx = x - chesslength / 2
        vy = y - chesslength / 2

        if lx <= vx <= rx and uy <= vy <= dy:
            i = ((x - lx) / inteval)
            j = ((y - uy) / inteval)'''

        if i != -1 and j != -1:
            if rule.GetWlist()[i][j] != 1 and rule.GetBlist()[i][j] != 1:
                self.UpdateAllChess()

                px = (2 * i + 1) * (inteval / 2) - chesslength / 2 + lx
                py = (2 * j + 1) * (inteval / 2) - chesslength / 2 + uy

                screen.blit(self.newblackchess, (px, py)) if self.order else screen.blit(self.newwhitechess, (px, py))
                pygame.display.update(pygame.Rect(px, py, chesslength, chesslength))

                rule.ListAppend(self.order, i, j)
                if self.order:
                    rule.new_bchess = (i, j)
                else:
                    rule.new_wchess = (i, j)

                if rule.IsGameOver(self.order, i, j):
                    print ('Black' if self.order else 'White') + 'Win'

                self.order = not self.order

    def RestartIcon(self, x, y):
        restart_icon = 'restart_active.png' if 657 <= x <= 702 and 268 <= y < 300 else 'restart.png'
        restart_bot = pygame.image.load('res' + os.sep + restart_icon).convert_alpha()
        restart_bot = pygame.transform.smoothscale(restart_bot, (45, 40))
        screen.blit(restart_bot, (656, 267))
        pygame.display.update(pygame.Rect(656, 267, 45, 40))

    def UndoIcon(self, x, y):
        undo_icon = 'undo_active.png' if 657 <= x <= 702 and 330 < y <= 365 else 'undo.png'
        undo_bot = pygame.image.load('res' + os.sep + undo_icon).convert_alpha()
        undo_bot = pygame.transform.smoothscale(undo_bot, (45, 36))
        screen.blit(undo_bot, (656, 327))
        pygame.display.update(pygame.Rect(656, 327, 45, 36))

    def Restart(self):
        rule.SetBlist(numpy.zeros((16, 16)))
        rule.SetWlist(numpy.zeros((16, 16)))
        self.UpdateAllChess()
        rule.gg = False
        self.order = True

    def Undo(self):
        rule.blist[rule.new_bchess[0]][rule.new_bchess[1]] = 0
        rule.wlist[rule.new_wchess[0]][rule.new_wchess[1]] = 0
        self.UpdateAllChess()

    def TransLoc(self, x, y):
        lx = self.lx
        rx = self.rx
        uy = self.uy
        dy = self.dy
        chesslength = self.chesslength
        inteval = self.inteval

        vx = x - chesslength / 2
        vy = y - chesslength / 2

        if lx <= vx <= rx and uy <= vy <= dy:
            i = ((x - lx) / inteval)
            j = ((y - uy) / inteval)
            return i, j
        else:
            return -1, -1


panellength = 384
chesslength = 16
panel = Panel(panellength, chesslength)
panel.Background()
panel.ChessPanel()
pygame.display.update()

rule = Rule()

panel.DrawChess(8, 8)
while not rule.GetGameState():
    a, b, ms = computer.calcuMaxPoint(rule.wlist, rule.blist)
    if(ms==0):
        print "平局"
        break
    else:
        panel.DrawChess(a, b)
        #time.sleep(1)

while True:
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


# while True:
#     for event in pygame.event.get():
#         x, y = pygame.mouse.get_pos()
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#
#         elif event.type == MOUSEBUTTONDOWN:
#             if 657 <= x <= 702 and 268 <= y < 300:
#                 panel.Restart()
#
#             elif 657 <= x <= 702 and 330 < y <= 365:
#                 panel.Undo()
#
#             elif not rule.GetGameState():
#                 a, b = panel.TransLoc(x, y)#玩家（黑棋落子）
#                 panel.DrawChess(a, b)
#
#                 # if not panel.order:
#                 #     a, b = computer.calcuMaxPoint(rule.wlist, rule.blist)#AI（白棋）落子
#                 #     panel.DrawChess(a, b)
#
#
#
#         panel.RestartIcon(x, y)
#         panel.UndoIcon(x, y)
#         # 更新界面
#         #pygame.display.update()
