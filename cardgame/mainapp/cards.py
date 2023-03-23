from mainapp import models, game_engine


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

    def damage_calculation(self, damage, player, match):
        enemy_side = self.select_enemy_side(player, match)
        if enemy_side.wall >= damage:
            enemy_side.wall -= damage
        else:
            damage_wall_difference = damage - enemy_side.wall
            enemy_side.wall = 0
            enemy_side.tower -= damage_wall_difference
            enemy_side.tower = game_engine.less_than_zero_check(enemy_side.tower)
        return enemy_side.wall, enemy_side.tower

    def friendly_fire_calculation(self, damage, player, match):
        my_side = self.select_my_side(player, match)
        if my_side.wall >= damage:
            my_side.wall -= damage
        else:
            damage_wall_difference = damage - my_side.wall
            my_side.wall = 0
            my_side.tower -= damage_wall_difference
            my_side.tower = game_engine.less_than_zero_check(my_side.tower)
        return my_side.wall, my_side.tower


class TinyMouse(Card):

    def __init__(self):
        super().__init__()
        self.id = 1
        self.name = "Tiny Mouse"
        self.color = "G"
        self.cost = 2
        self.rarity = 3
        self.description = "Deals 2 damage. The opponent loses 10 food."
        # self.image =

    def usage(self, player, match):
        # Deals 2 damage. The opponent loses 10 food.
        enemy_side = super().select_enemy_side(player, match)
        my_side = super().select_my_side(player, match)
        my_side.food -= self.cost
        super().damage_calculation(2, player, match)
        if enemy_side.food >= 10:
            enemy_side.food -= 10
        else:
            enemy_side.food = 0
        match.second_last_card = match.last_card
        match.last_card = self.id
        enemy_side.save()
        my_side.save()
        match.save()
        return enemy_side.wall, enemy_side.food

class ArcaneButterfly(Card):

    def __init__(self):
        super().__init__()
        self.id = 2
        self.name = "Arcane Butterfly"
        self.color = "B"
        self.cost = 2
        self.rarity = 2
        self.description = "Deals 5 damage if your fountain level is higher that your opponent's. Otherwise deals 3 damage"
        # self.image =

    def usage(self, player, match):
        # Deals 5 damage if your fountain level is higher that your opponent's. Otherwise deals 3 damage
        enemy_side = super().select_enemy_side(player, match)
        my_side = super().select_my_side(player, match)
        my_side.mana -= self.cost
        my_side.save()
        if my_side.fountain > enemy_side.fountain:
            super().damage_calculation(5, player, match)
        else:
            super().damage_calculation(3, player, match)
        match.second_last_card = match.last_card
        match.last_card = self.id
        enemy_side.save()
        my_side.save()
        match.save()
        return enemy_side.wall, enemy_side.tower

class FelineFamiliar(Card):
    def __init__(self):
        super().__init__()
        self.id = 3
        self.name = "Feline Familiar"
        self.color = "B"
        self.cost = 8
        self.rarity = 1
        self.description = "Increases both your farm level and your fountain level by 1"
        # self.image =

    def usage(self, player, match):
        # increase both your farm level and your fountain level by 1
        my_side = super().select_my_side(player, match)
        my_side.food -= self.cost
        my_side.fountain += 1
        my_side.farm += 1
        my_side.save()
        match.second_last_card = match.last_card
        match.last_card = self.id
        my_side.save()
        match.save()
        return my_side.fountain, my_side.farm

class FoamReptile(Card):
    def __init__(self):
        super().__init__()
        self.id = 4
        self.name = "Foam Reptile"
        self.color = "G"
        self.cost = 7
        self.rarity = 1
        self.description = "Deals 15 damage if enemy wall is 15 or higher. Otherwise, deals 8 damage"
        # self.image =

    def usage(self, player, match):
        # Deals 15 damage if enemy wall is 15 or higher. Otherwise, deals 8 damage
        enemy_side = super().select_enemy_side(player, match)
        my_side = super().select_my_side(player, match)
        my_side.food -= self.cost
        if enemy_side.wall >= 15:
            enemy_side.wall -= 15
        else:
            super().damage_calculation(8, player, match)
        match.second_last_card = match.last_card
        match.last_card = self.id
        enemy_side.save()
        my_side.save()
        match.save()
        return enemy_side.wall, enemy_side.tower

class LoyalMount(Card):
    def __init__(self):
        super().__init__()
        self.id = 5
        self.name = "Loyal Mount"
        self.color = "R"
        self.cost = 10
        self.rarity = 1
        self.description = "You get gold and food equal to your corresponding production levels. Also, increases wall by 5"
        # self.image =

    def usage(self, player, match):
        # You get gold and food equal to your corresponding production levels. Also, increases wall by 5
        my_side = super().select_my_side(player, match)
        my_side.gold -= self.cost
        my_side.food += my_side.farm
        my_side.gold += my_side.mine
        my_side.wall += 5
        match.second_last_card = match.last_card
        match.last_card = self.id
        my_side.save()
        match.save()
        return my_side.food, my_side.gold, my_side.wall

