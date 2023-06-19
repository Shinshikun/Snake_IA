import numpy as np

from game import Game_AI


def Agent():

    def __init__(self):
        pass

    def get_state_of_game(self, game: Game_AI) -> np.ndarray:
        snake_pos = game.snake.pos

        right = game.direction == 1
        down = game.direction == 2
        left = game.direction == 3
        up = game.direction == 4

        case_right = [snake_pos[0] + 10, snake_pos[1]]
        case_down = [snake_pos[0], snake_pos[1] + 10]
        case_left = [snake_pos[0] - 10, snake_pos[1]]
        case_up = [snake_pos[0], snake_pos[1] - 10]

        # On va créer un vecteur de 1 ou 0 représentant l'état de notre jeu et toutes les informations possibles
        # Le vecteur est créé de façon arbitraire, il s'agit uniquement de
        # définir une représentation logique de l'état de la partie
        state = []

        # On check si collision devant nous
        state.append(
            (right and game.check_collide(case_right)) or
            (down and game.check_collide(case_down)) or
            (left and game.check_collide(case_left)) or
            (up and game.check_collide(case_up))
        )

        # On check si collision à notre droite
        state.append(
            (right and game.check_collide(case_down)) or
            (down and game.check_collide(case_left)) or
            (left and game.check_collide(case_up)) or
            (up and game.check_collide(case_right))
        )

        # On check si collision à notre gauche
        state.append(
            (right and game.check_collide(case_up)) or
            (down and game.check_collide(case_right)) or
            (left and game.check_collide(case_down)) or
            (up and game.check_collide(case_left))
        )

        # On ajoute à l'état la position du fruit
        state.append(
            snake_pos[0] < game.fruit.pos[0],  # Fruit à droite
            snake_pos[1] < game.fruit.pos[1],  # Fruit en bas
            snake_pos[0] > game.fruit.pos[0],  # Fruit à gauche
            snake_pos[1] > game.fruit.pos[1]  # Fruit en haut
        )

        # On ajoute la direction actuelle de notre serpent
        state.append(
            right,
            down,
            left,
            up
        )

        return np.array(state, dtype=int)
