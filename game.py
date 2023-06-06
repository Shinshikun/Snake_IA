import pygame
import time
import random

from snake import Snake
from fruit import Fruit
 
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


class Game():

    def __init__(self, wx=720, wy=480, title="Snake"):
        self.wx = wx
        self.wy = wy
        self.score = 0
        self.snake = Snake()
        self.fruit = Fruit(pos=(random.randrange(1, (self.wx//10)) * 10,
                                random.randrange(1, (self.wy//10)) * 10))

        pygame.init()
        pygame.display.set_caption(title)

        self.game_window = pygame.display.set_mode((self.wx, self.wy))
        self.fps = pygame.time.Clock()


    def show_score(self, color=white, font='times new roman', size=20):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)


    def game_over(self):
        font = pygame.font.SysFont('times new roman', 50)

        game_over_surface = font.render(
            'Your Score is : ' + str(self.score), True, red)
        
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.wx/2, self.wy/4)

        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        quit()

    def create_new_fruit(self):
        x=random.randrange(1, (self.wx//10)) * 10
        y=random.randrange(1, (self.wy//10)) * 10

        while([x,y] in self.snake.body):
            x=random.randrange(1, (self.wx//10)) * 10
            y=random.randrange(1, (self.wy//10)) * 10

        self.fruit = Fruit((x,y))



    def run(self):
        direction = 'RIGHT'
        change_to = direction
        while True:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        change_to = 'RIGHT'

            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

            if direction == 'UP':
                self.snake.move_up()
            if direction == 'DOWN':
                self.snake.move_down()
            if direction == 'LEFT':
                self.snake.move_left()
            if direction == 'RIGHT':
                self.snake.move_right()


            if self.snake.pos[0] == self.fruit.pos[0] and self.snake.pos[1] == self.fruit.pos[1]:
                self.score += 10
                self.snake.add_body()
                self.create_new_fruit()


            self.game_window.fill(black)
     
            for pos in self.snake.body:
                pygame.draw.rect(self.game_window, green,
                                pygame.Rect(pos[0], pos[1], 10, 10))
                
            pygame.draw.rect(self.game_window, white, pygame.Rect(
                self.fruit.pos[0], self.fruit.pos[1], 10, 10))
        
            # Game Over conditions
            if self.snake.pos[0] < 0 or self.snake.pos[0] > self.wx-10:
                self.game_over()
            if self.snake.pos[1] < 0 or self.snake.pos[1] > self.wy-10:
                self.game_over()
        
            # Touching the snake body
            for block in self.snake.body[0:-1]:
                if self.snake.pos[0] == block[0] and self.snake.pos[1] == block[1]:
                    self.game_over()
        
            # displaying score continuously
            self.show_score(white, 'times new roman', 20)
        
            # Refresh game screen
            pygame.display.update()
        
            # Frame Per Second /Refresh Rate
            self.fps.tick(15)