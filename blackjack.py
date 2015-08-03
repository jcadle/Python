# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "test"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object

    def __str__(self):
        # return a string representation of a hand
        list = ""
        for card in self.cards:
            list += str(card)
            list += " "
        return "Hand contains " + list

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        aces = False
        value = 0
        for card in self.cards:
            value += VALUES[card.rank]
            if 'A' in card.rank:
                aces = True
        if aces and (value + 10) <= 21:
            return value + 10
        else:
            return value
        
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 72
            # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.stack = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.stack.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.stack) # use random.shuffle()

    def deal_card(self):
        return self.stack.pop(0) # deal a card object from the deck
    
    def __str__(self):
        output = ""
        for card in self.stack:
            output += str(card) # return a string representing the deck
            output += " "
        return "Deck contains " + output



#define event handlers for buttons
def deal():
    global outcome, in_play, playdeck, phand, chand, score
    if in_play:
        score -= 1
    playdeck = Deck()
    playdeck.shuffle()
    phand = Hand()
    chand = Hand()
    count = 0
    while count < 2:
        chand.add_card(playdeck.deal_card())
        phand.add_card(playdeck.deal_card())
        count += 1
    # your code goes here
    outcome = "Hit or Stand?"
    in_play = True

def hit():
    global in_play, outcome, score
    if in_play:
        phand.add_card(playdeck.deal_card())
        print phand.get_value()
    if phand.get_value() > 21:
        in_play = False
        outcome = "You Busted!"
        score -= 1
        
    
    # replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, score, outcome
    if in_play:
        while chand.get_value() <= 17:
            chand.add_card(playdeck.deal_card())
            
        if chand.get_value() > 21:
            score += 1
            outcome = "House busted! You win! New Deal?"
        elif chand.get_value() >= phand.get_value() and chand.get_value() <= 21:
            score -= 1
            outcome = "House wins! New Deal?"
        elif chand.get_value() < phand.get_value() and phand.get_value() <= 21:
            score += 1
            outcome = "You win! New Deal?"
        in_play = False
        # replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # card = Card("S", "A")
    # card.draw(canvas, [300, 300])
    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [300 + CARD_BACK_CENTER[0], 300 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    phand.draw(canvas, [100, 500])
    chand.draw(canvas, [100, 50])
    canvas.draw_text(outcome, [100, 450], 30, "White")
    canvas.draw_text("Score: " + str(score), [500, 25], 18, "White")
    canvas.draw_text("Blackjack", [200, 25], 28, "White")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 50 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    else:
        return
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
