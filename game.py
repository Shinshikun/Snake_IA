import pygame
import time
import random
import numpy as np
from abc import ABC

from snake import Snake
from fruit import Fruit

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


class BaseGame(ABC):
    """ Classe de base pour la création d'une partie de Snake"""

    def __init__(self, wx=720, wy=480, title="Snake", spd=15):
        self.wx = wx
        self.wy = wy
        self.score = 0
        self.spd = spd
        self.snake = Snake()
        self.fruit = Fruit(pos=(random.randrange(1, (self.wx // 10)) * 10,
                                random.randrange(1, (self.wy // 10)) * 10))

        pygame.display.set_caption(title)

        self.game_window = pygame.display.set_mode((self.wx, self.wy))
        self.fps = pygame.time.Clock()

    def create_new_fruit(self):
        """ Permet de placer un fruit à récupérer"""

        x = random.randrange(1, (self.wx // 10)) * 10
        y = random.randrange(1, (self.wy // 10)) * 10

        while ([x, y] in self.snake.body):
            x = random.randrange(1, (self.wx // 10)) * 10
            y = random.randrange(1, (self.wy // 10)) * 10

        self.fruit = Fruit((x, y))

    def check_head_fruit(self) -> bool:
        """ Check si le serpent entre en collision avec le fruit """

        if self.snake.pos[0] == self.fruit.pos[0] and self.snake.pos[1] == self.fruit.pos[1]:
            self.score += 10
            self.snake.add_body()
            self.create_new_fruit()
            return True
        return False

    def check_collide(self, pos=None) -> bool:
        """ Check si le serpent entre en collision avec son corps ou le bord de l'écran """

        if pos is None:
            pos = self.snake.pos

        if pos[0] < 0 or pos[0] > self.wx - \
                10 or pos[1] < 0 or pos[1] > self.wy - 10:
            return True

        if pos in self.snake.body[:-1]:
            return True

        return False

    def update_ui(self):
        """ Permet de mettre à jour l'UI """

        self.game_window.fill(black)
        for pos in self.snake.body:
            pygame.draw.rect(self.game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(self.game_window, white, pygame.Rect(
            self.fruit.pos[0], self.fruit.pos[1], 10, 10))

        self.show_score(white, 'times new roman', 20)
        pygame.display.update()
        self.fps.tick(self.spd)


class Game_AI(BaseGame):
    """ Classe du jeu pour être utilisée par une IA """

    def __init__(self, wx=720, wy=480, title="Snake", spd=15):
        super().__init__(wx, wy, title, spd)
        self.direction = 1

    def game_step(self, action) -> tuple(int, int, int):
        """
        Effectue une étape d'une partie
        action = [Devant, Droite, Gauche]
        """

        reward = 0
        game_over = False
        list_dir = [1, 2, 3, 4]  # Droite, Bas, Gauche, Haut
        index = list_dir.index[self.direction]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if np.array_equal(action, [1, 0, 0]):
            dir = list_dir[index]
        elif np.array_equal(action, [0, 1, 0]):
            dir = list_dir[(index + 1) % 4]
        elif np.array_equal(action, [0, 0, 1]):
            dir = list_dir[(index - 1) % 4]

        self.direction = dir

        match dir:
            case 1:
                self.snake.move_right()
            case 2:
                self.snake.move_down()
            case 3:
                self.snake.move_left()
            case 4: self.snake.move_right()

        if self.check_head_fruit():
            reward = 1
            return reward, game_over, self.score

        if self.check_collide():
            reward = -1
            game_over = True

            return reward, game_over, self.score

        self.update_ui()

        return reward, game_over, self.score

    def reset(self):
        """ Permet de réinitialiser la partie """

        self.direction = 1
        self.score = 0
        self.snake = Snake()


class Game(BaseGame):
    """ Classe du jeu permettant à un humain d'y jouer """

    def __init__(self, wx=720, wy=480, title="Snake", spd=15):
        super().__init__(wx, wy, title, spd)

    def show_score(self, color=white, font='times new roman', size=20):
        """ Permet d'afficher le score à l'écran """

        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render(
            'Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)

    def game_over(self):
        """ Permet de passer à l'étape du game over et ferme ensuite le jeu """

        font = pygame.font.SysFont('times new roman', 50)

        game_over_surface = font.render(
            'Your Score is : ' + str(self.score), True, red)

        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.wx / 2, self.wy / 4)

        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        quit()

    def run(self):
        """ Permet de lancer la boucle du jeu """

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
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

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

            self.check_head_fruit()

            if self.check_collide():
                self.game_over()

            self.update_ui()
