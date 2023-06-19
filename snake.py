class Snake:
    """ Objet représentant le serpent """

    def __init__(self, pos=[100, 100]):
        self.len = 4
        self.pos = pos
        self.body = [[70, 100], [80, 100], [90, 100], [100, 100]]

    def move_up(self):
        """ Permet de déplacer le serpent d'une case vers le haut """

        self.pos[1] -= 10
        self.update()

    def move_down(self):
        """ Permet de déplacer le serpent d'une case vers le bas """

        self.pos[1] += 10
        self.update()

    def move_right(self):
        """ Permet de déplacer le serpent d'une case vers la droite """

        self.pos[0] += 10
        self.update()

    def move_left(self):
        """ Permet de déplacer le serpent d'une case vers la gauche """

        self.pos[0] -= 10
        self.update()

    def update(self):
        """ Permet de mettre à jour le corps du serpent """

        self.body.pop(0)
        self.body.append(self.pos.copy())

    def add_body(self):
        """ Permet d'ajouter un segment au corps du serpent """

        self.body = [self.body[0], *self.body]
