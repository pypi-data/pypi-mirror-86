import pygame, sys
import random
import math
from pygame import mixer
from pygame.locals import *


#Setting pygame
clock=pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Ninja vs Zombies')
WINDOW_SIZE=(1280,768)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((640,384))
bg_image=pygame.image.load('sprites/tileset/BG/BG.png')
mixer.music.load('sounds/Sundown Drive.mp3')
mixer.music.play(-1)


def load_animations(path,finalframe,name,scale,colorkey,invertx):
    animation_list=[]
    for i in range(finalframe+1):
        image=pygame.image.load(path+name+'__'+str(i)+'.png')
        image=pygame.transform.smoothscale(image,(int(image.get_width()/scale),int(image.get_height()/scale)))
        image.set_colorkey(colorkey)
        if invertx:
            image=pygame.transform.flip(image,True,False)
        animation_list.append(image)
    return animation_list

#Player animations and rect
player_imgs_idle=load_animations('sprites/ninja/',9,'Idle',3.2,(255,255,255),False)
player_imgs_idle_flip=load_animations('sprites/ninja/',9,'Idle',3.2,(255,255,255),True)
player_imgs_run=load_animations('sprites/ninja/',9,'Run',3.2,(255,255,255),False)
player_imgs_run_flip=load_animations('sprites/ninja/',9,'Run',3.2,(255,255,255),True)
player_imgs_jump=load_animations('sprites/ninja/',9,'Jump',3.2,(255,255,255),False)
player_imgs_jump_flip=load_animations('sprites/ninja/',9,'Jump',3.2,(255,255,255),True)
player_imgs_throw=load_animations('sprites/ninja/',9,'Throw',3.2,(255,255,255),False)
player_imgs_throw_flip=load_animations('sprites/ninja/',9,'Throw',3.2,(255,255,255),True)
player_imgs_jump_throw=load_animations('sprites/ninja/',9,'Jump_Throw',3.2,(255,255,255),False)
player_imgs_jump_throw_flip=load_animations('sprites/ninja/',9,'Jump_Throw',3.2,(255,255,255),True)
player_frame_i=0
checkpoint_x=280
checkpoint_y=780
player_rect=pygame.Rect(checkpoint_x,checkpoint_y,player_imgs_idle[0].get_width(),player_imgs_idle[0].get_height())

#Movement bools
moving_right=False
moving_left=False
flip_right=True
flip_left=False

#Jumping variables
player_y_momentum=0
air_timer=0

#Throw kunai
kunai_state=False  #True : kunai was thrown (cannot throw)
kunai_state_i=0
kunai_img=pygame.image.load('sprites/tileset/Object/Kunai_0.png')
kunai_img=pygame.transform.smoothscale(kunai_img,(int(kunai_img.get_width()/3),int(kunai_img.get_height()/3)))
kunai_img_flip=pygame.transform.flip(kunai_img,True,False)
kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())

def kunai_throw(x,y,img,display):
    global kunai_state
    kunai_state=True
    display.blit(img,(x+10,y+18))
    
#Window scrolling
true_scroll=[0,0]
scroll=[0,0]

#Tile mapping - 0 to 9 : ---
#10 - A,11 - B,etc
def loadtiles(path,finalnum):
    tiles_img=[]
    for i in range(1,finalnum+1):
        tile_img=pygame.image.load(path+str(i)+'.png')
        tile_img=pygame.transform.smoothscale(tile_img,(32,32))
        tiles_img.append(tile_img)
    return tiles_img
tiles_img=loadtiles('sprites/tileset/Tiles/',19)
TILE_SIZE=tiles_img[0].get_width()

#Tiles that reset player position
def danger_tiles(DANGER,gamemap):
    danger_coord=[]
    for i in range(len(gamemap)-1):
        for j in range(len(gamemap[0])):
            if gamemap[i][j] in DANGER:
                danger_coord.append((32*j,32*i))
    return danger_coord

#Function for loading map
def load_map(path):
    f=open(path + '.txt','r')
    data=f.read()
    f.close()
    data=data.split('\n')
    gamemap=[]
    for row in data:
        gamemap.append(list(row))
    return gamemap

#Setting which tiles dont collide , and also those whom reset the player´s position.
COLLIDE_OFF=['H','I','0','J']
DANGER=['H','J']
gamemap=load_map('map2')
danger_tiles=danger_tiles(DANGER,gamemap)

#Checking if rect collides with any of the tiles
def collision_test(rect,tiles):
    hit_list=[] 
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#Moves rect, according to its movement, if it is not colliding with tiles
def move(rect,movement,tiles):
    collision_types = {'top': False, 'bottom': False , 'right': False , 'left': False}
    rect.x+=movement[0]
    hit_list=collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left # .right = coord. x da borda direita , .left = coord.x da borda esquerda
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left']=True
    rect.y+=movement[1]
    hit_list=collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom=tile.top
            collision_types['bottom']= True
        elif movement[1] < 0:
            rect.top =tile.bottom
            collision_types['top']=True
    return rect, collision_types

