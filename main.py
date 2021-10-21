import numpy as np
from random import randint
import pandas as pd


def get_cards():
    cards = []
    card_decks = 8
    four_times_cards = [2, 3, 4, 5, 6, 7, 8, 9, 69]
    sixteen_times_cards = [10]
    for i in range(card_decks):
        for f in range(4):
            for k in four_times_cards:
                cards.append(k)
        for f in range(16):
            for k in sixteen_times_cards:
                cards.append(k)
    cards = np.array(cards, dtype="int8")
    np.random.shuffle(cards)
    return cards


def get_random_card(cards):
    card = 111
    while card == 111:
        random_number = randint(0, len(cards) - 1)
        card = cards[random_number]
        cards[random_number] = 111
    return cards, card


def dealer(cards):
    # normale_karten_chance = 4/52
    # zehner_karten_chance = 10/52
    card_value = 0

    while card_value < 17:
        if check(cards) is False:
            cards = get_cards()
        cards, card = get_random_card(cards)
        if card_value == 0:
            first_card = card
        if card == 69:
            if card_value <= 10:
                card = 11
            else:
                card = 1
        card_value += card

    if card_value > 21:
        return False, card_value, first_card
    else:
        return True, card_value, first_card


def player(cards, secure_val):
    # normale_karten_chance = 4/52
    # zehner_karten_chance = 10/52

    card_value = 0
    while card_value < 21 - secure_val:
        if check(cards) is False:
            cards = get_cards()
        cards, card = get_random_card(cards)
        if card == 69:
            if card_value <= 10:
                card = 11
            else:
                card = 1
        card_value += card

    if card_value > 21:
        return False, card_value
    else:
        return True, card_value



def check(cards):
    if np.sort(cards)[0] == 111:
        return False
    return True

def append_results(player_list, pl1_check, pl1_val, deal_check, deal_val):
    # beide true
    if deal_check and pl1_check:
        if pl1_val == deal_val:
            player_list["dealer"]["won"].append(0); player_list["dealer"]["lost"].append(0); player_list["dealer"]["tie"].append(1); player_list["dealer"]["burn"].append(0)
            player_list["player1"]["won"].append(0); player_list["player1"]["lost"].append(0); player_list["player1"]["tie"].append(1); player_list["player1"]["burn"].append(0)
        elif pl1_val < deal_val:
            player_list["dealer"]["won"].append(1); player_list["dealer"]["lost"].append(0); player_list["dealer"]["tie"].append(0); player_list["dealer"]["burn"].append(0)
            player_list["player1"]["won"].append(0); player_list["player1"]["lost"].append(1); player_list["player1"]["tie"].append(0); player_list["player1"]["burn"].append(0)
        elif pl1_val > deal_val:
            player_list["dealer"]["won"].append(0); player_list["dealer"]["lost"].append(1); player_list["dealer"]["tie"].append(0); player_list["dealer"]["burn"].append(0)
            player_list["player1"]["won"].append(1); player_list["player1"]["lost"].append(0); player_list["player1"]["tie"].append(0); player_list["player1"]["burn"].append(0)

    # beide false
    elif deal_check is False and pl1_check is False:
        player_list["dealer"]["won"].append(1); player_list["dealer"]["lost"].append(0); player_list["dealer"]["tie"].append(0); player_list["dealer"]["burn"].append(0)
        player_list["player1"]["won"].append(0); player_list["player1"]["lost"].append(1); player_list["player1"]["tie"].append(0); player_list["player1"]["burn"].append(1)

    # dealer = true, player = false
    elif deal_check and pl1_check is False:
        player_list["dealer"]["won"].append(1); player_list["dealer"]["lost"].append(0); player_list["dealer"]["tie"].append(0); player_list["dealer"]["burn"].append(0)
        player_list["player1"]["won"].append(0); player_list["player1"]["lost"].append(1); player_list["player1"]["tie"].append(0); player_list["player1"]["burn"].append(1)

    # dealer = false, player = true
    elif deal_check is False and pl1_check:
        player_list["dealer"]["won"].append(0); player_list["dealer"]["lost"].append(1); player_list["dealer"]["tie"].append(0); player_list["dealer"]["burn"].append(1)
        player_list["player1"]["won"].append(1); player_list["player1"]["lost"].append(0); player_list["player1"]["tie"].append(0); player_list["player1"]["burn"].append(0)

    return player_list

def run(space_val):
    player_list = {
        "dealer": {
            "won": [],
            "lost": [],
            "tie": [],
            "burn": []
        },
        "player1": {
            "won": [],
            "lost": [],
            "tie": [],
            "burn": []
        }
    }

    cards = get_cards()
    for i in range(1000000):
        pl1_check, pl1_val = player(cards, space_val)
        deal_check, deal_val, first_card = dealer(cards)
        player_list = append_results(player_list, pl1_check, pl1_val, deal_check, deal_val)

    return player_list

if __name__ == "__main__":
    space_val = 5
    generation = 1
    direction = 1
    highest_mean = 0

    while True:
        generation += 1
        try:
            mean_before = player1.mean()["won"]
        except NameError:
            mean_before = 0
        player_list = run(space_val)
        player1 = pd.DataFrame(player_list["player1"])

        mean_now = player1.mean()["won"]
        if mean_now - mean_before > 0:
            # keep direction
            space_val += 1 * direction
        else:
            # change direction
            direction = direction * (-1)
            space_val += 1 * direction

        if highest_mean < mean_now:
            highest_space_val = space_val
            highest_mean = mean_now
            o = open("top_results", "w")
            o.write(f"{highest_space_val}\n{player1.describe()}")
            o.close()

        print(f"gerneration: {generation}, highest_mean: {highest_mean} with space_val {highest_space_val}\nspace value: {space_val}")
        print(player1.mean())






        

