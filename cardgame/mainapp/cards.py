card_count = 0

class Card:

    def __init__(self):
        self.player = 0
        # self.image =
        self.back_image = []

    def discard(self):
        player = 0
        return player

    def select_my_side(self):
        if self.player == 1:
            my_side = player_1
            return my_side
        elif self.player == 2:
            my_side = player_2
            return my_side

    def select_enemy_side(self):
        if self.player == 1:
            enemy_side = player_2
            return enemy_side
        elif self.player == 2:
            enemy_side = player_1
            return enemy_side
        else:
            return "Encountered an error while trying to check sides"

class TinyMouse(Card):

    def __init__(self):
        super().__init__()
        self.id = 1
        self.name = "Tiny mouse"
        self.color = "G"
        self.cost = 2
        self.rarity = 3
        # self.image =

    def usage(self):
        super.select_enemy_side()
        enemy_side.wall -= 2
        enemy_side.food -= 10
        return enemy_side.wall, enemy_side.food
