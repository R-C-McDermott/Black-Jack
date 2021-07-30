'''
 - BLACK JACK v1.11 -

 By Ryan C. McDermott

*v1.0*
- Functioning player, dealer and table objects (1 player so far).
- Betting system.

*v1.1*
- Player now has the choice to double down.
- Betting system now pays out depending on proper Black Jack odds.
- Fixed dealer hit bug where an infinite loop would occur at 17.

*v1.11*
- Card value now displays (soft value/hard value) for hands with aces.
- Fixed the blackjack win rules - now detects blackjack win before
main hit/stand loop.
- No longer win 2.5 times bet for simply having 21, you now need to have
blackjack.
- Now reveals one card from the dealer's hand at beginning of every round.

* TO ADD *
- Multiplayer system.
- Option to split.

'''
import random # to be used for shuffling

# Card suits and values
suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
values = [x for x in range(1,14)]

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def show(self):
        card_value = self.number
        if card_value == 1:
            card_value = "Ace"
        if card_value == 11:
            card_value = "Jack"
        if card_value == 12:
            card_value = "Queen"
        if card_value == 13:
            card_value = "King"
        print(f"{card_value} of {self.suit}")

    # def hardSoftValue(self):
    #     if self.number == 1:
    #         return

class Deck:
    def __init__(self):
        self.cards = []
        self.buildDeck()

    def deckSize(self):
        return len(self.cards)

    def buildDeck(self):
        for i in suits:
            for j in values:
                self.cards.append(Card(i, j))

    def printDeck(self):
        for c in self.cards:
            c.show()

    def drawCard(self):
        return self.cards.pop()

    def shuffleDeck(self):
        random.shuffle(self.cards)


class Player:
    def __init__(self):
        self.hand = []

    def draw(self, deck, number_of_cards):
        for i in range(number_of_cards):
            self.hand.append(deck.drawCard())

    def showHand(self):
        for h in self.hand:
            h.show()
        if self.cardValueCount()[0] == self.cardValueCount()[1]:
            print(f"Hand value: {self.cardValueCount()[0]}")
        elif self.cardValueCount()[1] < 21:
            print(f"Hand value: ({self.cardValueCount()[0]}/{self.cardValueCount()[1]})")
        elif self.cardValueCount()[1] > 21:
            print(f"Hand value: {self.cardValueCount()[0]}")
        elif self.cardValueCount()[1] == 21:
            print(f"Hand value: {self.cardValueCount()[1]}")



    def cardValueCount(self):

        '''
        The cardValueCount function iterates through the players current
        hand and converts Jack, Queen and King (11, 12, 13) to 10.

        The function also returns a soft and hard value for hands if
        any aces are to appear. It works by creating two seperate lists -
        soft_value and hard_value and summing each list to get the total hand
        value. It also counts the number of aces while iterating in order to
        avoid bugs with multiple aces in the players hand, leading to the
        function giving both extremes i.e. 2, 22 for 2 aces as opposed to
        2, 12 as you would say in a normal game of blackjack.

        '''
        card_value = [j.number for j in self.hand]
        soft_value = []
        hard_value = []
        ace_count = 0
        for i in range(len(card_value)):
            if card_value[i] > 10:
                soft_value.append(10)
                hard_value.append(10)
            elif card_value[i] == 1 and ace_count == 0:
                soft_value.append(1)
                hard_value.append(11)
                ace_count += 1
            elif card_value[i] == 1 and ace_count > 0:
                soft_value.append(1)
                hard_value.append(1)
            else:
                soft_value.append(card_value[i])
                hard_value.append(card_value[i])
        return sum(soft_value), sum(hard_value)

    def softOrHardVal(self):
        if self.cardValueCount()[1] > 21:
            return self.cardValueCount()[0] # Returns soft value if hard > 21
        else:
            return self.cardValueCount()[1] # Returns hard value if < 21

class Human(Player):
    def __init__(self, name, chips):
        super().__init__()
        self.name = name
        self.chips = chips
        self.bet = 0

    def showChips(self):
        print(f"Remaining balance: {self.chips}")

    def playBet(self):
        player_bet = int(input("How much would you like to bet?: "))
        try:
            if player_bet > self.chips:
                print("You don't have enough chips to place that bet!")
                self.playBet()
            else:
                self.bet += player_bet
                self.chips -= player_bet
                return player_bet
        except ValueError:
            print("Invalid input")

    def playerHitStand(self, deck):
        '''
        For simplicity, the function checks whether the player has sufficient
        funds in order to offer a double down choice... If not the function
        simply asks the user to hit or stand.

        '''

        if len(self.hand) == 2 and self.chips >= self.bet:
            player_choice = str(input("Would you like to hit, stand or double down? (H/S/D): "))
            player_choice = player_choice.strip().upper()
        else:
            player_choice = str(input("Would you like to hit or stand? (H/S): "))
            player_choice = player_choice.strip().upper()
        try:
            if player_choice == "H":
                self.draw(deck, 1)
                return False, player_choice
            if player_choice == "D":
                self.draw(deck, 1)
                return True, player_choice
            if player_choice == "S":
                return True, player_choice
            if player_choice not in ["H", "S", "D"]:
                print("Invalid input - Use H (Hit) or S (Stand)")
                self.playerHitStand(deck, number_of_cards=1)
        except ValueError:
            print("Invalid input - Use H (Hit) or S (Stand)")
            self.playerHitStand(deck)



