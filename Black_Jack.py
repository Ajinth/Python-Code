# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = None 
player = None 
dealer = None
message = ' ' 


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
        self.cards = []
        

    def __str__(self):
        result = 'Hand contains'
        
        for card in self.cards:
            result = result + ' ' + str(card)
        
        return result

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        ace_present = False
        
        for cards in self.cards: 
            value = value + VALUES[cards.get_rank()]
            
            if cards.get_rank() == 'A':
                ace_present = True
                
        if ace_present and value + 10 <= 21:
            value += 10
            
        return value
            
    def draw(self, canvas, pos):
        c = 0 
        for cards in self.cards: 
            cards.draw(canvas, [pos[0] + CARD_SIZE[0]*c, pos[1]])
            c = c + 1 
            
        
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        rep = 'Deck contains'
        
        for card in self.deck:
            rep += ' ' + str(card)
            
        return rep

#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, message
     
    if in_play:
        score -= 1
    
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    
    in_play = True
    outcome = "Do you want to HIT or STAND?"
    message = ' '
    
def hit():
    global outcome, message, score, in_play
    
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
    
    if player.get_value() > 21: 
        outcome = "NEW DEAL?"
        message = "YOU HAVE BEEN BUSTED"
        score += -1
        in_play = False
        
def stand():
    global in_play, score, outcome, message
    
    if player.get_value() > 21: 
        message = "YOU HAVE BEEN BUSTED"
        score += -1 
        in_play = False 
    
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
    
    if dealer.get_value() > 21: 
        message = "THE DEALER HAS BEEN BUSTED"
        score += 1 
    else: 
        if player.get_value() <=dealer.get_value():
            message = "THE DEALER WINS" 
            score -= 1
        else: 
            message = "NICE GAME, YOU WIN!" 
            score +=1
    
    outcome = "PLAY AGAIN?"
    
    in_play= False
    
    
# draw handler    
def draw(canvas):
    canvas.draw_text("BLACKJACK TABLE", (350, 50), 40, "Black")
    
    canvas.draw_text("DEALER", (50, 150), 30, "Black")
    canvas.draw_text("PLAYER", (50, 350), 30, "Black")
    
    canvas.draw_text(outcome, (250, 350), 30, "Black")
    canvas.draw_text(message, (250, 150), 30, "Black")
    
    canvas.draw_text("Score: " + str(score), (800, 150), 30, "Black")

    player.draw(canvas, [75, 400])
    dealer.draw(canvas, [75, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [75 + CARD_BACK_CENTER[0],
                           200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)    
    
def quit():
    frame.stop()
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 1000, 700)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Quit", quit, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric