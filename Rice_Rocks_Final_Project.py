# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
max_rocks=12
collisions=0


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.5)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)
    
def process_sprite_group(group, canvas):
    for element in set(group):
        element.draw(canvas)
        
        if element.update():
            group.remove(element)
    
def group_collide(group, other_object):
    collision = False
    for element in set(group):
        if element.collide(other_object):
            group.remove(element)
            collision = True
    return collision

def group_group_collide(group1, group2):
    collisions = 0
    for element in set(group1):
        if group_collide(group2, element):
            collisions += 1
            group1.discard(element)
            
    return collisions
        
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
        self.delta_angle = 0.08
        self.turning_left = False 
        self.turning_right = True 
        self.acceleration = 0.3
        self.friction = 0.04
        
    def draw(self,canvas):
        #Global Thrust
        ship_center=ship_info.get_center()
        ship_size = ship_info.get_size()
        ship_angle = self.angle
        #Code to draw the ship by dynamically passing the position of the ship
        if self.thrust:
            canvas.draw_image(ship_image, (ship_center[0]+ship_size[0], ship_center[1]), 
                              (ship_size), (self.pos[0], self.pos[1]), (ship_size), self.angle)
        else:
            canvas.draw_image(ship_image, (ship_center), 
                              (ship_size), (self.pos[0], self.pos[1]), (ship_size), self.angle)
            
    def update(self):
        if self.thrust:
            forward_movement = angle_to_vector(self.angle)
            self.vel[0] += forward_movement[0] * self.acceleration
            self.vel[1] += forward_movement[1] * self.acceleration
 
        self.vel[0] -= self.vel[0] * self.friction
        self.vel[1] -= self.vel[1] * self.friction
        #Updating the position of the ship based on the velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        #Keeping the ship inside the canvas 
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        #Updating the angle of orientation of the ship if the left key was pressed  
        self.angle += self.angle_vel
 
    def turn_left(self):
        self.turning_left = True
        self.angle_vel = - self.delta_angle
        
    def turn_right(self):
        self.turning_right = True
        self.angle_vel = self.delta_angle
        
    def start_thrust(self):
        self.thrust = True
        ship_thrust_sound.play()
    
    def stop_thrust(self):
        self.thrust = False
        ship_thrust_sound.rewind()

    def stop_turn(self, right = True):
        if right: 
            self.turning_right = False 
            self.angle_vel = 0
        else: 
            self.turning_left = False
            self.angle_vel = 0
    
    def shoot(self):
        #global missile_group
        forward = angle_to_vector(self.angle)
        missile_position = [self.pos[0] + (self.image_size[0] / 2) *  forward[0],
                            self.pos[1] + (self.image_size[1] / 2)* forward[1]]
        missile_velocity = [self.vel[0] + forward[0] * 5,
                            self.vel[1] + forward[1] * 5]
        a_missile = Sprite(missile_position,
                           missile_velocity,
                           0,
                           0,
                           missile_image,
                           missile_info,
                           missile_sound)
        missile_group.add(a_missile)
        #forward = angle_to_vector(self.angle)
        #missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        #missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        #missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        
    def get_position(self):
        return self.pos 
    
    def get_radius(self):
        return self.radius

class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
       canvas.draw_image(self.image, (self.image_center), 
                              (self.image_size), (self.pos), (self.image_size), self.angle)
    
    def update(self):
        self.pos[0] +=self.vel[0]
        self.pos[1] +=self.vel[1]
        
        self.pos[0] %=WIDTH
        self.pos[1] %=HEIGHT
        
        self.angle += self.angle_vel
        
        self.age += 1 
        #print self.lifespan
        if self.age >=self.lifespan:
            return True
        
        
    def get_position(self):
        return self.pos 
    
    def get_radius(self):
        return self.radius
            
    def collide(self, other_object):
        return (dist(self.get_position(), other_object.get_position())
                     <= self.get_radius() + other_object.get_radius())

           
def draw(canvas):
    global time,lives, score, rock_group, missile_group, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    score += group_group_collide(missile_group, rock_group)
    
    my_ship.update()
    
    if group_collide(rock_group, my_ship):
        lives -= 1
        
        if lives <= 0:
            started = False 
            rock_group = set([])
            missile_group = set([])
            soundtrack.pause()
            return
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())    
    
    
    canvas.draw_text("Score: " + str(score), (650, 20), 20, "White", "monospace")
    canvas.draw_text("Lives: " + ' X '  + str(lives), (10, 20), 20, "White", "monospace")
    
    
#Rock Spawner based on Timer    
def rock_spawner():
    if len(rock_group)>12 or not started:
        return
    else: 
        a_rock = Sprite((random.randrange(0,WIDTH), random.randrange(0, HEIGHT)), 
                    [random.choice([1, -1]), random.choice([1, -1])], 
                    random.choice([1, -1]), 
                    random.choice([1, -1]) * 0.05, 
                    asteroid_image, asteroid_info)
        
        if not a_rock.collide(my_ship):
            rock_group.add(a_rock)

#Keyup handler
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.stop_turn(False)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.stop_turn()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.stop_thrust()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

#KeyDown handler
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn_left()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.turn_right()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.start_thrust()

#Click Handler
def click(pos):
    global started, lives, rock_group, missile_group, score 
    size = splash_info.get_size()
    if not started: 
        started = True
        lives = 3
        score = 0 
        rock_group = set([])
        missile_group = set([])
        soundtrack.rewind()
        soundtrack.play()
        
        
        
        
#Frame Initialization
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# Ship Creation, RockGroup and Missile Group Initialization
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group=set([])
missile_group=set([])

#Handler Registration
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

#Start Timer and Frame 
timer.start()
frame.start()
#