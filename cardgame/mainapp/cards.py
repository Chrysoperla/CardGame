from mainapp import models

class Card:

    def __init__(self):
        self.player = 0
        # self.image =
        self.back_image = []

    def discard(self):
        player = 0
        return player

    def select_my_side(self, player, match):
        if player == 1:
            my_side = match.player1
            return my_side
        elif player == 2:
            my_side = match.player2
            return my_side

    def select_enemy_side(self, player, match):
        if player == 1:
            enemy_side = match.player2
            return enemy_side
        elif player == 2:
            enemy_side = match.player1
            return enemy_side

    def damage_calculation(self, damage):
        enemy_side = self.select_enemy_side()
        if enemy_side.wall >= damage:
            enemy_side.wall -= damage
        else:
            damage_wall_difference = damage - enemy_side.wall
            enemy_side.wall = 0
            enemy_side.tower -= damage_wall_difference
        return enemy_side.wall, enemy_side.tower

    def friendly_fire_calculation(self, damage):
        my_side = self.select_my_side()
        if my_side.wall >= damage:
            my_side.wall -= damage
        else:
            damage_wall_difference = damage - my_side.wall
            my_side.wall = 0
            my_side.tower -= damage_wall_difference
        return my_side.wall, my_side.tower


class TinyMouse(Card):

    def __init__(self):
        super().__init__()
        self.id = 1
        self.name = "Tiny Mouse"
        self.color = "G"
        self.cost = 2
        self.rarity = 3
        # self.image =

    def usage(self, player):
        # Deals 2 damage. The opponent loses 10 food.
        enemy_side = super().select_enemy_side()
        super().damage_calculation(2)
        if enemy_side.food >= 10:
            enemy_side.food -= 10
        else:
            enemy_side.food = 0
        return enemy_side.wall, enemy_side.food

class ArcaneButterfly(Card):

    def __init__(self):
        super().__init__()
        self.id = 2
        self.name = "Arcane Butterfly"
        self.color = "B"
        self.cost = 2
        self.rarity = 2
        # self.image =

    def usage(self, player):
        # Deals 5 damage if your fountain level is higher that your opponent's. Otherwise deals 3 damage
        enemy_side = super().select_enemy_side()
        my_side = super().select_my_side()
        if my_side.fountain > enemy_side.fountain:
            super().damage_calculation(5)
        else:
            super().damage_calculation(3)
        return enemy_side.wall, enemy_side.tower

class FelineFamiliar(Card):
    def __init__(self):
        super().__init__()
        self.id = 3
        self.name = "Feline Familiar"
        self.color = "G"
        self.cost = 8
        self.rarity = 1
        # self.image =

    def usage(self, player):
        # increase both your farm level and your fountain level by 1
        my_side = super().select_my_side()
        my_side.fountain += 1
        my_side.farm += 1
        return my_side.fountain, my_side.farm

class FoamReptile(Card):
    def __init__(self):
        super().__init__()
        self.id = 4
        self.name = "Foam Reptile"
        self.color = "G"
        self.cost = 7
        self.rarity = 1
        # self.image =

    def usage(self, player):
        # Deals 15 damage if enemy wall is 15 or higher. Otherwise, deals 8 damage
        enemy_side = super().select_enemy_side()
        if enemy_side.wall >= 15:
            enemy_side.wall -= 15
        else:
            super().damage_calculation(8)
            return enemy_side.wall, enemy_side.tower

class LoyalMount(Card):
    def __init__(self):
        super().__init__()
        self.id = 5
        self.name = "Loyal Mount"
        self.color = "R"
        self.cost = 10
        self.rarity = 1
        # self.image =

    def usage(self, player):
        # You get gold and food equal to your corresponding production levels. Also, increases wall by 5
        my_side = super().select_my_side()
        my_side.food += my_side.farm
        my_side.gold += my_side.mine
        my_side.wall += 5
        return my_side.food, my_side.gold, my_side.wall

class CommonWolf(Card):
    def __init__(self):
        super().__init__()
        self.id = 6
        self.name = "Common wolf"
        self.color = "G"
        self.cost = 3
        self.rarity = 2
        # self.image =

    def usage(self, player):
        # Deals 5 damage
        enemy_side = super().select_enemy_side()
        super().damage_calculation(5)
        return enemy_side.wall, enemy_side.tower

class Werewolf(Card):
    def __init__(self):
        super().__init__()
        self.id = 7
        self.name = "Werewolf"
        self.color = "B"
        self.cost = 9
        self.rarity = 1
        # self.image =

    def usage(self, player):
        # Deals 15 damage to your opponent. You take 5 damage
        enemy_side = super().select_enemy_side()
        my_side = super().select_my_side()
        super().damage_calculation(15)
        super().friendly_fire_calculation(5)
        return enemy_side.wall, enemy_side.tower, my_side.wall, my_side.tower

class Dwarves(Card):
    def __init__(self):
        super().__init__()
        self.id = 8
        self.name = "Dwarves"
        self.color = "R"
        self.cost = 10
        self.rarity = 1
        # self.image =

    def usage(self, player):
        # You get 1 mine level. Additionally, your tower and wall get increased by 5
        my_side = super().select_my_side()
        my_side.mine += 1
        my_side.wall += 5
        my_side.tower += 5
        return my_side.mine, my_side.wall, my_side.tower

class Mermaid(Card):
    def __init__(self):
        super().__init__()
        self.id = 9
        self.name = "Mermaid"
        self.color = "B"
        self.cost = 7
        self.rarity = 1
        # self.image =

    def usage(self, player):
        # Opponent's wall takes 15 damage
        enemy_side = super().select_enemy_side()
        if enemy_side.wall > 15:
            enemy_side.wall -= 15
        else:
            enemy_side.wall = 0
        return enemy_side.wall

class Orcs(Card):
    def __init__(self):
        super().__init__()
        self.id = 10
        self.name = "Orcs"
        self.color = "R"
        self.cost = 6
        self.rarity = 2
        # self.image =

    def usage(self, player):
        # Deals 8 damage to your opponent. Your tower +3
        enemy_side = super().select_enemy_side()
        my_side = super().select_my_side()
        super().damage_calculation(8)
        my_side.tower += 3
        return my_side.tower, enemy_side.tower, enemy_side.wall

class FriendlyFairy(Card):
    def __init__(self):
        super().__init__()
        self.id = 11
        self.name = "Friendly Fairy"
        self.color = "B"
        self.cost = 4
        self.rarity = 2
        # self.image =
    def usage(self, player, match):
        # Your fountain level gets increased by 1
        my_side = super().select_my_side(player, match)
        my_side.mana -= self.cost
        my_side.fountain += 1
        match.second_last_card = match.last_card
        match.last_card = self.id
        my_side.save()
        match.save()
        return my_side.fountain

def create_deck():
    deck = []
    for subclass in Card.__subclasses__():
        for i in range(1, subclass().rarity):
            card = subclass()
            deck.append(card)
    return deck



