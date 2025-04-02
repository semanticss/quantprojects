import random as rand
import math
from collections import Counter
import math
import os
import streamlit as st
from itertools import combinations
import tqdm as tqdm

# all cards are tuples
# consider a Game class to make global variable stuff not so cooked

hands_score_dict = { # <-- quantified hand rankings
        "royal_flush": 9,
        "straight_flush": 8,
        "quads": 7,
        "full_house": 6,
        "flush": 5,
        "straight": 4,
        "three_of_a_kind": 3,
        "two_pair": 2,
        "pair": 1,
        "high_card": 0
    }

ranks = ['2','3','4','5','6','7','8',"9","10", 'J', 'Q', 'K', 'A']
suits = ['s', 'h', 'c', 'd']

sorted_ranks = sorted(ranks)

deck = [(rank, suit) for rank in ranks for suit in suits]
int_deck = [13 * {'s': 3, 'h': 2, 'c': 0, 'd': 1}[suit]
            + {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}[rank] 
            for (rank, suit) in deck]
    
rand.shuffle(deck)
rand.shuffle(int_deck)

def card_str_to_int(card_str):
        rank_map = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6,
                    '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
        suit_map = {'c': 0, 'd': 1, 'h': 2, 's': 3}
        rank_part = card_str[:-1]
        suit_part = card_str[-1].lower()
        return 13 * suit_map[suit_part] + rank_map[rank_part.upper()]

def get_rank(card: int):
    assert type(card) == int
    return card % 13

def get_suit(card: int):
    assert type(card) == int
    return card // 13

playerdict = {} # <-- instantiates dictionary to store other players

def evaluate_five_card_hand(cards: list):

    assert len(cards) == 5 # <-- make sure the input has only 5 cards


    ranks = [get_rank(c) for c in cards] # <-- get the rank of each card
    suits = [get_suit(c) for c in cards] # <-- get the suit of each card
    sorted_ranks = sorted(ranks) 
    rank_appearances = Counter(ranks) # <-- count how many times each rank appears, store them in a dict with the corresponding values
    suit_appearances = Counter(suits) # <-- count how many times each suit appears, store them in a dict with the corresponding values

    # <-- sort the ranks in ascending order


    flush = straight = three_of_a_kind = quads = pair = two_pair = full_house = straight_flush = royal_flush = False # <-- you have no made hand before we evaluate
    
    # Royal Flush Checker - working

    if len(set(suits)) == 1: # <-- if all same suit
        if len(set(ranks)) == 5: # <-- if all distinct cards
            if max(ranks) == 12 and min(ranks) == 8: # <-- if the highest card is an ace and if the lowest card is a 10
                if sorted_ranks[-1] - sorted_ranks[0] == 4: # <-- if the difference of biggest and smallest is 4. this works because we are accessing these values from a sorted list.
                    royal_flush = True
                 
    # Straight Flush Tester - working

    if len(set(suits)) == 1:
        if len(set(ranks)) == 5:
            if sorted_ranks[-1] - sorted_ranks[0] == 4:
                straight_flush = True
            if sorted_ranks[-1] - sorted_ranks[0] == 12: # <-- accounts for ace low straights
                straight_flush = True
            
    # Flush tester  - working
    if len(set(suits)) == 1:
        flush = True

    # Straight tester - ace low straight accounted for  - working
    
    if len(set(ranks)) == 5:
        sorted_ranks = sorted(ranks)
        if sorted_ranks[-1] - sorted_ranks[0] == 4:
            straight = True
        if sorted_ranks[-1] - sorted_ranks[0] == 12:
            straight = True

    # Quads tester  - working

    if max(rank_appearances.values()) == 4:
        quads = True


    # Boat + Three of a kind checker  - working

    elif 3 in rank_appearances.values(): # <-- if something occurs three times
        if 2 in rank_appearances.values(): # <-- if something else occurs two times
            full_house = True
        else: # <-- minimum something appeared 3 times
            three_of_a_kind = True 


    # Two pair checker  - working

    elif list(rank_appearances.values()).count(2) == 2:
        two_pair = True


    # Pair checker  - working

    elif max(rank_appearances.values()) == 2: # 
        pair = True

    # returns highest score
    if royal_flush:
        return (hands_score_dict["royal_flush"], [])
    
    elif straight_flush:
        return (hands_score_dict["straight_flush"], [max(sorted_ranks)])
    
    elif quads:
        quads_rank = [rank for rank, count in rank_appearances.items() if count == 4][0]
        kicker = [rank for rank in reversed(sorted_ranks) if rank != quads_rank][0]
        return (hands_score_dict["quads"], [quads_rank, kicker])
    
    elif full_house:
        trips_rank = max(rank for rank, count in rank_appearances.items() if count == 3)
        pair_rank = max(rank for rank, count in rank_appearances.items() if count == 2)
        return (hands_score_dict["full_house"], [trips_rank, pair_rank])

    
    elif flush:
        return (hands_score_dict["flush"], sorted_ranks)
    
    elif straight:
        return (hands_score_dict["straight"], [max(sorted_ranks)])
    
    elif three_of_a_kind:
        trips_rank = [rank for rank, count in rank_appearances.items() if count == 3][0]
        kickers = [rank for rank in reversed(sorted_ranks) if rank != trips_rank][:2]
        return (hands_score_dict["three_of_a_kind"], [trips_rank] + kickers)
    
    elif two_pair:
        pair_ranks = sorted([rank for rank, count in rank_appearances.items() if count == 2], reverse=True)
        kicker = [rank for rank in reversed(sorted_ranks) if rank not in pair_ranks][0]
        return (hands_score_dict["two_pair"], pair_ranks[:2] + [kicker])
    
    elif pair:
        pair_rank = [rank for rank, count in rank_appearances.items() if count == 2][0]
        kickers = [rank for rank in reversed(sorted_ranks) if rank != pair_rank][:3]
        return (hands_score_dict["pair"], [pair_rank] + kickers)
    
    else:
        high_cards = list(reversed(sorted_ranks))[:5]
        return (hands_score_dict["high_card"], high_cards)
    
