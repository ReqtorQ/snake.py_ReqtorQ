# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 22:17:26 2022

@author: Renze
"""
import pygame as pg
import sys
import random

class Snake(object):
    def __init__(self):
        self.length = 1
        self.pos = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (154, 205, 50)
        self.score = 0
    
    def get_head_pos(self):
        return self.pos[0]
    
    def turn(self,point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        cur = self.get_head_pos()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) % SCREEN_WIDTH), 
                (cur[1] + (y*GRID_SIZE)) % SCREEN_HEIGHT)
        
        if len(self.pos) > 2 and new in self.pos[2:]:
            main.score = 0
            self.reset()

            
        else:
            self.pos.insert(0, new)
            if len(self.pos) > self.length:
                self.pos.pop()
    
    def reset(self):
        self.length = 1
        self.pos = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    
    def draw(self, surface):
        for p in self.pos:
            r = pg.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, self.color, r)
            pg.draw.rect(surface, (142,142,142  ), r, 1)
    
    def handle_keys(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.turn(UP)
                elif event.key == pg.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pg.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pg.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
    

class Food(object):
    def __init__(self):
        self.pos = (0, 0)
        self.color = (223, 163, 49)
        
    
    def randomize_pos(self):
        self.pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, 
                    random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        
    def draw(self, surface):
        r = pg.Rect((self.pos[0], self.pos[1]), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.color, r)
        pg.draw.rect(surface, (50,50,50), r, 1)

def drawGrid(surface):
    for y in range(0, int(SCREEN_HEIGHT)):
        for x in range(0, int(SCREEN_WIDTH)):
            if (x + y) % 2 == 0:
                r = pg.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pg.draw.rect(surface, (142,142,142), r)
            
            else:
                rr = pg.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pg.draw.rect(surface, (50,50,50), rr)


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    pg.init()
    
    clock = pg.time.Clock()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    
    surface = pg.Surface(screen.get_size())
    surface = surface.convert()
    
    drawGrid(surface)
    
    snake = Snake()
    food = Food()
    scorefont = pg.font.SysFont('calibri', 30)
    while (True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_pos() == food.pos:
            snake.length += 1
            snake.score += 1
            food.randomize_pos()
        # handle events
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = scorefont.render('Score: {0}'.format(snake.score), 1, (255,0,0))
        screen.blit(text, (5, 10))
        pg.display.update()

main()