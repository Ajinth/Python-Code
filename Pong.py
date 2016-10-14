########################################################################################################################
#Implementation of the Classic Arcade Game Pong
#Import the needed libraries  
import simplegui
import random

##############################################################################################
# Initialize global Variables
WIDTH = 600
HAlF_WIDTH = WIDTH/2
HEIGHT = 400
HALF_HEIGHT = HEIGHT/2
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
left = False
right = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [random.randrange(60, 180)/60,random.randrange(120, 240)/60]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0 
score2 = 0 
first_choice = random.randrange(1,3)

##############################################################################################
#Function to initialize all global variables, this will be called by the Restart Button 
def new_game():
    global paddle1_pos
    global paddle2_pos
    global score1
    global score2
    global first_choice
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    score1 = 0 
    score2 = 0
    first_choice = random.randrange(1,3)
    spawn_ball(first_choice)
    pass

#############################################################################################
# Initialize ball_pos and ball_vel for new bal in middle of table
# If direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(right):
    global ball_pos 
    global ball_vel
    #print right
    ball_pos = [WIDTH/2,HEIGHT/2]
    ball_vel[1] = -random.randrange(60, 180)/60
    if right == 1:
        ball_vel[0] = random.randrange(120, 240)/60
    else:
        ball_vel[0] = -random.randrange(120, 240)/60
    pass

############################################################################################## 
    # Draw Event Handler
def draw(canvas):
    global score1 
    global score2 
    global paddle1_pos 
    global paddle2_pos 
    global BALL_POS 
    global BALL_VEL 
    global paddle2_vel 
    global paddle1_vel
    
    ############################################################################################## 
    # Draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Yellow")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Green")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "Red")
        
    ############################################################################################## 
    # Update Ball Position based on velocity 
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    ############################################################################################## 
    #Check to make the ball bounce of the top and bottom walls
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS) or ball_pos[1] <= (BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    else:
        pass
    
    ##############################################################################################
    #Check bounce fail on the Right wall and increment score2, else increment speed by 10%   
    if ball_pos[0] >= (WIDTH - BALL_RADIUS -PAD_WIDTH):
       if ball_pos[1] < (paddle2_pos - HALF_PAD_HEIGHT) or ball_pos[1] > (paddle2_pos + HALF_PAD_HEIGHT): 
            score1 = score1 + 1
            spawn_ball(False)
       else:
                ball_vel[0] = -ball_vel[0]* 1.1
    ##############################################################################################
    #Check bounce fail on the left wall and increment score2, else increment speed by 10%
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
       if ball_pos[1] < (paddle1_pos - HALF_PAD_HEIGHT) or ball_pos[1] > (paddle1_pos + HALF_PAD_HEIGHT): 
            score2 = score2 + 1
            spawn_ball(True)
       else:
               ball_vel[0] = -ball_vel[0] * 1.1
    

    #####################################################################################################################
    # Code to Draw the ball based on position
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,'Yellow','Yellow')
    
    #####################################################################################################################
    # Calculating the paddle 2 position to keep it inside the screen
    if ((paddle2_pos < HALF_PAD_HEIGHT) and paddle2_vel < 0):
        paddle2_vel = 0
    if ((paddle2_pos + HALF_PAD_HEIGHT) > HEIGHT and paddle2_vel > 0):
        paddle2_vel = 0
    
    #####################################################################################################################    
    # Calculating the paddle 1 position to keep it inside the screen
    if ((paddle1_pos < HALF_PAD_HEIGHT) and paddle1_vel < 0):
        paddle1_vel = 0
    if ((paddle1_pos + HALF_PAD_HEIGHT) > HEIGHT and paddle1_vel > 0):
        paddle1_vel = 0
    
    #####################################################################################################################    
    #New Position for the Right paddle 
    paddle2_pos = paddle2_pos + paddle2_vel
    
    #####################################################################################################################
    #New Position for the Left paddle 
    paddle1_pos = paddle1_pos + paddle1_vel
    
    #####################################################################################################################
    # Draw paddles
    #Drawing the Left Paddle 
    canvas.draw_polygon([(0,paddle1_pos - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), 
                        (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (0, paddle1_pos + HALF_PAD_HEIGHT)],
                        1, 'Green', 'Green')
    
    #Drawing the Right Paddle
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT),(WIDTH , paddle2_pos - HALF_PAD_HEIGHT), 
                         (WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)],
                        1, 'Red', 'Red')
    #####################################################################################################################
    # Draw scores
    canvas.draw_text(str(score1), (170, 50), 35, "Green")
    canvas.draw_text(str(score2), (400, 50), 35, "Red")
    
    
#####################################################################################################################
#Validating the DOWN key strokes for Paddle_1 & Paddle_2
def keydown(key):
    global paddle1_vel
    global paddle2_vel
    
    if key == simplegui.KEY_MAP['w']: 
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP['s']: 
        paddle1_vel = 4
    if key == simplegui.KEY_MAP['up']: 
        paddle2_vel = -4
        
    if key == simplegui.KEY_MAP['down']: 
        paddle2_vel = 4
        
#####################################################################################################################
#Validating the UP key strokes for Paddle_1 & Paddle_2
def keyup(key):
    global paddle1_vel
    global paddle2_vel
    
    if key == simplegui.KEY_MAP['w']: 
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']: 
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['up']: 
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']: 
        paddle2_vel = 0    
    
#####################################################################################################################
# Create frame
frame = simplegui.create_frame("Week 4 - Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart Game',new_game, 100)
#####################################################################################################################
# Start Frame and also the game on Frame load
frame.start()
spawn_ball(1)