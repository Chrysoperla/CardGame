import pytest
from django.contrib.auth import authenticate, login
from django.test import TestCase
from mainapp import models, game_engine
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.django_db
def test_start_new_match(request):
    user = authenticate(username='PyTester', password='passed')
    if user is not None:
        login(request, user)
    try:
        player1_state = models.Player1State.objects.get(user=user)
        player1_state.remove()
    except models.Player1State.DoesNotExist:
        pass
    game_engine.player1_card_usage(request)
    game_engine.check_victory_conditions(request)
    initial_state = models.InitialState.objects.get(tower=20, wall=10, mine=3, fountain=2, farm=3, gold=10, mana=15,
                                                    food=10, cov_tower=60, cov_resources=250)
    game_engine.start_game(request, initial_state)
    assert models.Player1State.objects.get(user=user)



#
# def test_card_cost():
#     pass
#
#
# def test_card_usage():
#     pass
#
