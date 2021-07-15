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

    def cardValueCount(self):
        card_value = [i.number for i in self.hand]
        for i in range(len(card_value)):
            if card_value[i] > 10:
                card_value[i] = 10
            else:
                pass
        return sum(card_value)



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
                self.bet()
            else:
                self.bet += player_bet
                self.chips -= player_bet
                return player_bet
        except ValueError:
            print("Invalid input")

    def playerHitStand(self, deck, number_of_cards=1):
        player_choice = str(input("Would you like to hit or stand? (H/S): "))
        player_choice = player_choice.strip().upper()
        try:
            if player_choice == "H":
                self.draw(deck, number_of_cards)
            if player_choice == "S":
                pass
            if player_choice not in ["H", "S"]:
                print("Invalid input - Use H (Hit) or S (Stand)")
                self.playerHitStand(deck, number_of_cards=1)
        except ValueError:
            print("Invalid input - Use H (Hit) or S (Stand)")
            self.playerHitStand(deck, number_of_cards=1)


class Dealer(Player):
    def __init__(self):
        super().__init__()

'''    def dealerHit(self):
        if self.hand'''


class Table:
    def __init__(self):
        self.players = []

# True and False statements to be used to return game over state (game over = True)

    def playerStatus(self, player):
        if player.cardValueCount() > 21:
            print("Burst!")
            return True
        if player.cardValueCount() == 21:
            print("Blackjack!")
            return True
        if player.cardValueCount() < 21:
            pass

    def addPlayer(self, player):
        self.players.append(player)



def main():
    # Create Player and Deck
    game = Table()
    p = Human("Ryan", 100)
    D = Dealer()
    d = Deck()
    d.shuffleDeck()

    game.addPlayer(p)

    p.draw(d, number_of_cards=3)
    p.showHand()
    game.playerStatus(p, d)
    print(f"{p.cardValueCount()}")





    # Check deck size again to ensure everything is working properly
    #print(f"Deck size: {d.deckSize()}")

if __name__ == '__main__':
    main()
