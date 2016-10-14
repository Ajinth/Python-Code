# Python-Coursera - "Stopwatch: The Game"
#########################################
# Import the needed libraries############
import simplegui

# define global variables
tick_counter = 0
a = 0
bc = 0
d = 0
x = 0
y = 0
str_a= '0'
str_bc= '00'
str_d= '0'
str_x ='0'
str_y ='0'
stopped = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(tick):
    global str_a
    global str_bc
    global str_d
    global d
    d=tick%10
    c1=tick//10
    c2=c1%60
    if c2<=9:
        bc="0"+str(c1%60)
    else:
        bc=c1%60
    a=c1//60
    str_d = str(d)
    str_bc = str(bc)
    str_a = str(a)
        
# define event handlers for Start Button 
def start_button_handler():
    global stopped
    if stopped == True:
        stopped = False
        timer.start()
        return stopped
      
# define event handlers for Stop Button 
def stop_button_handler():
    global y
    global x
    global str_x
    global str_y
    global stopped
    global d
    if stopped == False:
        timer.stop()
        stopped = True
        if d == 0:
            y = y + 1 
            x = x + 1
            str_y = str(y)
            str_x = str(x)
            return str_x, str_y
        else:
            y = y + 1 
            str_y = str(y)
            str_x = str(x)
            return str_x, str_y
    else: 
        return "The timer is already stopped" 

    
# define event handlers for Reset Button 
def reset_button_handler():
    timer.stop()
    global a 
    global bc
    global d
    global str_x
    global str_y
    global str_a
    global str_bc
    global str_d
    global x 
    global y
    a = 0
    bc = 0
    d = 0
    x = 0
    y = 0
    str_a= '0'
    str_bc= '00'
    str_d= '0'
    str_x = '0'
    str_y ='0'
    stopped = True



# define event handler for timer with 0.1 sec interval
def timer_tick():
    global tick_counter 
    tick_counter = tick_counter + 1
    format(tick_counter)



# define draw handler
def canvas_handler(canvas):
    canvas.draw_text(str_a+":"+str_bc+":"+str_d, [250, 250], 40, 'Red')
    canvas.draw_text(str_x+"/"+str_y, [400, 50], 40, 'Green')
    
    
# create frame
frame = simplegui.create_frame("Stopwatch", 500, 500)

# register event handlers
timer = simplegui.create_timer(100, timer_tick)
start_button = frame.add_button('Start', start_button_handler, 100)
stop_button = frame.add_button('Stop', stop_button_handler, 100)
reset_button = frame.add_button('Reset', reset_button_handler, 100)
canvas_boundary = frame.set_draw_handler(canvas_handler)

# start frame
frame.start()
