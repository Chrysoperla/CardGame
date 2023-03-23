from mainapp import cards, models
from random import sample, randint

def first_turn_roll(request, user):
    roll = randint(1, 2)
    if roll == 1:
        announcement = "Player1 was drawn to get the first turn of the match"
        return announcement
    elif roll == 2:
        announcement = "Player2 was drawn to get the first turn of the match"
        player2_card_choice(request, user)
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
    roll = first_turn_roll(request, user)
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
            if card_number_in_hand == 0:
                player1_state.card1 = card_replacement.id
            elif card_number_in_hand == 1:
                player1_state.card2 = card_replacement.id
            elif card_number_in_hand == 2:
                player1_state.card3 = card_replacement.id
            elif card_number_in_hand == 3:
                player1_state.card4 = card_replacement.id
            elif card_number_in_hand == 4:
                player1_state.card5 = card_replacement.id
            return


def player2_round_start(user):
    player1_state = models.Player1State.objects.get(user=user)
    player2 = models.MatchState.objects.get(player1=player1_state).player2
    player2.gold += player2.mine
    player2.mana += player2.fountain
    player2.food += player2.farm
    return player2.gold, player2.mana, player2.food


def player2_card_choice(request, user):
    # an algorhytm that the server uses to make the non-human player make its moves
    player1_state = models.Player1State.objects.get(user=request.user)
    match = models.MatchState.objects.get(player1=player1_state)
    player2 = models.MatchState.objects.get(player1=player1_state).player2
    player2_round_start(user)
    player2_deck = [player2.card1, player2.card2, player2.card3, player2.card4, player2.card5]
    card_list = cards.create_card_list()
    for i in range(0, 5):
        for card in card_list:
            if card.id == player2_deck[i]:
                player2_deck[i] = card
                break
    for card_in_hand in player2_deck:
        card_color = card_in_hand.color
        if card_color == "G":
            if card_in_hand.cost <= player2.food:
                card_in_hand.usage(2, match)
                new_card = replace_card()
                player2.card = new_card
                return new_card
        if card_color == "R":
            if card_in_hand.cost <= player2.gold:
                card_in_hand.usage(2, match)
                new_card = replace_card()
                player2.card = new_card
                return new_card
        if card_color == "B":
            if card_in_hand.cost <= player2.mana:
                card_in_hand.usage(2, match)
                new_card = replace_card()
                player2.card = new_card
                return new_card
    player2.card1.discard()


def check_victory_conditions(request):
    # function that checks if any of victory conditions has been met. Returns 0 if none of them were met, 1 if
    # player1 wins or 2 if player 2 wins
    player1 = models.Player1State.objects.get(user=request.user)
    player2 = models.MatchState.objects.get(player1=player1).player2
    match_initial_state = models.MatchState.objects.get(player1=player1).initial_state
    is_game_over = 0
    if player1.tower < 1:
        is_game_over = 2
        result = "Your tower has been destroyed"
    elif player2.tower < 1:
        is_game_over = 1
        result = "Your opponent's tower has been destroyed"
    elif player1.tower >= match_initial_state.cov_tower:
        is_game_over = 1
        result = "Your tower has reached victorious height"
    elif player2.tower >= match_initial_state.cov_tower:
        is_game_over = 2
        result = "Your opponent's tower has reached victorious height"
    elif (player1.gold or player1.mana or player1.food) >= match_initial_state.cov_resources:
        is_game_over = 1
        result = "You have gathered enough resources to triumph over your opponent"
    elif (player2.gold or player2.mana or player2.food) >= match_initial_state.cov_resources:
        is_game_over = 2
        result = "Your opponent have gathered plenty of resources and won"
    if is_game_over != 0:
        return is_game_over, result
    return


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


def get_card_names_desc(ctx, last_card_id, second_last_card_id, player_cards_ids):
    # fills ctx for html templates with names, descriptions, color and cost of cards
    card_list = cards.create_card_list()
    for card in card_list:
        if last_card_id == card.id:
            last_card_name = card.name
            ctx["last_card_name"] = last_card_name
            last_card_desc = card.description
            ctx["last_card_description"] = last_card_desc
            last_card_color = card.color
            ctx["last_card_color"] = last_card_color
            last_card_cost = card.cost
            ctx["last_card_cost"] = last_card_cost
        if second_last_card_id == card.id:
            second_last_card_name = card.name
            ctx["second_last_card_name"] = second_last_card_name
            second_last_card_desc = card.description
            ctx["second_last_card_description"] = second_last_card_desc
            second_last_card_color = card.color
            ctx["second_last_card_color"] = second_last_card_color
            second_last_card_cost = card.cost
            ctx["second_last_card_cost"] = second_last_card_cost
        if player_cards_ids[0] == card.id:
            card1_name = card.name
            ctx["card1_name"] = card1_name
            card1_desc = card.description
            ctx["card1_description"] = card1_desc
            card1_color = card.color
            ctx["card1_color"] = card1_color
            card1_cost = card.cost
            ctx["card1_cost"] = card1_cost
        if player_cards_ids[1] == card.id:
            card2_name = card.name
            ctx["card2_name"] = card2_name
            card2_desc = card.description
            ctx["card2_description"] = card2_desc
            card2_color = card.color
            ctx["card2_color"] = card2_color
            card2_cost = card.cost
            ctx["card2_cost"] = card2_cost
        if player_cards_ids[2] == card.id:
            card3_name = card.name
            ctx["card3_name"] = card3_name
            card3_desc = card.description
            ctx["card3_description"] = card3_desc
            card3_color = card.color
            ctx["card3_color"] = card3_color
            card3_cost = card.cost
            ctx["card3_cost"] = card3_cost
        if player_cards_ids[3] == card.id:
            card4_name = card.name
            ctx["card4_name"] = card4_name
            card4_desc = card.description
            ctx["card4_description"] = card4_desc
            card4_color = card.color
            ctx["card4_color"] = card4_color
            card4_cost = card.cost
            ctx["card4_cost"] = card4_cost
        if player_cards_ids[4] == card.id:
            card5_name = card.name
            ctx["card5_name"] = card5_name
            card5_desc = card.description
            ctx["card5_description"] = card5_desc
            card5_color = card.color
            ctx["card5_color"] = card5_color
            card5_cost = card.cost
            ctx["card5_cost"] = card5_cost
    return ctx