#Setting game loop
while True: 
    #Init settings
    display.fill((146,244,255))
    display.blit(bg_image,(0,0))
    tile_rects= []
    true_scroll[0] += ((player_rect.x-true_scroll[0])-200)/8 
    true_scroll[1] += ((player_rect.y-true_scroll[1])-200)/8 
    scroll[0]=int(true_scroll[0])
    scroll[1]=int(true_scroll[1])
    
    #Creates tileset , and defines images
    for i in range(len(gamemap)-1): 
        for j in range(len(gamemap[0])):
            if gamemap[i][j] == '1':
                display.blit(tiles_img[0],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '2':
                display.blit(tiles_img[1],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '3':
                display.blit(tiles_img[2],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '4':
                display.blit(tiles_img[3],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '5':
                display.blit(tiles_img[4],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '6':
                display.blit(tiles_img[5],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '7':
                display.blit(tiles_img[6],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '8':
                display.blit(tiles_img[7],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '9':
                display.blit(tiles_img[8],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'A':
                display.blit(tiles_img[9],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'B':
                display.blit(tiles_img[10],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'C':
                display.blit(tiles_img[11],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'D':
                display.blit(tiles_img[12],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'E':
                display.blit(tiles_img[13],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'F':
                display.blit(tiles_img[14],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'G':
                display.blit(tiles_img[15],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'H': 
                display.blit(tiles_img[16],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'I': 
                display.blit(tiles_img[17],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'J':
                display.blit(tiles_img[18],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'K':
                display.blit(tiles_img[19],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'L':
                display.blit(tiles_img[20],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] not in COLLIDE_OFF:
                tile_rects.append(pygame.Rect(j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE,TILE_SIZE))
    
    #Setting player movement
    player_movement=[0,0]
    if moving_right:
        player_movement[0]+=3
        if flip_left:
            flip_left=False
            flip_right=True
    if moving_left:
        player_movement[0]-=3
        if flip_right:
            flip_right=False
            flip_left=True
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
    player_rect,player_collisions=move(player_rect,player_movement,tile_rects)
    #print(f'player x {player_rect.x}')
    #print(f'player y {player_rect.y}')
    
    #If player touches dangerous tiles
    for i in range(len(danger_tiles)):
        if player_rect.x > danger_tiles[i][0] and player_rect.x < danger_tiles[i][0] +33 and player_rect.y > danger_tiles[i][1]-32 and player_rect.y < danger_tiles[i][1]:
            player_rect.x=checkpoint_x
            player_rect.y=checkpoint_y
    
    #Correcting jumping variables
    if player_collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    elif player_collisions['top']:
        player_y_momentum = 0
    else:
        air_timer += 1

    #Player Animations 
    if player_frame_i<=44:
        player_frame_i+=1
    elif player_frame_i == 45:
        if air_timer == 0:
            player_frame_i=0
        else:
            player_frame_i=45
    if moving_right:
        if air_timer <= 5:
            if flip_right:
                display.blit(player_imgs_run[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif flip_left:
                display.blit(player_imgs_run_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        elif air_timer > 5:
            if flip_right:
                display.blit(player_imgs_jump[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif flip_left:
                display.blit(player_imgs_jump_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
    elif moving_left:
        if air_timer <= 5:
            if flip_right:
                display.blit(player_imgs_run[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif flip_left:
                display.blit(player_imgs_run_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        elif air_timer > 5:
            if flip_right:
                display.blit(player_imgs_jump[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif flip_left:
                display.blit(player_imgs_jump_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
    else:
        if air_timer <= 5:
            if flip_right:
                display.blit(player_imgs_idle[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif flip_left:
                display.blit(player_imgs_idle_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        elif air_timer > 5:
            if flip_right:
                display.blit(player_imgs_jump[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif flip_left:
                display.blit(player_imgs_jump_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
    
    #Kunai movement
    if kunai_state:
        if kunai_state_i < 60:
            if kunai_right:
                kunai_rect,kunai_collisions=move(kunai_rect,kunai_movement,tile_rects)
                kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img,display)
                if kunai_collisions['left'] or kunai_collisions['right']:
                    kunai_state_i=0
                    kunai_state=False
                    kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())
            elif kunai_left:
                kunai_rect,kunai_collisions=move(kunai_rect,kunai_movement,tile_rects)
                kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img_flip,display)
                if kunai_collisions['left'] or kunai_collisions['right']:
                    kunai_state_i=0
                    kunai_state=False
                    kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())
            kunai_state_i+=1
        elif kunai_state_i == 60:
            kunai_state_i=0
            kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())
            kunai_state=False


    #Getting inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum=-6
            if event.key == K_v and kunai_state == False:
                kunai_rect.x=player_rect.x+10
                kunai_rect.y=player_rect.y+18
                if flip_right:
                    kunai_right=True
                    kunai_left=False
                    kunai_movement=[7,0]
                    kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img,display) 
                elif flip_left:
                    kunai_left=True
                    kunai_right=False
                    kunai_movement =[-7,0]
                    kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img_flip,display)
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player_frame_i=0
                moving_right = False
            if event.key == K_LEFT:
                player_frame_i=0
                moving_left = False   
    
    #Updating game screen
    surf = pygame.transform.smoothscale(display,WINDOW_SIZE)
    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60) 
