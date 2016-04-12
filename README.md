# PokerTexter

*The documentation for this app is also [on my website](http://www.johnloeber.com/docs/pokertexter.html).*

This repository contains source code and setup instructions for PokerTexter, an SMS app that gives you an advantage when playing Texas Hold 'Em. Running the app will let you text the PokerTexter phone number with your cards and number of other players, and it texts you back some pre-flop statistics:
* % Chance of Winning
* % Chance of Tying
* Expected Unit Gain: suppose you bet $1, everyone else bets $1 each, and no further bets are made. The expected unit gain is the average amount of money you expect to win (with those two cards and that number of players).

For example: suppose you're playing Poker with three other people. You are dealt a nine of hearts and a seven of clubs. You message PokerTexter that you have a nine and a seven unsuited with three other players. It texts you back that your probability of winning the hand is 21.52%, your probability of tying is 2.82%, and your expected unit gain is -0.111. Since the expected unit gain is negative, i.e. on average you will lose $0.111 on a bet of $1, it would be unwise to play the hand.

![Example of Use](https://raw.githubusercontent.com/Datamine/PokerTexter/master/example.png)


## Notes and Terminology

* Some people play Poker *suited*, which is when Spades, Hearts, Clubs, and Diamonds are all ranked, and their ranking is used to break ties. PokerTexter does not support suited play.
* Though in theory, anywhere between 2 and 23 people can play Texas Hold 'Em, PokerTexter currently supports only between 2 and 10 players (these are standard numbers of players). Extending the script to support up to 23 players would be easy, but it hasn't been done yet because this use case seems exceedingly rare.
* To verify the results offered by this app, I cross-referenced the lookup tables against the Flash Poker Odds Calculator located [here](http://www.pokernews.com/poker-tools/poker-odds-calculator.htm).

## Components

Following is a list of files in this repository and notes on what they're for:
* `destroy.sh`: destroys all created Heroku apps. If you're having trouble launching, then you may in the process create lots of apps. This script clears them up.
* `launch.sh`: launches the Heroku app and scales it with one dyno [worker]. Once you've done this, you can use PokerTexter from your phone.
* `lookup-table-n`: this is a lookup table, mapping any starting hand (on a table with *n* players) to probabilities and expected gains.
* `Procfile`: necessary for the Heroku app to run.
* `requirements.txt`: requirements for `run-pokertexter.py`. Heroku needs the requirements, so as to install any necessary packages for the app.
* `deprecated`: folder containing items that are not essential to `run-pokertexter.py`.
* `deprecated/generate-lookup-table.py`: for a number of players *n*, generate `lookup-table-n`. Relies on the `deuces` library.
* `deprecated/deuces`: the [deuces library](https://github.com/worldveil/deuces).

## Launch Instructions

Following are the steps you need to take to get PokerTexter to run. Note that these instructions are dated April 12, 2016: certain steps may change if Twilio or Heroku adjust their products or infrastructure in any way.

1. Make a [Twilio](https://www.twilio.com/) account.
2. Get a Twilio phone number. It's free.
3. Register your personal mobile phone number with Twilio. You need to have "whitelisted" your number so you can communicate with the Twilio phone number. (I believe this restriction is in place to prevent abuse of Twilio's free service.)
4. Make a [Heroku](https://www.heroku.com/) account.
5. Open up your terminal and download this repository: `git clone https://github.com/Datamine/PokerTexter` and `cd` into it.
6. Install the [Heroku Toolbelt](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) and login to Heroku.
7. While in `PokerTexter`, type `heroku create`. This creates a Heroku app.
8. Then type `git push heroku master`. Note that you do not have to take the usual prior steps of `git init; git add *; git commit -m "asdf"` because you cloned a repository, which contains an already-setup `.git` folder.
9. The previous step generates some printed output. Toward the bottom there will be a line reading something like `remote:        http://lit-bastion-5032.herokuapp.com/ deployed to Heroku`. (The name between `http://` and `.herokuapp.com` is a unique identifier. Yours will be different.) This is the URL at which your Heroku app is accessible.
10. Go to your [Twilio Numbers Page](https://www.twilio.com/user/account/phone-numbers/incoming) and click on your Twilio phone number. You'll get a page where you can set various settings for that number. Toward the bottom there will be a *Messaging* subheader, and a field *Request URL*. Copy-paste your Heroku app's URL (from the previous step) into this field and save your changes.
11. Go back to your terminal, and type `heroku ps:scale web=1` to add a worker.
12. You can check the status of your app with `heroku logs --tail`.

If you make any changes to `run-pokertexter.py` or to any of the other files in `PokerTexter`, you will need to relaunch the app for the changes to propagate. You can relaunch easily by typing `./launch`. No other steps will be necessary, **unless** you create a new Heroku app and thereby create a new Heroku app URL, in which case you'll need to amend your Twilio Numbers Page appropriately.

## Remarks

While the probabilities of winning and tying scale as you would expect in the number of players, the expected gains change sign in some cases. For example, if you're playing with nine other players, a 9-K offsuit has an expected gain of -0.0036. It would be inadvisable to play that hand. However, if you're playing with two other players, a 9-K offsuit has an expected gain of 0.184. You'd want to play that hand.

This instruction set assumes that you're using the Twilio free trial. Regrettably, to remind you that you're on their "free" tier, they prepend "Sent from your Twilio trial account -" to every text message that PokerTexter sends. You can easily fix this by upgrading from Twilio free to Twilio Hobby, but that costs $7 a month.

The scope of this app is currently quite limited: it doesn't permit you to submit cards beyond your initial two. It is easily possible to also support additional known cards (e.g. cards on the table, known burned cards, etc.) but the usefulness of such features is limited because additional cards are made known only in the later stages of the game, when probability can be more easily intuitively approximated (it's easy to figure out your outs and their approximate odds), and the psychological aspect of the game becomes more important. Nonetheless, I aim to add such features in the near future.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
