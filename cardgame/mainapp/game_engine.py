from mainapp import cards, models
from random import sample, randint

def first_turn_roll(request, user):
    # chooses a player who makes the first move of the game: player1 (roll=1) or player2 (roll=2)
    roll = randint(1, 2)
    if roll == 1:
        return
    elif roll == 2:
        player2_card_choice(request)
        return


def start_game(request, initial_state):
    # starts a game match based on given initial state
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
    # chooses a random card to replace a used / discarded one
    deck = cards.create_deck()
    random_card = sample(deck, 1)
    return random_card[0]


def player1_round_start(user):
    # increases player1's resources by a number equal to their production level at the start of their every round but
    # first
    player1 = models.Player1State.objects.get(user=user)
    player1.gold += player1.mine
    player1.mana += player1.fountain
    player1.food += player1.farm
    player1.save()
    return


def player1_card_usage(request):
    # calls usage function of the card that had its "use" button clicked. After that moves the card to "last used cast"
    # spot and replaces the card
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
            player1_state.save()
            return


def player2_round_start(user):
    # increases player2's resources by a number equal to their production level at the start of their every round but
    # first
    player1_state = models.Player1State.objects.get(user=user)
    player2 = models.MatchState.objects.get(player1=player1_state).player2
    player2.gold += player2.mine
    player2.mana += player2.fountain
    player2.food += player2.farm
    player2.save()
    return


def player2_card_choice(request):
    # an algorhytm that the server uses to make the non-human player make its moves
    player1_state = models.Player1State.objects.get(user=request.user)
    match = models.MatchState.objects.get(player1=player1_state)
    player2 = models.MatchState.objects.get(player1=player1_state).player2
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
            last_card_cost = card.cost
            ctx["last_card_cost"] = last_card_cost
        if second_last_card_id == card.id:
            second_last_card_name = card.name
            ctx["second_last_card_name"] = second_last_card_name
            second_last_card_desc = card.description
            ctx["second_last_card_description"] = second_last_card_desc
            second_last_card_cost = card.cost
            ctx["second_last_card_cost"] = second_last_card_cost
        if player_cards_ids[0] == card.id:
            card1_name = card.name
            ctx["card1_name"] = card1_name
            card1_desc = card.description
            ctx["card1_description"] = card1_desc
            card1_cost = card.cost
            ctx["card1_cost"] = card1_cost
        if player_cards_ids[1] == card.id:
            card2_name = card.name
            ctx["card2_name"] = card2_name
            card2_desc = card.description
            ctx["card2_description"] = card2_desc
            card2_cost = card.cost
            ctx["card2_cost"] = card2_cost
        if player_cards_ids[2] == card.id:
            card3_name = card.name
            ctx["card3_name"] = card3_name
            card3_desc = card.description
            ctx["card3_description"] = card3_desc
            card3_cost = card.cost
            ctx["card3_cost"] = card3_cost
        if player_cards_ids[3] == card.id:
            card4_name = card.name
            ctx["card4_name"] = card4_name
            card4_desc = card.description
            ctx["card4_description"] = card4_desc
            card4_cost = card.cost
            ctx["card4_cost"] = card4_cost
        if player_cards_ids[4] == card.id:
            card5_name = card.name
            ctx["card5_name"] = card5_name
            card5_desc = card.description
            ctx["card5_description"] = card5_desc
            card5_cost = card.cost
            ctx["card5_cost"] = card5_cost
    colors_for_styles = add_card_colors_to_html(last_card_id, second_last_card_id, player_cards_ids)
    ctx["last_card_color"] = colors_for_styles[0]
    ctx["second_last_card_color"] = colors_for_styles[1]
    ctx["card1_color"] = colors_for_styles[2][0]
    ctx["card2_color"] = colors_for_styles[2][1]
    ctx["card3_color"] = colors_for_styles[2][2]
    ctx["card4_color"] = colors_for_styles[2][3]
    ctx["card5_color"] = colors_for_styles[2][4]
    return ctx

def color_interpreter(color):
    # changes name color from one-letter abbreviation to HEX color for coloring cards
    if color == "R":
        hex_color = "#ff968f"
    if color == "B":
        hex_color = "#8fb0ff"
    if color == "G":
        hex_color = "#76cf79"
    return hex_color
def add_card_colors_to_html(last_card_id, second_last_card_id, player_cards_ids):
    card_list = cards.create_card_list()
    for card in card_list:
        if last_card_id == card.id:
            last_card_color = color_interpreter(card.color)
        if second_last_card_id == card.id:
            second_last_card_color = color_interpreter(card.color)
        if player_cards_ids[0] == card.id:
            card1_color = color_interpreter(card.color)
        if player_cards_ids[1] == card.id:
            card2_color = color_interpreter(card.color)
        if player_cards_ids[2] == card.id:
            card3_color = color_interpreter(card.color)
        if player_cards_ids[3] == card.id:
            card4_color = color_interpreter(card.color)
        if player_cards_ids[4] == card.id:
            card5_color = color_interpreter(card.color)
    if last_card_id == None:
        last_card_color = None
    if second_last_card_id == None:
        second_last_card_color = None

    colors_for_styles = [last_card_color, second_last_card_color, [card1_color, card2_color, card3_color, card4_color,
                                                                   card5_color]]
    return colors_for_styles

def initial_state_check(tower, wall, mine, gold, fountain, mana, farm, food, cov_tower, cov_resources):
    if tower < 1 or tower > 999 or cov_tower < 1 or cov_tower > 999:
        error_message = "The tower must be higher that 0 and lower than 1000"
    elif wall < 0 or wall > 999:
        error_message = "The wall must be higher or equal 0 and lower than 1000"
    elif (mine or fountain or farm) < 1 or (mine or fountain or farm) > 99:
        error_message = "The production levels must be higher that 0 and lower than 100"
    elif (gold or mana or food) < 0 or (gold or mana or food) > 999 or cov_resources < 0 or cov_resources > 999:
        error_message = "The resource numbers must be higher or equal 0 and lower than 1000"
    elif tower >= cov_tower:
        error_message = "The initial height of the tower must be lower than the victorious one"
    elif (gold or mana or food) >= cov_resources:
        error_message = "The initial amounts of resources must be lower than the victorious one"
    return error_message
