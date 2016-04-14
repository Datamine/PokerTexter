# John Loeber | contact@johnloeber.com | Python 2.7.11 | April 2016

from itertools import product
from random import shuffle
from deuces import Card, Evaluator
from sys import argv

"""
This script creates lookup tables of probabilities and expected values for
preflop hands, for a given number of players. The script takes one command-line
argument: the numbers of players. Within the script, you may also set the number
of trials for each hand, but the default value should be fine. The output of
this script is a file `lookup-table-n` where n == other_players (see line 139).
"""

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["s","d","c","h"]

# constants for outcome of a given hand
WIN = 0x00
TIE = 0x01
LOSE = 0x02

# initialize deuces hand-evaluator
evaluator = Evaluator()

def expected_gain(wins, ties):
    """
    computes the expected gain (EG) of a preflop hand. Assumes no blinds,
    a 1-unit bet per player, and no further bets. To be clear, an EG of 0 implies
    expected breakeven, > 0 implies an expected gain, < 0 implies an expected loss.
    We use the standard expected value formula, grouping all opponents into one.
    """
    my_val = wins * other_players
    their_val = (1 - wins - ties) * 1
    return my_val - their_val

def eval_table(my_hand, shared_cards, other_hands):
    """
    Evaluates the table, your hand, and the hands of other players to see whether
    you win, lose, or tie. We use the deuces library to score all hands on a
    [1,7462] interval, where 1 == Royal Flush.
    """
    # Can I shortcut this? Detect when the player has the strongest possible hand given the board?
    my_score = evaluator.evaluate(shared_cards, my_hand)
    # keep track of the best (lowest) score of any other player
    max_other = 9999
    for hand in other_hands:
        opponent_result = evaluator.evaluate(shared_cards,hand)
        if opponent_result <  my_score:
            return LOSE
        max_other = min(max_other, opponent_result)
    if max_other==my_score:
        return TIE
    else:
        return WIN

def get_probabilities(card_1, card_2, other_players, trials=10000):
    """
    for a given preflop hand, compute the probabilities of winning or tying.
    Note that we've got a very important design decision here: we could obtain
    the probabilities in a combinatorial fashion -- it's possible to mathematically
    reason to obtain the exact probability of winning or tying, but this seems
    quite involved. It's much easier to use a Monte Carlo simulation to approximate
    the probabilities. With a large number of trials (e.g. 10k or 100k) the
    approximations should be sufficiently close to the theoretical "true" values
    for all practical intents and purposes. 
    """
    deck = map(lambda (x,y): Card.new(y+x), list(product(suits,ranks)))
    wins = 0
    ties = 0
    deck.remove(card_1)
    deck.remove(card_2)
    for i in range(trials):
        # Randomly shuffling the deck and slicing the first few cards to get hands
        # seems computationally cheaper than using random.choice to select subsets as hands
        shuffle(deck)
        shared_cards = deck[:5]
        # hands held by other players
        other_hands = [deck[5+(2*x):7+(2*x)] for x in range(other_players)]
        result = eval_table([card_1, card_2], shared_cards, other_hands)
        if result == WIN:
            wins +=1
        elif result == TIE:
            ties +=1
    return wins/float(trials), ties/float(trials)

def write_to_file(f, r1, r2, suiting, wins, ties):
    """
    this is a helper function only for cleanliness in the block of code below.
    """
    cards = r1 + "\t" + r2 + "\t" + suiting
    outcome = str(wins) + "\t" + str(ties) + "\t" + str(expected_gain(wins,ties))
    f.write(cards + "\t" + outcome + "\n")
    return

def main(other_players, trials):
    with open("lookup-table-" + str(other_players), "w") as f:
        # iterate over all 169 equivalent starting hands. If you're curious about 
        # why there are only 169 equivalent starting hands, see:
        # https://en.wikipedia.org/wiki/Texas_hold_'em_starting_hands#Essentials
        count = 0
        for c1 in range(len(ranks)):
            for c2 in range(c1,len(ranks)):
                # note that the way we iterate means that r1 <= r2 always. 
                # knowing this makes it easier to get data from the output lookup table. 
                r1 = ranks[c1]
                r2 = ranks[c2]
                # We only ever use Spades and Clubs as suits because all that matters
                # is whether your starting cards are suited or off-suit. The suits
                # themselves are all equivalent, so the nominal choice doesn't matter.
                if r1==r2:
                    wins,ties = get_probabilities((Card.new(r1 + "s")), Card.new(r2 + "c"), 
                                                    other_players, trials)
                    write_to_file(f, r1, r2, "offsuit", wins, ties)
                    count +=1
                else:
                    wins,ties = get_probabilities((Card.new(r1 + "s")), Card.new(r2+ "c"), 
                                                    other_players, trials)
                    write_to_file(f, r1, r2, "offsuit", wins, ties)
                    count +=1

                    wins,ties = get_probabilities((Card.new(r1 + "s")), Card.new(r2+ "s"), 
                                                    other_players, trials)
                    write_to_file(f, r1, r2, "suited", wins, ties)
                    count +=1
                # Log the script's progress. For a given number of players, every simulation 
                # should take roughly equally long. However, the more players you have, 
                # the longer the entire process takes. (More hands to evaluate.)
                print "Simulated " + str(count) +" / 169"

if __name__=='__main__':
    # number of players excluding yourself.
    other_players = int(argv[1])
    if other_players < 1:
        raise ValueError("other_players < 1. You should be playing with at least 1 other person.")
    elif other_players > 22:
        raise ValueError("other_players > 22. Theoretical maximum number of players is 23.")
    
    # set the number of trials according to the level of statistical rigor you want.
    # the default of 10k yields a small standard error and should be fine for almost all
    # purposes, but if you need very high-precision results, consider increasing to
    # 100k or 1m trials.
    if len(argv) == 3:
        trials = int(argv[2])
    else:
        trials = 10000

    main(other_players,trials)
