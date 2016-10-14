#Week 2 Mini Project - Guess The Number" 
#Importing the needed libraries 

import simplegui
import math
import random

# Global Variable Initialization
range_low_limit = 0 
range_high_limit = 100
guess_count = math.ceil(math.log(range_high_limit, 2))
correct_number = random.randint(range_low_limit, range_high_limit)

# Function to start a new_game after completing a previous game
def new_game():
    if range_high_limit == 100:
        range100()
    else: 
        range1000()

# Functions definitions for range and input processing
def range100():
    print " " 
    global range_low_limit
    global range_high_limit
    global guess_count
    global correct_number
    range_high_limit = 100
    correct_number = random.randint(range_low_limit, range_high_limit)   
    str_range_low_limit = str(range_low_limit)
    str_range_high_limit = str(range_high_limit)
    guess_count = math.ceil(math.log(range_high_limit, 2))
    print "New Game. Range is from " + str_range_low_limit + " to " + str_range_high_limit
    print "Number of remaining guess is: ",guess_count 
    
    
def range1000():
    print " "
    global range_low_limit
    global range_high_limit
    global guess_count
    global correct_number
    range_high_limit = 1000
    correct_number = random.randint(range_low_limit, range_high_limit)    
    str_range_low_limit = str(range_low_limit)
    str_range_high_limit = str(range_high_limit)
    guess_count = math.ceil(math.log(range_high_limit, 2))
    print "New Game. Range is from " + str_range_low_limit + " to " + str_range_high_limit
    print "Number of remaining guess is: ",guess_count 
    
def input_guess(guess):
    global range_low_limit
    global range_high_limit
    global guess_count
    global correct_number
    guess_float = int(guess)
    guess_count = guess_count - 1
    if guess_float == correct_number:
        a.set_text("")
        print "Guess was", guess_float
        print "Correct"
        print " "
        new_game()
        return None
    elif guess_float > correct_number:
        a.set_text("")
        print "Guess was", guess_float
        print "Lower!"
        print " "
        
    else: 
        a.set_text("")
        print "Guess was", guess_float
        print "Higher"
        print " " 
    if guess_count > 0: 
        print "Number of remaining guess is: ",guess_count    
    else:
        print "You ran out of Guesses. The number is: ", correct_number
        print " " 
        new_game()
       
    
# create frame
proj_frame = simplegui.create_frame("Guess the number", 400, 400)


# register event handlers for control elements
a=proj_frame.add_input("Enter a number", input_guess, 100)
play_range_100 = proj_frame.add_button("Range 0 to 100", range100)
play_range_1000 = proj_frame.add_button("Range 0 to 1000", range1000)


# call new_game and start frame
proj_frame.start()
range100()

