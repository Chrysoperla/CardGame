from django.db import models
from django.contrib.auth.models import User

class InitialState(models.Model):
    tower = models.IntegerField()
    wall = models.IntegerField()
    mine = models.IntegerField()
    gold = models.IntegerField()
    fountain = models.IntegerField()
    mana = models.IntegerField()
    farm = models.IntegerField()
    food = models.IntegerField()
    cov_tower = models.IntegerField()
    cov_resources = models.IntegerField()

class HumanPlayer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial_states = models.ManyToManyField(InitialState)
    game_count = models.IntegerField(default=0)

class Player1State(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tower = models.IntegerField()
    wall = models.IntegerField()
    mine = models.IntegerField()
    gold = models.IntegerField()
    fountain = models.IntegerField()
    mana = models.IntegerField()
    farm = models.IntegerField()
    food = models.IntegerField()
    card1 = models.IntegerField()
    card2 = models.IntegerField()
    card3 = models.IntegerField()
    card4 = models.IntegerField()
    card5 = models.IntegerField()

class Player2State(models.Model):
    tower = models.IntegerField()
    wall = models.IntegerField()
    mine = models.IntegerField()
    gold = models.IntegerField()
    fountain = models.IntegerField()
    mana = models.IntegerField()
    farm = models.IntegerField()
    food = models.IntegerField()
    card1 = models.IntegerField()
    card2 = models.IntegerField()
    card3 = models.IntegerField()
    card4 = models.IntegerField()
    card5 = models.IntegerField()

class MatchState(models.Model):
    initial_state = models.ForeignKey(InitialState, on_delete=models.CASCADE)
    player1 = models.OneToOneField(Player1State, on_delete=models.CASCADE)
    player2 = models.OneToOneField(Player2State, on_delete=models.CASCADE, null=True)