def best_seven_card_hand(cards: list):

    assert len(cards) == 7
    return max(evaluate_five_card_hand(list(combo)) for combo in combinations(cards, 5))


def monte_sim(hero_hole: tuple, opponents: int, community_cards: list, num_simulations: int = 1000)-> float:
    wins, ties, losses = 0,0,0

    for _ in tqdm.tqdm(range(num_simulations)):
        used_cards = set(list(hero_hole) + community_cards)
        available_deck = [card for card in int_deck if card not in used_cards]
        rand.shuffle(deck)
        rand.shuffle(int_deck)

        # Deal cards to opponents
        opponent_hands = [tuple(available_deck[i:i+2]) for i in range(0, 2 * opponents, 2)]
        community_cards_remaining = 5 - len(community_cards)
        board = community_cards + available_deck[2 * opponents:2 * opponents + community_cards_remaining]

        hero_hand_score = best_seven_card_hand(list(hero_hole) + board)

        opponent_best_hands = [best_seven_card_hand(list(opponent_hand) + board) for opponent_hand in opponent_hands]

        if any(hero_hand_score < opp_hand for opp_hand in opponent_best_hands):
            losses += 1
        elif any(hero_hand_score == opp_hand for opp_hand in opponent_best_hands):
            ties += 1
        else:
            wins += 1


    return {
        "win_probability": wins / num_simulations,
        "tie_probability": ties / num_simulations,
        "loss_probability": losses / num_simulations
    }

def ev_calc(pot: float, call: float, winp: float, tiep: float, oppnum: int) -> float:

    expected_val = (winp * pot) + (tiep * pot / (1 + oppnum)) - call

    return expected_val

def best_choice(pot: float, call: float, raise_amnt: float, winp: float, tiep: float, oppnum: int) -> str:

    ev_call = ev_calc(pot, call, winp, tiep, oppnum)
    ev_raise = ev_calc(pot + raise_amnt, raise_amnt, winp, tiep, oppnum)

    if ev_call > 0 and ev_call >= ev_raise:
        return 'call'
    elif ev_raise > ev_call and ev_raise > 0:
        return 'raise'
    else:
        return 'fold'

def poker_solver(hero_hole: tuple, num_opponents: int, community_cards: list, # return after 100, 1000, 10000, etc.
                 pot_size: float, call_amount: float, raise_amount: float,
                 num_simulations: int = 1000) -> dict:

    chances = monte_sim(hero_hole, num_opponents, community_cards, num_simulations)

    win_probability = chances["win_probability"]
    tie_probability = chances["tie_probability"]
    decision = best_choice(pot_size, call_amount, raise_amount, win_probability, tie_probability, num_opponents)

    return {
        "probabilities": chances,
        "optimal_decision": decision
    }

if __name__ == "__main__":
    
    print("Enter hero hole cards in format like 'As Ks' (rank and suit, space separated):")

    hero_input = input().strip().split()
    hero_hole = tuple(card_str_to_int(card) for card in hero_input)

    print("Enter number of opponents:")
    num_opponents = int(input().strip())

    print("community cards:")
    community_input = input().strip()
    community_cards = [card_str_to_int(card) for card in community_input.split()] if community_input else []

    print("Enter pot size:")
    pot_size = float(input().strip())

    print("Enter call amount:")
    call_amount = float(input().strip())

    print("Enter raise amount:")
    raise_amount = float(input().strip())

    print("Enter number of simulations:")
    num_simulations = int(input().strip())

    result = poker_solver(hero_hole, num_opponents, community_cards, pot_size, call_amount, raise_amount, num_simulations)

    print("\n--- Simulation Results ---")
    print("Win probability:", result['probabilities']['win_probability'])
    print("Tie probability:", result['probabilities']['tie_probability'])
    print("Loss probability:", result['probabilities']['loss_probability'])
    print("Recommended action:", result['optimal_decision'])