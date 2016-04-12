# PokerTexter

This is the source code for PokerTexter, an SMS app that gives you an advantage when playing Texas Hold 'Em. Running the app will let you text the PokerTexter phone number with your cards and number of other players, and it texts you back some pre-flop statistics:
* % Chance of Winning
* % Chance of Tying
* Expected Unit Gain: suppose you bet $1, everyone else bets $1 each, and no further bets are made. The expected unit gain is the average amount of money you expect to win (with those two cards and that number of players).

For example: suppose you're playing Poker with three other people. You draw a nine of hearts and a seven of clubs. You text PokerTexter that you have a nine and a seven unsuited with three other players. It texts you back that your probability of winning the hand is 21.52%, your probability of tying is 2.82%, and your expected unit gain is -0.111. Since the expected unit gain is quite negative, it would be unwise to play the hand.

![Example of Use][https://raw.githubusercontent.com/Datamine/PokerTexter/master/example.png]

# Notes and Terminology

* Some people play Poker *suited*, which is when Spades, Hearts, Clubs, and Diamonds are all ranked, and their ranking is used to break ties. PokerTexter does not support suited play.
* 

what you need to do

1. make a twilio account
2. get a twilio phone number
3. register your phone number w twilio so your bot can talk to it
4. make a heroku account
5. install virtualenv (actally necessary?)
6. install heroku toolbelt
7. heroku login
8. git init .
9. git add *
10. git commit -m "ghshdsd"
11. heroku create
12. git push heroku master
13. heroku ps:scale web=1
14. heroku logs --tail to check
15. set the phone number/messaging to ur severs url
16. text to ur twilio phone number

nb the calculator is UNSUITED

results verified w http://www.pokernews.com/poker-tools/poker-odds-calculator.htm

---

note that these probabilities change w number of players: e.g. 9K offsuit is ok in 2-player, but bad in 9-player.a


## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
