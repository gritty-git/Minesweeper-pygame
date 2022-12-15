import pygame
import random
import math
import numpy as np
import time

#Initialize array
flagged = np.zeros(16)
opened = np.zeros((4,4))
#Initialize the pygame
pygame.init()

#global Variables
runn = 0
first = True
mines = np.zeros((4,4))
ctrr = 0
go = False
openctr = 0

#colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

dull_red = (200,0,0)
dull_green=(0,200,0)


#Create Screen
screen = pygame.display.set_mode((600,710))
background = pygame.image.load('background.png')
ibg = pygame.image.load('ibg.png')
flag = pygame.image.load('flag.png')
mine = pygame.image.load('mine.png')
restart = pygame.image.load('restart.png')

#Title and icon
pygame.display.set_caption("MineSweeper")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#GO text
over_font = pygame.font.SysFont(("comicsansms"),64)


clock = pygame.time.Clock()

#Functions
def counter(blk):
    no = 0
    l = blk % 4
    b = int(int(blk) / int(4))
    for i in range(4):
        for j in range(4):
            if(i!=l or j!=b) and ((abs(i-l)<2) and (abs(j-b)<2)):
                if mines[i,j]==1:
                    no = no + 1
    return no
##mines[1,1]=1
##mines[1,0] = 1
##mines[0,1] = 1
##print(counter(0))

def mapper(x,y):
    blk = 0
    it = False
    for i in range(4):
        for j in range(4):
            if(60+120*j<x<60+120*(j+1)) and (30+120*i<y<30+120*(i+1)):
                it = True
                break
                
            else:
                blk = blk+1
        if it == True:
            break
    return blk
def inv_map(blk):
    l = blk % 4
    b = int(int(blk) / int(4))
    x = 60 + 120 * l
    y = 30 + 120 * b
    return x,y
#print(inv_map(9))
    
#print(mapper(360,240))
def text_objects(text, font):
    textSurface = font.render(text, True, [0,0,0])
    return textSurface, textSurface.get_rect()

def one_to_two(blk):
    l = blk % 4
    b = int(int(blk) / int(4))
    return(l,b)
#print(one_to_two(5))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,red)
    screen.blit(over_text,(100,250))

def victory_text():
    over_text = over_font.render("VICTORY",True,blue)
    screen.blit(over_text,(100,250))
    
def button(msg,x,y,w,h,ic,ac,action = None):
            global runn
            global first
            global ctrr
            global opened
            global go
            global openctr
 
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed() 

            if x+w>mouse[0]>x and y+h>mouse[1]>y :
                pygame.draw.rect(screen, ac, (x,y,w,h))
                if click[0] == 1 and action != None:
                    if action == "play":
                        runn = 1
                        time.sleep(0.1)
                    elif action == "quit":
                        pygame.quit()
                        quit()
                        time.sleep(0.1)
                    elif action == "click":
                        if first == True:
                            #print("open total 3 block")
                            blk = mapper(mouse[0],mouse[1])
                            opened[one_to_two(blk)] = 1
                            openctr = openctr+1
                            #print(blk)
                            ctrr = 0
                            while True: 
                                a = random.randrange(0, 16, 1)
                                if (a!=blk) and (mines[one_to_two(a)] != 1):
                                    print(a,one_to_two(a))
                                    mines[one_to_two(a)] = 1
                                    ctrr = ctrr+1
                                    
                                if ctrr ==3:
                                    break
                            l = blk % 4
                            b = int(int(blk) / int(4))
                            print(l,b)
                            ctrrr = 0
                            for i in range(4):
                                for j in range(4):
                                    if(i!=l or j!=b) and ((abs(i-l)<2) and (abs(j-b)<2)) and (ctrrr<2) and (mines[i,j]==0):
                                        opened[i,j] = 1
                                        openctr = openctr+1
                                        ctrrr =ctrrr+1
                            first = False
                            print(mines)
                            print(opened)
                            
                        else:
                            blk = mapper(mouse[0],mouse[1])
                            print(blk)
                            if (mines[one_to_two(blk)] == 1):
                                
                                go = True
                                print(mines)
                                print(opened)
                            else:
                                opened[one_to_two(blk)] = 1
                                openctr = openctr+1
                                print(mines)
                                print(opened)
                            #print("check if block contains mine then display gameover else open the box")
                        time.sleep(0.1)

                        
                elif click[2] == 1 and action != None:
                    if action == "click":
                        blk = mapper(mouse[0],mouse[1])
                        #print(blk)
                        if flagged[blk] != 1:
                            flagged[blk] = 1
                        else:
                            flagged[blk] = 0
                        time.sleep(0.1)
                        
                        
                    
                #print("heija")
            else:
                pygame.draw.rect(screen, ic, (x,y,w,h))
            smallText = pygame.font.SysFont(("comicsansms"),20)
            textSurf, textRect = text_objects(msg, smallText)
            textRect.center = ((x + (w/2)),(y + (h/2)))
            screen.blit(textSurf,textRect)

def game_intro():
    
    global runn
    intro = True
    
    while intro:
        screen.blit(ibg, (0,0))
        p = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #screen.fill([255,255,255])
        intro_font = pygame.font.SysFont(("comicsansms"),80)
        TextSurf, TextRect = text_objects("Minesweeper",intro_font)
        TextRect.center = ((300),(355))
        screen.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,dull_green,"play")
        button("Quit!",350,450,100,50,red,dull_red,"quit")
        if runn == 1:
            intro = False
                
        pygame.display.update()

def display_flag(x,y):
    screen.blit(flag,(x,y))
#Game Loop
def gameloop():
    global openctr
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0,0))
        screen.blit(restart,(236,560))
        for j in range(4):
            for i in range (4):
                button("",60 + 120*(i),30 + 120*(j),120,120,[100,100,100],[180,180,180],"click")
                if opened[i,j] == 1:
                    pygame.draw.rect(screen,(200,200,200),(60 + 120*(i),30 + 120*(j),120,120))
                    smallText = pygame.font.SysFont(("comicsansms"),20)
                    textSurf, textRect = text_objects(str(counter(j*4 + i)), smallText)
                    textRect.center = ((60 + 120*(i) + (120/2)),(30 + 120*(j) + (120/2)))
                    screen.blit(textSurf,textRect)



        for ii in range(5):
            pygame.draw.line(screen, (0, 0, 0), (60 + 120*(ii), 30), (60 + 120*(ii), 510), 3)
        for ij in range(5):
            pygame.draw.line(screen, (0, 0, 0), (60, 30 + 120*(ij)), (540, 30 + 120*(ij)), 3)
        
        for ib in range(16):
            if flagged[ib]==1:
                x,y = inv_map(ib)
                screen.blit(flag,(x,y))
                #print(flagged)
                
        if (go == True) and (openctr < 13):
            for j in range(4):
                for i in range(4):
                    if mines[i,j] == 1:
                        screen.blit(mine,(60 + 120*(i),30 + 120*(j)))
            game_over_text()
        if (openctr >= 13) and (go == False):
            
            for j in range(4):
                for i in range(4):
                    if mines[i,j] == 1:
                        screen.blit(mine,(60 + 120*(i),30 + 120*(j)))
            victory_text()
            
        pygame.display.update()

game_intro()
gameloop()
pygame.quit()
quit()
