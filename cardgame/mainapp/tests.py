import pytest
from django.contrib.auth import authenticate, login
from django.test import TestCase
from mainapp import models, game_engine, cards
from django.core.exceptions import ObjectDoesNotExist
from random import sample

@pytest.mark.django_db
def test_start_new_match(request):
    user = models.User.objects.create_user(username="Pytester", password='passed')
    initial_state = models.InitialState.objects.create(tower=20, wall=10, mine=3, fountain=2, farm=3, gold=10, mana=15,
                                                       food=10, cov_tower=60, cov_resources=250)
    # copy-pasted game_engine.start_game just avoiding using request
    deck = cards.create_deck()
    player1_cards = sample(deck, k=5)
    player2_cards = sample(deck, k=5)
    player1 = models.Player1State.objects.create(user=user, tower=initial_state.tower, wall=initial_state.wall,
                                                 mine=initial_state.mine, gold=initial_state.gold,
                                                 fountain=initial_state.fountain, mana=initial_state.mana,
                                                 farm=initial_state.farm, food=initial_state.food,
                                                 card1=player1_cards[0].id, card2=player1_cards[1].id, card3=player1_cards[2].id,
                                                 card4=player1_cards[3].id, card5=player1_cards[4].id)
    player2 = models.Player2State.objects.create(tower=initial_state.tower, wall=initial_state.wall,
                                                 mine=initial_state.mine, gold=initial_state.gold,
                                                 fountain=initial_state.fountain, mana=initial_state.mana,
                                                 farm=initial_state.farm, food=initial_state.food,
                                                 card1=player2_cards[0].id, card2=player2_cards[1].id, card3=player2_cards[2].id,
                                                 card4=player2_cards[3].id, card5=player2_cards[4].id)
    match_state = models.MatchState.objects.create(initial_state=initial_state, player1=player1, player2=player2)
    print(user)
    print(match_state)
    assert models.MatchState.objects.get(player1=player1)

@pytest.mark.django_db
def test_saving_match_state(request):
    user = models.User.objects.create_user(username="Pytester", password='passed')
    initial_state = models.InitialState.objects.create(tower=20, wall=10, mine=3, fountain=2, farm=3, gold=10, mana=15,
                                                       food=10, cov_tower=60, cov_resources=250)
    player1 = models.Player1State.objects.create(user=user, tower=10, wall=10, mine=1, gold=20, fountain=1, mana=20,
                                                 farm=1, food=20, card1=1, card2=2, card3=3, card4=4, card5=5)
    player2 = models.Player2State.objects.create(tower=10, wall=10, mine=1, gold=20, fountain=1, mana=20,
                                                 farm=1, food=20, card1=1, card2=2, card3=3, card4=4, card5=5)
    match_state = models.MatchState.objects.create(initial_state=initial_state, player1=player1, player2=player2)
    card_list = cards.create_card_list()
    card = card_list[0]
    print(f"Card id: {card.id}")
    assert player1.food == 20, player1.card1 == 1
    card.usage(1, match_state)
    assert player1.food == 18, player1.card1 == 1
    card_replacement = game_engine.replace_card()
    player1.card1 = card_replacement.id
    print(f"Card id: {player1.card1}")
    assert player1.food == 18
    player1.save()
    assert player1.food == 18



