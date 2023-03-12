from mainapp import cards, models
from random import sample, randint

# TYMCZASOWE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
mouse = TinyMouse()
deck = [mouse, mouse, mouse, mouse, mouse]

def first_turn_roll(player1, player2):
    roll = randint(1, 2)
    if roll == 1:
        return player1
    elif roll == 2:
        return player2


def start_game(request, initial_state):
    user = request.user
    player1_cards = sample(cards.deck, k=5)
    player2_cards = sample(cards.deck, k=5)
    player1 = models.Player1State.objects.create(user=user, tower=initial_state.tower, wall=initial_state.wall,
                                                 mine=initial_state.mine, gold=initial_state.gold,
                                                 fountain=initial_state.fountain, mana=initial_state.mana,
                                                 farm=initial_state.farm, food=initial_state.food,
                                                 card1=player1_cards[0], card2=player1_cards[1], card3=player1_cards[2],
                                                 card4=player1_cards[3], card5=player1_cards[4])
    player2 = models.Player2State.objects.create(tower=initial_state.tower, wall=initial_state.wall,
                                                 mine=initial_state.mine, gold=initial_state.gold,
                                                 fountain=initial_state.fountain, mana=initial_state.mana,
                                                 farm=initial_state.farm, food=initial_state.food,
                                                 card1=player2_cards[0], card2=player2_cards[1], card3=player2_cards[2],
                                                 card4=player2_cards[3], card5=player2_cards[4])
    match_state = models.MatchState.objects.create(initial_state=initial_state, player1=player1, player2=player2)
    roll = first_turn_roll(player1, player2)
    if roll == player1:
        return "Player1 turn"
    elif roll == player2:
        return "Player2 turn"

def replace_card():
    random_card = sample(deck, 1)
    return random_card

def computer_player(user):
    # an algorhytm that the server uses to make the non-human player make its moves
    player2 = models.MatchState.objects.get(player1=user).player2
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

# dokończyć dla kart 2,3,4,5