class CommonWolf(Card):
    def __init__(self):
        super().__init__()
        self.id = 6
        self.name = "Common wolf"
        self.color = "G"
        self.cost = 3
        self.rarity = 2
        self.description = "Deals 5 damage"
        # self.image =

    def usage(self, player, match):
        # Deals 5 damage
        enemy_side = super().select_enemy_side(player, match)
        my_side = super().select_my_side(player, match)
        my_side.food = my_side.food - self.cost
        my_side.save()
        super().damage_calculation(5, player, match)
        enemy_side.save()
        match.second_last_card = match.last_card
        match.last_card = self.id
        match.save()
        return

class Werewolf(Card):
    def __init__(self):
        super().__init__()
        self.id = 7
        self.name = "Werewolf"
        self.color = "B"
        self.cost = 9
        self.rarity = 1
        self.description = "Deals 15 damage to your opponent. You take 5 damage"
        # self.image =

    def usage(self, player, match):
        # Deals 15 damage to your opponent. You take 5 damage
        enemy_side = super().select_enemy_side(player, match)
        my_side = super().select_my_side(player, match)
        my_side.mana -= self.cost
        super().damage_calculation(15, player, match)
        super().friendly_fire_calculation(5, player, match)
        match.second_last_card = match.last_card
        match.last_card = self.id
        enemy_side.save()
        my_side.save()
        match.save()
        return enemy_side.wall, enemy_side.tower, my_side.wall, my_side.tower

class Dwarves(Card):
    def __init__(self):
        super().__init__()
        self.id = 8
        self.name = "Dwarves"
        self.color = "R"
        self.cost = 10
        self.rarity = 1
        self.description = "You get 1 mine level. Additionally, your tower and wall get increased by 5"
        # self.image =

    def usage(self, player, match):
        # You get 1 mine level. Additionally, your tower and wall get increased by 5
        my_side = super().select_my_side(player, match)
        my_side.gold -= self.cost
        my_side.mine += 1
        my_side.wall += 5
        my_side.tower += 5
        match.second_last_card = match.last_card
        match.last_card = self.id
        my_side.save()
        match.save()
        return my_side.mine, my_side.wall, my_side.tower

class Mermaid(Card):
    def __init__(self):
        super().__init__()
        self.id = 9
        self.name = "Mermaid"
        self.color = "B"
        self.cost = 7
        self.rarity = 1
        self.description = "Opponent's wall takes 15 damage"
        # self.image =

    def usage(self, player, match):
        # Opponent's wall takes 15 damage
        enemy_side = super().select_enemy_side(player, match)
        my_side = super().select_my_side(player, match)
        my_side.mana -= self.cost
        if enemy_side.wall > 15:
            enemy_side.wall -= 15
        else:
            enemy_side.wall = 0
        match.second_last_card = match.last_card
        match.last_card = self.id
        enemy_side.save()
        my_side.save()
        match.save()
        return enemy_side.wall

class Orcs(Card):
    def __init__(self):
        super().__init__()
        self.id = 10
        self.name = "Orcs"
        self.color = "R"
        self.cost = 6
        self.rarity = 2
        self.description = "Deals 8 damage to your opponent. Your tower +3"
        # self.image =

    def usage(self, player, match):
        # Deals 8 damage to your opponent. Your tower +3
        enemy_side = super().select_enemy_side(player, match)
        my_side = super().select_my_side(player, match)
        my_side.gold -= self.cost
        super().damage_calculation(8, player, match)
        my_side.tower += 3
        match.second_last_card = match.last_card
        match.last_card = self.id
        enemy_side.save()
        my_side.save()
        match.save()
        return my_side.tower, enemy_side.tower, enemy_side.wall

class FriendlyFairy(Card):
    def __init__(self):
        super().__init__()
        self.id = 11
        self.name = "Friendly Fairy"
        self.color = "B"
        self.cost = 4
        self.rarity = 2
        self.description = "Your fountain level gets increased by 1"
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
    # creates a list of all the cards. The same card will appear in the deck the number of times its rarity applies.
    deck = []
    for subclass in Card.__subclasses__():
        for i in range(1, subclass().rarity+1):
            card = subclass()
            deck.append(card)
    return deck

def create_card_list():
    # creates a list of all the cards. Every card will appear only once. For iterations
    card_list = []
    for subclass in Card.__subclasses__():
        card = subclass()
        card_list.append(card)
    return card_list



