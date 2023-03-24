from django.db import models
from django.contrib.auth.models import User

class InitialState(models.Model):
    tower = models.PositiveIntegerField()
    wall = models.PositiveIntegerField()
    mine = models.PositiveIntegerField()
    gold = models.PositiveIntegerField()
    fountain = models.PositiveIntegerField()
    mana = models.PositiveIntegerField()
    farm = models.PositiveIntegerField()
    food = models.PositiveIntegerField()
    cov_tower = models.IntegerField()
    cov_resources = models.IntegerField()

class HumanPlayer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial_states = models.ManyToManyField(InitialState)
    game_count = models.IntegerField(default=0)

CARDS = (
    (1, "Tiny Mouse"),
    (2, "Arcane Butterfly"),
    (3, "Feline Familiar"),
    (4, "Foam Reptile"),
    (5, "Loyal Mount"),
    (6, "Common Wolf"),
    (7, "Werewolf"),
    (8, "Dwarves"),
    (9, "Mermaid"),
    (10, "Orcs"),
    (11, "Friendly Fairy"),
    (12, "Fire Dragon")
    )
class Player1State(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    tower = models.PositiveIntegerField()
    wall = models.PositiveIntegerField()
    mine = models.PositiveIntegerField()
    gold = models.PositiveIntegerField()
    fountain = models.PositiveIntegerField()
    mana = models.PositiveIntegerField()
    farm = models.PositiveIntegerField()
    food = models.PositiveIntegerField()
    card1 = models.IntegerField(choices=CARDS)
    card2 = models.IntegerField(choices=CARDS)
    card3 = models.IntegerField(choices=CARDS)
    card4 = models.IntegerField(choices=CARDS)
    card5 = models.IntegerField(choices=CARDS)

class Player2State(models.Model):
    tower = models.PositiveIntegerField()
    wall = models.PositiveIntegerField()
    mine = models.PositiveIntegerField()
    gold = models.PositiveIntegerField()
    fountain = models.PositiveIntegerField()
    mana = models.PositiveIntegerField()
    farm = models.PositiveIntegerField()
    food = models.PositiveIntegerField()
    card1 = models.IntegerField(choices=CARDS)
    card2 = models.IntegerField(choices=CARDS)
    card3 = models.IntegerField(choices=CARDS)
    card4 = models.IntegerField(choices=CARDS)
    card5 = models.IntegerField(choices=CARDS)

class MatchState(models.Model):
    initial_state = models.ForeignKey(InitialState, on_delete=models.CASCADE)
    player1 = models.OneToOneField(Player1State, on_delete=models.CASCADE)
    player2 = models.OneToOneField(Player2State, on_delete=models.CASCADE)
    last_card = models.IntegerField(null=True, choices=CARDS)
    second_last_card = models.IntegerField(null=True, choices=CARDS)
