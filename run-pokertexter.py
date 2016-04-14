# John Loeber | contact@johnloeber.com | April 2016 | Python 2.7.11

# adapted from the Twilio quickstart tutorial:
# https://www.twilio.com/docs/quickstart/python/sms/replying-to-sms-messages

from flask import Flask, request, redirect
from os import environ
import twilio.twiml
# only import stdout if you need to debug. Then use stdout.flush() after print.
# from sys import stdout

"""
This script runs on Heroku, and is connected to Twilio such that it handles
incomingo messages, responding in turn with appropriate statistics for the
poker hand described in the message. It determines the statistics by parsing
the described hand, and looking it up in one of the lookup-tables in this
directory.
"""

# we'll need the list of ranks for a fast lookup.
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

# standard errormessage as response to bad input
STANDARD_ERRORMSG = "Error! Could not parse input. " \
                    "Send text in form RANK RANK SUITING OTHER_PLAYERS. " \
                    "Respond with `examples` if you need examples."

app = Flask(__name__)

def get_rank(string):
    """
    Parses a string representing a rank. Returns a string in the correct form
    for the lookup table. Returns None if the input could not be parsed.
    """
    if "ace" in string or string=="a":
        return "A"
    if "king" in string or string=="k":
        return "K"
    if "queen" in string or string=="q":
        return "Q"
    if "jack" in string or string=="j":
        return "J"
    if "ten" in string or string=="10" or string=="t":
        return "T"
    if "nine" in string or string=="9":
        return "9"
    if "eight" in string or string=="8":
        return "8"
    if "seven" in string or string=="7":
        return "7"
    if "six" in string or string=="6":
        return "6"
    if "five" in string or string=="5":
        return "5"
    if "four" in string or string=="4":
        return "4"
    if "three" in string or string=="3":
        return "3"
    if "two" in string or string=="2":
        return "2"
    else:
        return None

def get_suiting(string):
    """
    Parses a string representing the suiting (suited/offsuit) of the player's 
    two hole cards. Returns a string in the correct form for the lookup table.
    Returns None if the input could not be parsed.
    """
    if "of" in string or "un" in string:
        # handles offsuit, unsuited, etc.
        return "offsuit"
    elif "suit" in string:
        return "suited"
    else:
        return None

def get_players(string):
    """
    Parses a string representing the number of other players (i.e. excluding 
    the player) in the round. Currently supports only 1-9 other players. 
    Returns a string in the correct form for the lookup table.
    Returns None if the input could not be parsed.
    """
    if "nine" in string or string=="9":
        return "9"
    if "eight" in string or string=="8":
        return "8"
    if "seven" in string or string=="7":
        return "7"
    if "six" in string or string=="6":
        return "6"
    if "five" in string or string=="5":
        return "5"
    if "four" in string or string=="4":
        return "4"
    if "three" in string or string=="3":
        return "3"
    if "two" in string or string=="2":
        return "2"
    if "one" in string or string=="1":
        return "1"
    else:
        return None

@app.route("/", methods=['GET', 'POST'])
def respond():
    """
    Handle incoming messages.
    Assumption: message is a string of form
    RANK RANK SUITING OTHER_PLAYERS
    where RANK is the rank of each hole card, SUITING describes whether
    the hole cards are suited or offsuit, and OTHER_PLAYERS is the number of
    other players (i.e. excluding the player) in this round. These four
    components are assumed to be ordered as above, and space-separated.
    """

    # initialize twilio response
    resp = twilio.twiml.Response()

    # retrieve message. 
    received_message = request.values.get('Body').strip().lower()
    message_list = filter(lambda x: x != '', received_message.split(" "))

    # handle the "examples" case.
    if "example" in received_message:
        ex1 = "SEVEN EIGHT SUITED one"
        ex2 = "7 ace offsuit 9"
        resp.message(ex1 + "\n\n" + ex2)
        return str(resp)
    
    # otherwise, message_list has to contain exactly four items.
    if len(message_list) != 4:
        resp.message(STANDARD_ERRORMSG)
        return str(resp)

    # handle the described poker hand.
    rank1 = get_rank(message_list[0])
    rank2 = get_rank(message_list[1])
    suiting = get_suiting(message_list[2])
    players = get_players(message_list[3])

    # check that all the parsed input is valid
    if players==None:
        resp.message("Error! Only 1-9 other players are currently supported.")
        return str(resp)
    if any(map(lambda x: x==None, [rank1, rank2, suiting])):
        resp.message(STANDARD_ERRORMSG)
        return str(resp)
    if rank1==rank2 and suiting == "suited":
        resp.message("Error! It is impossible to have a suited pair. Did you mean offsuit?")
        return str(resp)

    # determine which of {rank1, rank2} is higher-ranked.
    # in the lookup table, hands are indexed in form RANK1 RANK2 where RANK1 <= RANK2.
    if ranks.index(rank1) <= ranks.index(rank2):
        lower, higher = rank1, rank2
    else:
        lower, higher = rank2, rank1

    # get the right lookup table
    lookup_table = "lookup-tables/lookup-table-" + players
    
    with open(lookup_table,"r") as lookup:
        for line in lookup:
            # line[4] is going to be 'o' or 's' for offsuit/suited, respectively
            if line[0]==lower and line[2]==higher and line[4]==suiting[0]:
                split_line = line.strip().split("\t")
                # convert to percentage for easier reading
                p_win = "P(win): " + str(float(split_line[3]) * 100) + "%\n"
                p_tie = "P(tie): " + str(float(split_line[4]) * 100) + "%\n"
                expected_gain = "Expected unit gain: " + split_line[5]
                resp.message(p_win + p_tie + expected_gain)
                return str(resp)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    # Debugging disabled for production build. 
    app.run(host='0.0.0.0', port=port, debug=False)
