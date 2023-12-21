import pygame
import sys 
import random
import numpy as np
import time
pygame.init()


# block_size = 32
# SW, SH = 30*block_size,16*block_size


# FONT = pygame.font.Font(None, block_size)

# screen = pygame.display.set_mode((SW, SH))
# pygame.display.set_caption("Minesweeper!")
# clock = pygame.time.Clock()

class minesweeper():
    def __init__(self,wid,height,mines):
        self.block_size = 40
    
        self.board_height = height
        self.board_wid = wid
        self.num_mines = mines
        self.SW, self.SH = self.board_wid*self.block_size, self.board_height*self.block_size

        self.board = np.zeros((self.board_height, self.board_wid), dtype=int)
        self.show_board = np.zeros((self.board_height, self.board_wid), dtype=int)
        self.blanks = (self.board_height*self.board_wid)-self.num_mines
        self.action_space =  np.zeros((self.board_height, self.board_wid), dtype=object)
        for y in range(self.board_height):
            for x in range(self.board_wid):
                self.action_space[y,x] = (y,x)
        
        
        self.screen = pygame.display.set_mode((self.SW, self.SH))
        self.ms1 = pygame.image.load('ms1.png')
        self.ms2 = pygame.image.load('ms2.png')
        self.ms3 = pygame.image.load('ms3.png')
        self.ms4 = pygame.image.load('ms4.png')
        self.ms5 = pygame.image.load('ms5.png')
        self.ms6 = pygame.image.load('ms6.png')
        self.msmine = pygame.image.load('msmine.png')
        self.msflag = pygame.image.load('msflag.png')
        self.font = pygame.font.Font(None, self.block_size)
        pygame.display.set_caption("Minesweeper!")
        self.clock = pygame.time.Clock()

    def reset(self):
        self.screen = pygame.display.set_mode((self.SW, self.SH))
        self.blanks = (self.board_height*self.board_wid)-self.num_mines

        #adds the mines to the empty board
        num_squares = self.board_height * self.board_wid
        mines = self.num_mines
        for y in range(self.board_wid):
            for x in range(self.board_height):
                if random.random() < (mines/num_squares):
                    self.board[x,y] = 9
                    mines = mines - 1
                else:
                    self.board[x,y] = 0
                num_squares = num_squares - 1

        #adds the number sqaures around the mines
        for y in range(self.board_wid):
            for x in range(self.board_height):

                if self.board[x,y] == 9:
                    if x>=1 and y>=1: 
                        if self.board[x-1,y-1] != 9:
                            self.board[x-1,y-1] += 1
                    if y>=1:
                        if self.board[x,y-1] != 9:
                            self.board[x,y-1] += 1
                    if x<self.board_height-1 and y>=1:
                        if self.board[x+1,y-1] != 9:
                            self.board[x+1,y-1] += 1
                    if x<self.board_height-1:
                        if self.board[x+1,y] != 9:
                            self.board[x+1,y] += 1
                    if x<self.board_height-1 and y<self.board_wid-1:
                        if self.board[x+1,y+1] != 9:
                            self.board[x+1,y+1] += 1
                    if y<self.board_wid-1:
                        if self.board[x,y+1] != 9:
                            self.board[x,y+1] += 1
                    if x>=1 and y<self.board_wid-1:
                        if self.board[x-1,y+1] != 9:
                            self.board[x-1,y+1] += 1
                    if x>=1:
                        if self.board[x-1,y] != 9:
                            self.board[x-1,y] += 1

        #makes the show_board "-1"'s
        for y in range(self.board_height):
            for x in range(self.board_wid):
                self.show_board[y,x] = -1
        self.show()

    def flag(self,x,y):
        if self.show_board[y,x] == -1:
            self.show_board[y,x] = 10
        elif self.show_board[y,x] == 10:
            self.show_board[y,x] = -1
        self.show()

    def chord(self,x,y):
        nearby = [(1,1),(1,0),(1,-1),(0,1),(-1,1),(-1,-1),(-1,0),(0,-1)]
        mine_counter = 0
        for i in nearby:
            x1 = x+ i[0]
            y1 = y+ i[1]
            if 0 <= x1 <self.board_wid and 0 <= y1 < self.board_height:
                if self.show_board[y1,x1] == 10:
                    mine_counter+=1
        
        if mine_counter == self.board[y,x]:
            for i in nearby:
                x1 = x+ i[0]
                y1 = y+ i[1]
                if 0 <= x1 <self.board_wid and 0 <= y1 < self.board_height:
                    if self.show_board[y1,x1] != 10:
                        if self.board[y1,x1] == 9:
                            self.reset()
                            print("Game Over!")
                        else:
                            self.find_zeros(x1,y1)

    def step(self,x,y):
        if self.show_board[y,x] != 10:
            if x not in range(self.board_wid) and y not in range(self.board_height):
                return "Not a possible input"

            reward = self.blanks
            terminated = bool(self.board[y,x] == 9)
            self.find_zeros(x,y)
            if not terminated:
                reward += -self.blanks
                counter = 0
                for val in np.nditer(self.show_board):
                    if val == -1 or val == 10:
                        counter += 1
                if counter == self.num_mines:
                    print("You Win!")
                    game.reset()
            else:
                reward = 0
                self.reset()
                print("Game Over!")
            
            self.show()

    def find_zeros(self,x,y):
        cs = [[x,y]]
        rq = [[x,y]]
        while len(cs) > 0:
            if self.show_board[cs[0][1],cs[0][0]] == -1:
                self.blanks += -1
            if self.board[cs[0][1],cs[0][0]] == 0:
                cs.append([cs[0][0]-1,cs[0][1]])
                cs.append([cs[0][0]+1,cs[0][1]])
                cs.append([cs[0][0],cs[0][1]-1])
                cs.append([cs[0][0],cs[0][1]+1])
                cs.append([cs[0][0]+1,cs[0][1]+1])
                cs.append([cs[0][0]-1,cs[0][1]-1])
                cs.append([cs[0][0]-1,cs[0][1]+1])
                cs.append([cs[0][0]+1,cs[0][1]-1])
            self.show_board[cs[0][1],cs[0][0]] = self.board[cs[0][1],cs[0][0]]
            remove_me = []
            res = []
            rq.append([cs[0][0],cs[0][1]])
            for d in cs:
                if d in rq:
                    remove_me.append(d)
                if d[0] == -1 or d[0]>=self.board.shape[1]:
                    remove_me.append(d)
                if d[1] == -1 or d[1]>=self.board.shape[0]:
                    remove_me.append(d)
            for i in remove_me:
                if i not in res:
                    res.append(i)
            for r in res:
                cs.remove(r)

    def show(self):
        for x in range(0, self.SW, self.block_size):
            for y in range(0, self.SH, self.block_size):
                rect = pygame.Rect(x, y, self.block_size-1, self.block_size-1)
                p = self.show_board[int(y/self.block_size),int(x/self.block_size)]
                if p == -1: # unknown
                    pygame.draw.rect(self.screen, "#808080", rect)
                elif p == 0: #blank
                    pygame.draw.rect(self.screen, "#c6c6c6", rect)
                elif p == 1:
                    self.screen.blit(self.ms1, (x+1,y+1))
                elif p == 2:
                    self.screen.blit(self.ms2, (x+1,y+1))
                elif p == 3:
                    self.screen.blit(self.ms3, (x+1,y+1))
                elif p == 4:
                    self.screen.blit(self.ms4, (x+1,y+1))
                elif p == 5:
                    self.screen.blit(self.ms5, (x+1,y+1))
                elif p == 6:
                    self.screen.blit(self.ms6, (x+1,y+1))
                elif p == 7:
                    pygame.draw.rect(self.screen, "#000000", rect)
                elif p == 8:
                    pygame.draw.rect(self.screen, "#888080", rect)
                elif p == 9: #mine
                    self.screen.blit(self.msmine, (x+1,y+1))
                elif p == 10: #flag
                    self.screen.blit(self.msflag, (x+1,y+1))

    def play(self):
        left = 1
        right = 3
        right_click_timer = time.time()
        down_time = time.time()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                mouse = pygame.mouse.get_pos()
                self.step(mouse[0] // self.block_size, mouse[1] // self.block_size)
                

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == right:
                if (time.time() - right_click_timer) > .1:
                    mouse = pygame.mouse.get_pos()
                    self.flag(mouse[0] // self.block_size, mouse[1] // self.block_size)
                    right_click_timer = time.time()
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                if .04 < time.time() - down_time < .25:
                    self.chord(mouse[0] // self.block_size, mouse[1] // self.block_size)
                down_time = time.time()
            pygame.display.update()






clock = pygame.time.Clock()
game = minesweeper(12,7,15)
game.reset()
game.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    rand = random.randint(0,479)
    rand_x = rand%30
    rand_y = rand//30
    game.step(rand_x, rand_y)
    pygame.display.update()
    clock.tick(30)