class Dealer(Player):
    def __init__(self):
        super().__init__()

    def dealerHit(self, deck):
        while True:
            if self.softOrHardVal() < 17:
                self.draw(deck, 1)
            if self.softOrHardVal() >= 17:
                break

    def initialShow(self):
        self.hand[0].show()
        print("<Hidden card>")

class Table:
    def __init__(self):
        self.players = []

    def addPlayer(self):
        try:
            p_name = input("Please enter your name:\n>")
            starting_chips = int(input("Starting chips:\n>"))
            self.players.append(Human(p_name, starting_chips))
        except ValueError:
            print("Incorrect input - chips must be integer value ... Try again")
            self.addPlayer()

    def playRound(self, dealer, deck):

        # Reset variables for new round
        round_over = False
        player_done = False
        player = self.players[0]
        player.hand = []
        player.bet = 0
        dealer.hand = []
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # Deck shuffling, player bet and initial 2 card draw for player and dealer
        print("\nShuffling deck...\n")
        deck.shuffleDeck()
        player.showChips()
        player.bet = player.playBet()
        print(f"\nPlayer's bet: {player.bet}\n")
        player.showChips()
        player.draw(deck, 2)
        dealer.draw(deck, 2)

        print("\n~~~~~~~~ PLAYER'S HAND ~~~~~~~~\n")
        player.showHand()
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        print("\n~~~~~~~~ DEALER HAS ~~~~~~~~~~~\n")
        dealer.initialShow()
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        if player.cardValueCount()[1] == 21:
            print("Blackjack!")
            player.chips += int(2.5*player.bet) # 3/2 odds for blackjack win plus original bet
            player_done = True
            round_over = True
        # Loop for player's turn
        while player_done == False:
            choice = player.playerHitStand(deck)

            # Check for double down
            player_done = choice[0]
            if choice[1] == "D":
                player.chips -= player.bet
                player.bet *= 2
                print(f"\nPlayer's bet: {player.bet}\n")
                player.showChips()
            # ~~~~~~~~~~~~~~~~~~~ #

            print("\n~~~~~~~~ PLAYER'S HAND ~~~~~~~~\n")
            player.showHand()
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            if player.cardValueCount()[0] > 21:
                print("Burst!")
                player_done = True
                round_over = True
            elif player.softOrHardVal() == 21:
                print("You have 21")
                player_done = True
            elif player.cardValueCount()[0] < 21:
                pass
        # __________________________ #

        # Dealer plays until hand value is greater than 17
        if round_over == False:
            dealer.dealerHit(deck)
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                  "\n\nDealer's Turn...\n\n"
                  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            dealer.showHand()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # Winning and payout conditions
            if dealer.cardValueCount()[0] > 21:
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nDealer is burst! Player wins!")
                player.chips += 2*player.bet # 1/1 odds for winning plus original bet
                round_over = True
            elif dealer.softOrHardVal() > player.softOrHardVal():
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nDealer wins!")
                round_over = True
            elif player.softOrHardVal() > dealer.softOrHardVal():
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nPlayer wins!")
                player.chips += 2*player.bet # 1/1 odds for winning plus original bet
                round_over = True
            elif dealer.softOrHardVal() == player.softOrHardVal():
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nIt's a draw!")
                player.chips += player.bet # return chips to player
                round_over = True
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # Ask user if they would like to play another round
        if player.chips == 0:
            print("\nYou've lost all of your chips!\nBetter luck next time\n")
            print("\n~~~ Thank you for playing! ~~~\n")
        else:
            try:
                play_again = str(input("\nWould you like to play another round? (y/n)\n>"))
                play_again = play_again.strip().lower()
                if play_again == "y":
                    self.playRound(deck=Deck(), dealer=Dealer()) # Using fresh deck object
                if play_again == "n":
                    print("\n~~~ Thank you for playing! ~~~\n")
            except ValueError:
                print("Invalid input, please use 'y' (yes) or 'n' (no)")

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Functions for multiple players ... to be used for later versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def playerCountInput(self):
        try:
            player_number = int(input("How many players are joining the table?:\n>"))
            return player_number
        except ValueError:
            print("Incorrect input - number of players must be an integer value ... Try again")
            self.playerCount()

    def countPlayers(self):
        return len([players for players in self.players]

'''



def main():
    # Create table object
    game = Table()

    # Add player to game
    game.addPlayer()

    # Game loop and initialise dealer and deck objects
    game.playRound(dealer=Dealer(), deck=Deck())


if __name__ == '__main__':
    main()
