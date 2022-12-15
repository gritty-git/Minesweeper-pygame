import pygame
import random
import math
import numpy as np
import time

grid_size = 8
blk_no = 64
mine_no = 10
pre = 10
#Initialize array
flagged = np.zeros(blk_no)
opened = np.zeros((grid_size,grid_size))
#Initialize the pygame
pygame.init()

#global Variables
blk_size = 60
runn = 0
first = True
mines = np.zeros((grid_size,grid_size))
ctrr = 0
go = False
openctr = 0
restart = False

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
flag = pygame.image.load('flag8.png')
mine = pygame.image.load('mine8.png')
restarti = pygame.image.load('restart.png')

#Title and icon
pygame.display.set_caption("MineSweeper")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#GO text
over_font = pygame.font.SysFont(("comicsansms"),64)


clock = pygame.time.Clock()

#Functions
def counter(blk):
    global grid_size
    no = 0
    l = blk % grid_size
    b = int(int(blk) / int(grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if(i!=l or j!=b) and ((abs(i-l)<2) and (abs(j-b)<2)):
                if mines[i,j]==1:
                    no = no + 1
    return no
##mines[1,1]=1
##mines[1,0] = 1
##mines[0,1] = 1
##print(counter(0))

def mapper(x,y):
    global grid_size
    global blk_size
    blk = 0
    it = False
    for i in range(grid_size):
        for j in range(grid_size):
            if(60+blk_size*j<x<60+blk_size*(j+1)) and (30+blk_size*i<y<30+blk_size*(i+1)):
                it = True
                break
                
            else:
                blk = blk+1
        if it == True:
            break
    return blk
def inv_map(blk):
    global blk_size
    global grid_size
    l = blk % grid_size
    b = int(int(blk) / int(grid_size))
    x = 60 + blk_size * l
    y = 30 + blk_size * b
    return x,y
#print(inv_map(9))
    
#print(mapper(360,240))
def text_objects(text, font):
    textSurface = font.render(text, True, [0,0,0])
    return textSurface, textSurface.get_rect()

def one_to_two(blk):
    global grid_size
    l = blk % grid_size
    b = int(int(blk) / int(grid_size))
    return(l,b)
#print(one_to_two(5))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,red)
    screen.blit(over_text,(100,250))

def victory_text():
    over_text = over_font.render("VICTORY",True,blue)
    screen.blit(over_text,(140,250))
    
def button(msg,x,y,w,h,ic,ac,action = None):
            global blk_size
            global grid_size
            global runn
            global first
            global ctrr
            global opened
            global go
            global openctr
            global restart
            global flagged
            global mines
            global mine_no
            global pre
 
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed() 

            if x+w>mouse[0]>x and y+h>mouse[1]>y :
                pygame.draw.rect(screen, ac, (x,y,w,h))
                if click[0] == 1 and action != None:
                    if action == "play":
                        runn = 1
                        time.sleep(0.1)
                    elif action == "restart":
                        restart = True
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
                                a = random.randrange(0, blk_no, 1)
                                if (a!=blk) and (mines[one_to_two(a)] != 1):
                                    print(a,one_to_two(a))
                                    mines[one_to_two(a)] = 1
                                    ctrr = ctrr+1
                                    
                                if ctrr == mine_no:
                                    break
                            l = blk % grid_size
                            b = int(int(blk) / int(grid_size))
                            print(l,b)
                            ctrrr = 0
                            for i in range(grid_size):
                                for j in range(grid_size):
                                    if(i!=l or j!=b) and (((abs(i-l)<5) and (abs(j-b)<2))) and (ctrrr<(pre-1)) and (mines[i,j]==0):
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
                                if (opened[one_to_two(blk)] == 0):
                                    openctr = openctr+1
                                opened[one_to_two(blk)] = 1
                                
                                print(mines)
                                print(opened)
                            #print("check if block contains mine then display gameover else open the box")
                        time.sleep(0.01)

                        
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
    global grid_size
    
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

#Game Loop
def gameloop():
    global blk_size
    global grid_size
    global openctr
    global restart
    global go
    global mines
    global first
    global flagged
    global opened
    global runn
    global ctrr
    global mine_no
    global blk_no
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0,0))
        #print("bb")
        
        
        
        for j in range(grid_size):
            for i in range (grid_size):
                button("",60 + blk_size*(i),30 + blk_size*(j),blk_size,blk_size,[100,100,100],[180,180,180],"click")
                if opened[i,j] == 1:
                    pygame.draw.rect(screen,(200,200,200),(60 + blk_size*(i),30 + blk_size*(j),blk_size,blk_size))
                    smallText = pygame.font.SysFont(("comicsansms"),20)
                    textSurf, textRect = text_objects(str(counter(j*grid_size + i)), smallText)
                    textRect.center = ((60 + blk_size*(i) + (blk_size/2)),(30 + blk_size*(j) + (blk_size/2)))
                    screen.blit(textSurf,textRect)



        for ii in range(grid_size+1):
            pygame.draw.line(screen, (0, 0, 0), (60 + blk_size*(ii), 30), (60 + blk_size*(ii), 510), 3)
        for ij in range(grid_size+1):
            pygame.draw.line(screen, (0, 0, 0), (60, 30 + blk_size*(ij)), (540, 30 + blk_size*(ij)), 3)
        
        for ib in range(blk_no):
            if flagged[ib]==1 and opened[one_to_two(ib)]==0:
                x,y = inv_map(ib)
                screen.blit(flag,(x,y))
                #print(flagged)
                
        if (go == True) and (openctr < (blk_no - mine_no)):
            for j in range(grid_size):
                for i in range(grid_size):
                    if mines[i,j] == 1:
                        screen.blit(mine,(60 + blk_size*(i),30 + blk_size*(j)))
            game_over_text()
        if (openctr >= (blk_no - mine_no)) and (go == False):
            
            for j in range(grid_size):
                for i in range(grid_size):
                    if mines[i,j] == 1:
                        screen.blit(mine,(60 + blk_size*(i),30 + blk_size*(j)))
            victory_text()
        button("",236,560,128,128,[100,100,100],[180,180,180],"restart")
        screen.blit(restarti,(236,560))
        if restart == True:
            runn = 0
            first = True
            mines = np.zeros((grid_size,grid_size))
            flagged = np.zeros(blk_no)
            opened = np.zeros((grid_size,grid_size))
            ctrr = 0
            go = False
            openctr = 0
            restart = False
            print("restarting")
            main()
            
        pygame.display.update()

game_intro()
def main():
    
    gameloop()
    pygame.quit()
    quit()
main()
