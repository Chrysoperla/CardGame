from mainapp import cards, models
from random import sample, randint

def first_turn_roll(user):
    roll = randint(1, 2)
    if roll == 1:
        announcement = "Player1 was drawn to get the first turn of the match"
        return announcement
    elif roll == 2:
        announcement = "Player2 was drawn to get the first turn of the match"
        player2_card_choice(user)
        return announcement


def start_game(request, initial_state):
    user = request.user
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
    roll = first_turn_roll(user)
    if roll == player1:
        return "Player1 turn"
    elif roll == player2:
        return "Player2 turn"

def replace_card():
    deck = cards.create_deck()
    random_card = sample(deck, 1)
    return random_card[0]

def player1_round_start(user):
    player1 = models.MatchState.objects.get(user=user).player1
    player1.gold += player1.mine
    player1.mana += player1.fountain
    player1.food += player1.farm
    return player1.gold, player1.mana, player1.food

def player1_card_usage(request):
    buttons = ['card1_usage', 'card2_usage', 'card3_usage', 'card4_usage', 'card5_usage']
    player1_state = models.Player1State.objects.get(user=request.user)
    which_card = [player1_state.card1, player1_state.card2, player1_state.card3, player1_state.card4, player1_state.card5]
    for button in buttons:
        if request.GET.get(button):
            for i in range(0, 5):
                if button == buttons[i]:
                    card_to_use_id = which_card[i]
                    card_number_in_hand = i
                    break
            deck = cards.create_deck()
            card_to_use = None
            for card in deck:
                if card.id == card_to_use_id:
                    card_to_use = card
                    break
            match = models.MatchState.objects.get(player1=player1_state)
            card_to_use.usage(1, match)
            card_replacement = replace_card()
            which_card[card_number_in_hand] = card_replacement.id
            player1_state.save()
            return


def player2_round_start(user):
    player2 = models.MatchState.objects.get(player1=user).player2
    player2.gold += player2.mine
    player2.mana += player2.fountain
    player2.food += player2.farm
    return player2.gold, player2.mana, player2.food

def player2_card_choice(request, user):
    # an algorhytm that the server uses to make the non-human player make its moves
    player1_state = models.Player1State.objects.get(user=request.user)
    player2 = models.MatchState.objects.get(player1=player1_state).player2
    player2_round_start(user)
    player2_deck = [player2.card1, player2.card2, player2.card3, player2.card4, player2.card5]
    for card in player2_deck:
        card_color = card.color
        if card_color == "G":
            if card.cost <= player2.food:
                card.usage()
                new_card = replace_card()
                player2.card = new_card
                return new_card
        if card_color == "R":
            if card.cost <= player2.gold:
                card.usage()
                new_card = replace_card()
                player2.card = new_card
                return new_card
        if card_color == "B":
            if card.cost <= player2.mana:
                card.usage()
                new_card = replace_card()
                player2.card = new_card
                return new_card
    player2.card1.discard()

def check_victory_conditions(request):
    # function that checks if any of victory conditions has been met. Returns 0 if none of them were met, 1 if
    # player1 wins or 2 if player 2 wins
    player1 = models.Player1State.objects.get(user=request.user)
    player2 = models.Player1State.objects.get(user=request.user)
    match_initial_state = models.MatchState.objects.get(player1=player1).initial_state
    is_game_over = 0
    if player1.tower < 1:
        is_game_over = 2
        result = "Your tower has been destroyed"
        return is_game_over, result
    if player2.tower < 1:
        is_game_over = 1
        result = "Your opponent's tower has been destroyed"
        print(is_game_over)
        return is_game_over, result
    if player1.tower >= match_initial_state.cov_tower:
        is_game_over = 1
        result = "Your tower has reached victorious height"
        return is_game_over, result
    if player2.tower >= match_initial_state.cov_tower:
        is_game_over = 2
        result = "Your opponent's tower has reached victorious height"
        return is_game_over, result
    if player1.gold or player1.mana or player1.food >= match_initial_state.cov_resources:
        is_game_over = 1
        result = "You have gathered enough resources to triumph over your opponent"
        return is_game_over, result
    if player2.gold or player2.mana or player2.food >= match_initial_state.cov_resources:
        is_game_over = 2
        result = "Your opponent have gathered plenty of resources and won"
        return is_game_over, result
    return is_game_over

def less_than_zero_check(number):
    # a function that makes sure that tower / wall / resources are not negative numbers
    if number < 0:
        number = 0
    return number

def less_than_one_check(number):
    # a function that makes sure that production levels are positive numbers
    if number < 0:
        number = 0
    return number
