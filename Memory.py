#Import the needed libraries 
import simplegui
import random

#Height and Width of Canvas
height = 100 
width = 800 
#Text Width and Height
text_start_height = 0.65*height 
text_start_width = width/16
#Line width between the decks
line_width = 3
#Width of Deck
deck_width = width/16
#Exposed
exposed = [False for i in range(16)]
#Correct
correct = [False for i in range(8)]
#Card Shuffle
cards = [(i % 8) for i in range(16)]
random.shuffle(cards)
#Game State
state = 0 
card1 = 0
card2 = 0
#first_j = 0 
#second_j = 0 
#Moves 
moves = 0


def init():
    global height, width, text_start_height, text_start_width, line_width, deck_width, exposed, correct, cards, state, card1, card2, moves

    #Height and Width of Canvas
    height = 100 
    width = 800 
    #Text Width and Height
    text_start_height = 0.65*height 
    text_start_width = width/16
    #Line width between the decks
    line_width = 3
    #Width of Deck
    deck_width = width/16
    #Exposed
    exposed = [False for i in range(16)]
    #Correct
    correct = [False for i in range(8)]
    #Card Shuffle
    cards = [(i % 8) for i in range(16)]
    random.shuffle(cards)
    #Game State
    state = 0 
    card1 = 0
    card2 = 0
    #first_j = 0 
    #second_j = 0 
    #Moves 
    moves = 0

def game_state(instance):
    global state, card1, card2, moves
    if state == 0: 
        state = 1
        moves += 1
        
    elif state == 1: 
        card2 = cards[instance]
        if card1 == card2:
            correct[cards[instance]] = True
        state = 2
        
    else:
        for x in range(16):
            if not correct[cards[x]]:
                exposed[x]= False
        moves += 1
        state = 1 
    l.set_text("Moves = " + str(moves))

def mouseclick(pos):
    global card1, exposed
    for j in range(16):
        if ((pos[0] > (j*deck_width) and pos[0] < ((j+1)* deck_width)) 
            and not exposed[j]):
            game_state(j)
            card1=cards[j]
            exposed[j] = True

def draw(canvas):
    global text_start_height, text_start_width
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(cards[i]), [text_start_width * i + text_start_width/2, 
                                         text_start_height ], 25, "White")
            canvas.draw_line((text_start_width * i, 0),(text_start_width * i, height),line_width, "White")
        
        else: 
            canvas.draw_text("?", [text_start_width * i + text_start_width/2, 
                                         text_start_height ], 35, "White")
            
            canvas.draw_line((text_start_width * i, 0),(text_start_width * i, height),line_width, "White")
        
    


frame = simplegui.create_frame("Memory Game:", width, height)
frame.add_button("Restart the Game:", init)
l = frame.add_label("Moves = 0")



frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


frame.start()
init()