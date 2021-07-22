'''
 - BLACK JACK v1.0 -

 By Ryan C. McDermott

*v1.0*
- Functioning player and dealer (1 player so far)
- Betting system

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
        print(f"Hand value: {self.cardValueCount()}")


    def cardValueCount(self):
        card_value = [j.number for j in self.hand]
        new_value = []
        for i in range(len(card_value)):
            if card_value[i] > 10:
                new_value.append(10)
            else:
                new_value.append(card_value[i])
        return sum(new_value)

class Human(Player):
    def __init__(self, name, chips):
        super().__init__()
        self.name = name
        self.chips = chips
        #self.bet = 0

    def showChips(self):
        print(f"Remaining balance: {self.chips}")

    def playBet(self):
        player_bet = int(input("How much would you like to bet?: "))
        try:
            if player_bet > self.chips:
                print("You don't have enough chips to place that bet!")
                self.playBet()
            else:
                #self.bet += player_bet
                self.chips -= player_bet
                return player_bet
        except ValueError:
            print("Invalid input")

    def playerHitStand(self, deck):
        player_choice = str(input("Would you like to hit or stand? (H/S): "))
        player_choice = player_choice.strip().upper()
        try:
            if player_choice == "H":
                self.draw(deck, 1)
                return False
            if player_choice == "S":
                return True
            if player_choice not in ["H", "S"]:
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
            if self.cardValueCount() < 17:
                self.draw(deck, 1)
            if self.cardValueCount() > 17:
                break


class Table:
    def __init__(self):
        self.players = []

    def playerStatus(self, player):
        if player.cardValueCount() > 21:
            print("Burst!")
            return True
        if player.cardValueCount() == 21:
            print("Blackjack!")
            return True
        if player.cardValueCount() < 21:
            pass

    def addPlayer(self):
        try:
            p_name = input("Please enter your name:\n>")
            starting_chips = int(input("Starting chips:\n>"))
            self.players.append(Human(p_name, starting_chips))
        except ValueError:
            print("Incorrect input - chips must be integer value ... Try again")
            self.addPlayer()

    def playRound(self, dealer, deck):
        round_over = False
        player_done = False
        player = self.players[0]
        player.hand = []
        dealer.hand = []
        print("\nShuffling deck...\n")
        deck.shuffleDeck()
        player.showChips()
        player_bet = player.playBet()
        player.draw(deck, 2)
        dealer.draw(deck, 2)
        while player_done == False:
            print("\n~~~~~~~~ PLAYER'S HAND ~~~~~~~~\n")
            player.showHand()
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            player_done = player.playerHitStand(deck)
            print("\n~~~~~~~~ PLAYER'S HAND ~~~~~~~~\n")
            player.showHand()
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            if player.cardValueCount() > 21:
                print("Burst!")
                player_done = True
                round_over = True
            if player.cardValueCount() == 21:
                print("Blackjack!")
                player.chips += int(2.5*player_bet) # 3/2 odds for blackjack win plus original bet
                player_done = True
                round_over = True
            if player.cardValueCount() < 21:
                pass

        if round_over == False:
            dealer.dealerHit(deck)
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                  "\n\nDealer's Turn...\n\n"
                  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            dealer.showHand()
            if dealer.cardValueCount() > 21:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nDealer is burst! Player wins!")
                player.chips += int(2*player_bet) # 1/1 odds for winning plus original bet
                round_over = True
            elif dealer.cardValueCount() > player.cardValueCount():
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nDealer wins!")
                round_over = True
            elif player.cardValueCount() > dealer.cardValueCount():
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nPlayer wins!")
                player.chips += int(2*player_bet) # 1/1 odds for winning plus original bet
                round_over = True
            elif dealer.cardValueCount() == player.cardValueCount():
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                      "\nIt's a draw!")
                player.chips += player_bet # return chips to player
                round_over = True

        try:
            play_again = str(input("\nWould you like to play another round? (y/n)\n>"))
            play_again = play_again.strip().lower()
            if play_again == "y":
                self.playRound(deck=Deck(), dealer=Dealer()) # Using fresh deck object
            if play_again == "n":
                print("\n~~~ Thank you, for playing! ~~~\n")
        except ValueError:
            print

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
    # Create table, dealer and deck objects
    game = Table()

    # Add player to game and shuffle deck
    game.addPlayer()

    # Game loop
    game.playRound(dealer=Dealer(), deck=Deck())

if __name__ == '__main__':
    main()
