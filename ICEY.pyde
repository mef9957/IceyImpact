add_library('minim')
import os
import random
import math 

# Global Variables
PATH = os.getcwd()
RESOLUTION_W = 1280
RESOLUTION_H = 960
ARENA_RAD = 440
ITEM_RAD = 35
ITEM_TYPE = ['Size','Coin','Speed','Coin']
# Force referes to how fast the ball will accerlerate. Force and mass together determine the physics of the balls.
DEFAULT_FORCE = 0.2
DEFAULT_MASS = 1
DEFAULT_RAD = 50
DEFAULT_X2 = RESOLUTION_W/2 - ARENA_RAD + 100
DEFAULT_Y2 = RESOLUTION_H/2
DEFAULT_X1 = RESOLUTION_W/2 + ARENA_RAD - 100
DEFAULT_Y1 = RESOLUTION_H/2
MAX_SPEED = 50
player = Minim(this)



class Ball:
    
    def __init__(self, x, y, r, colors):
        self.x = x
        self.y = y
        self.r = r
        self.colors = colors
        # color is initially used to to create a ball to check the physics, but is later replaced to become the type (as the attribute is a string)
              
    
    # the following code is the display function for the arena, snowballs, and items.
    def display(self):
        noStroke()
        if self.colors == 'arena':
            image(self.img, RESOLUTION_W/2-self.r-20, RESOLUTION_H/2-self.r-30)
            # fill(0, 200)
            # circle(self.x, self.y, self.r * 2)
        if self.colors == 'player':
            image(self.img, self.x-self.r, self.y-self.r, self.r*2 , self.r*2)
        if self.colors == 'item':
            if self.type == 'Coin':
                image(self.img, self.x - self.slice_w//2, self.y - self.slice_h//2, self.slice_w, self.slice_h, (self.slice * self.slice_w)/2, 0, ((self.slice + 1) * self.slice_w)/2, self.slice_h/2)
            else:
                image(self.img, self.x - self.slice_w//2-17.5, self.y - self.slice_h//2-17.5, self.slice_w*1.5, self.slice_h*1.5, (self.slice * self.slice_w), 0, ((self.slice + 1) * self.slice_w), self.slice_h)
        
        
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
class Arena(Ball):
    
    def __init__(self, x, y, r, colors):
        Ball.__init__(self, x, y, r, colors)
        self.img = loadImage(PATH +'/images/Arena.png')
    
    # check if a round is over. If a snowball falls, it loses. If it collects 3 coins it wins.
    def round_over(self, snowball):
        if self.distance(snowball) > self.r:
            return 'Lose'
        elif snowball.coin >= 3:
            return 'Win'
        else:
            return None
        
class Item(Ball):

    def __init__(self, x, y, r, colors, type):
        Ball.__init__(self, x, y, r, colors)
        self.type = type
        self.coin_sound = player.loadFile(PATH + "/sounds/coin.wav")
        self.power_sound = player.loadFile(PATH + "/sounds/powerup.wav")
        if type == 'Coin':
            self.img = loadImage(PATH +'/images/coin.png')
            self.num_slices = 10
            self.slice_w = ITEM_RAD*2
            self.slice_h = ITEM_RAD*2
            self.slice = 0
        else:
            self.img = loadImage(PATH +'/images/powerup.png')
            self.num_slices = 4
            self.slice_w = ITEM_RAD*2
            self.slice_h = ITEM_RAD*2
            self.slice = 0    
    
    # the following function detects collision between the balls.
    def collision(self, snowball):
        if self.distance(snowball) < self.r + snowball.r:
            return True
        else:
            return False
    
    # upgrade function. Notice that the upgrade function has 2/3 probability to increase speed/size, and 1/3 probability to decrease speed/size.
    def upgrade(self, snowball):
        if self.type == 'Coin':
            snowball.coin += 1
            self.coin_sound.rewind()
            self.coin_sound.play()
        if self.type == 'Size':
            self.power_sound.rewind()
            self.power_sound.play()
            temp =(-1)**(random.randint(0,2))
            print(temp)
            snowball.r = snowball.r * 1.4 **temp
            snowball.m = snowball.m * 2.744**temp
        if self.type == 'Speed':
            self.power_sound.rewind()
            self.power_sound.play()            
            temp =(-1)**(random.randint(0,2))
            print(temp)
            snowball.force = snowball.force * 1.5**temp
    
    # check how overlapped two balls are. This function is used when two snowballs touch one item in a frame and check which ball is closer to the items and get the upgrade.
    def overlap(self, snowball):
        return self.distance(snowball) -(self.r + snowball.r)
    
    # play the anime for the items
    def update(self):
        if self.type =='Coin':
            if frameCount % 3 == 0: 
                self.slice = (self.slice + 1) % self.num_slices
        else:
            if frameCount % 10 == 0: 
                self.slice = (self.slice + 1) % self.num_slices
    

    
    
    
    

    

class Snowball(Ball):
    
    def __init__(self, x, y, r, colors, num):
        Ball.__init__(self, x, y, r, colors)
        self.key_handler = [{LEFT:False, RIGHT:False, UP:False, DOWN:False}, {'a':False, 'd':False, 'w':False, 's':False}]
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.fric_force = -0.05
        self.force = DEFAULT_FORCE
        self.num = num
        self.m = DEFAULT_MASS
        self.score = 0
        self.coin = 0
        self.bounce_sound = player.loadFile(PATH + "/sounds/collision.wav")
        if self.num == 1:
            self.img = loadImage(PATH +'/images/sb_1.png') 
        else:
            self.img = loadImage(PATH +'/images/sb_2.png') 
        
   
    # reset the snowballs default attributes after each round 
    def reset(self):
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.r = DEFAULT_RAD
        self.force = DEFAULT_FORCE
        self.coin = 0
        if self.num == 1:
            self.x = DEFAULT_X1
            self.y = DEFAULT_Y1
        if self.num == 2:
            self.x = DEFAULT_X2
            self.y = DEFAULT_Y2
        
    
        
    
    # This is the distance between the two balls one frame later so we detect collision one frame before the collision happen
    def update_distance(self, other):
        return (((self.x+self.vx) - (other.x +other.vx))**2 + ((self.y +self.vy) - (other.y+other.vy))**2)**0.5
        
    
    def real_speed(self):
        return ((self.vx)**2 + (self.vy)**2)**0.5
    
    def collide_ball(self, other):
        # When I was initally test this program, the float problem rise again so sometimes the balls
        # have a negative distance (like -1.2e-14) which changes the physics drastically. Here the code 
        # solves this problem completely and ensures
        # the balls never overlap by pushing it back
        while self.distance(other) <= self.r + other.r:
            dx = other.x - self.x
            dy = other.y - self.y
            impx = dx / (self.r + other.r)
            impy = dy / (self.r + other.r)
            self.x = self.x - impx
            self.y = self.y - impy
            other.x = other.x + impx
            other.y = other.y + impy
        
        if self.update_distance(other) >= self.r + other.r:
            return False
        # Because the game introduces friction, if the balls happen to stick together and they do not move, 
        # they cannot move by the logic of the main game display function. The elif here solves this problem simply
        # and solve the problem that two balls stick together and never seperate  
        elif self.vx == 0 and self.vy ==0 and other.vx ==0 and other.vy ==0:
            return False
        else:
            return True
        
    def bounce(self, other):
        self.bounce_sound.rewind()
        self.bounce_sound.play()
        # The physics behind finding the collision of two moving objects is complicated 
        # so I just found the formula and substitute everything
        dx = other.x - self.x
        dy = other.y - self.y
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        
        # Solving the quadratic equation
        a = dvx**2 + dvy ** 2
        b = 2* (dx*dvx + dy* dvy)
        c = dx ** 2 + dy **2 - (self.r + other.r)**2
        delta = b**2 - 4*a*c
        
        # There is a collision happening in exactly one frame so the existence of a collision is ensured
        # Therefore, delta must be greater than 0
        t1 = (-b + delta**0.5)/(2*a)
        t2 = (-b - delta**0.5)/(2*a)
        
        # The collision happens in the future so a positive solution exists
        t = min(t1, t2)
        # The following code solves annoying cases of the float that
        # it produced a very-close-to-0 negative number instead of 0
        if t<0:
            t = 0
        
        self.x = self.x + self.vx*t
        self.y = self.y + self.vy*t
        other.x = other.x + other.vx*t
        other.y = other.y + other.vy*t
    
    
        # This section is basicly the physics behind a perfect elastic collision
        dx = other.x - self.x
        dy = other.y - self.y
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        
        #line of impact decomposed
        impx = dx / (self.r + other.r)
        impy = dy / (self.r + other.r)
        
        #projection of velocity using dot product
        impvx = self.vx * impx + self.vy * impy
        impvy = other.vx * impx + other.vy * impy
        
        #the actual formula
        tempv_1 = (impvx*(self.m-other.m) + 2*other.m*impvy)/(self.m+other.m)
        tempv_2 = (impvy*(other.m-self.m) + 2*self.m*impvx)/(self.m+other.m)
        
        #decompose the component again
        self.vx = self.vx + (tempv_1-impvx) * impx
        self.vy = self.vy + (tempv_1-impvx) * impy
        other.vx = other.vx + (tempv_2-impvy) * impx
        other.vy = other.vy + (tempv_2-impvy) * impy
        
            
            
        
    
 

    
    def update(self):
        
        # the key handles of the snowballs
        if self.num == 1:
            if self.key_handler[0][LEFT] == True and self.key_handler[0][RIGHT] == True:
                self.ax = 0
            elif self.key_handler[0][LEFT] == True:
                self.ax = -self.force
            elif self.key_handler[0][RIGHT] == True:
                self.ax = self.force
            else:
                self.ax = 0
            
            if self.key_handler[0][UP] == True and self.key_handler[0][DOWN] == True:
                self.ay = 0
            elif self.key_handler[0][UP] == True:
                self.ay = -self.force
            elif self.key_handler[0][DOWN] == True:
                self.ay = self.force
            else:
                self.ay = 0
        
        if self.num == 2:
            if self.key_handler[1]['a'] == True and self.key_handler[1]['d'] == True:
                self.ax = 0
            elif self.key_handler[1]['a'] == True:
                self.ax = - self.force
            elif self.key_handler[1]['d'] == True:
                self.ax = self.force
            else:
                self.ax = 0
            
            if self.key_handler[1]['w'] == True and self.key_handler[1]['s'] == True:
                self.ay = 0
            elif self.key_handler[1]['w'] == True:
                self.ay = -self.force
            elif self.key_handler[1]['s'] == True:
                self.ay = self.force
            else:
                self.ay = 0
                
        
        # The following code introduces friction into the game by putting a constant decerleration on the ball
        # if the ball is moving. The friction will make the speed 0 when the speed is too low.
        self.true_v = sqrt(self.vx**2 + self.vy**2)
        self.move_angle = math.atan2(self.vy, self.vx)
        self.fx = self.fric_force * math.cos(self.move_angle)
        self.fy = self.fric_force * math.sin(self.move_angle)
        
        if self.vx != 0 and abs(self.vx) >= abs(self.fx):
            self.vx += self.fx
        elif self.vx != 0 and abs(self.vx) < abs(self.fx):
            self.vx = 0
        if self.vy != 0 and abs(self.vy) >= abs(self.fy):
            self.vy += self.fy
        elif self.vy != 0 and abs(self.vy) < abs(self.fy):
            self.vy = 0
        
        # puts a maximum speed on the ball 
        if self.real_speed() <= MAX_SPEED:
            self.vy += self.ay
            self.vx += self.ax
        
        self.x += self.vx
        self.y += self.vy
    

class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.snowball_1 = Snowball(DEFAULT_X1, DEFAULT_Y1, DEFAULT_RAD, 'player', 1)
        self.snowball_2 = Snowball(DEFAULT_X2, DEFAULT_Y2, DEFAULT_RAD, 'player', 2)
        self.arena = Arena(RESOLUTION_W/2, RESOLUTION_H/2, ARENA_RAD, 'arena')
        
        # state describes the current scene of the game. -1 is the starting stage, 0 is the gaming stage, 1 is the roundover stage, 2 is the game over stage.
        self.state = -1
        self.item = None
        self.img_init = loadImage(PATH +'/images/Starting.jpg')
        self.img_on = loadImage(PATH +'/images/Bg.jpg')
        self.img_end = loadImage(PATH +'/images/gameover.png')
        self.img_mid = loadImage(PATH +'/images/roundover.png')
        self.img_p1 = loadImage(PATH +'/images/player1.png')
        self.img_p2 = loadImage(PATH +'/images/player2.png')
        self.img_wins = loadImage(PATH +'/images/wins.png')
        # I include the bgm for the game, but the platform is very slow so I hashed it.
        # self.bg_sound = player.loadFile(PATH + "/sounds/holdsworth.mp3")
        # self.bg_sound.loop()
        self.end_sound = player.loadFile(PATH + "/sounds/die.wav")
        self.gameover_sound = player.loadFile(PATH + "/sounds/gameover.mp3")
    
    # generate one random item (coin or powerup) in the arena by using the polar coordinate r* theta
    def generate(self):
        temp_theta = random.randint(0,359)
        temp_r = random.randint(0, self.arena.r - ITEM_RAD*2 )
        temp_x = self.arena.x + math.cos(math.radians(temp_theta))*temp_r
        temp_y = self.arena.y + math.sin(math.radians(temp_theta))*temp_r
        temp_type = ITEM_TYPE[random.randint(0,3)]
        self.item = Item(temp_x, temp_y, ITEM_RAD, 'item', temp_type)
        # the following code (already hashed) is an idea to prevent items spawning on a snowball and immediately collects it.
        # but I realize that as we contain a powerup that increases the size, the ball may eventually take the whole arena and there will be no places for the item to generate
        # and I think it is fun if item can spawn on the player so it adds uncertainly to the game so I end up not using the idea
        # while self.item.distrance(self.snowball_1) < self.item.r + dself.snowball_1.r or self.item.distrance(self.snowball_1) < self.item.r + self.snowball_1.r
        # print(self.item.type)
   
    # reset the game arena, and if game has already ended, we clear the score.
    def reset(self):
        self.snowball_1.reset()
        self.snowball_2.reset()
        self.item = None
        if self.state == 2:
            self.snowball_1.score = 0
            self.snowball_2.score = 0
    
    # a scoreboard to display the scores and coins at the game stage
    def scoreboard(self):
        image(self.img_p1, RESOLUTION_W-310, 10, 300,100)
        image(self.img_p2, 10, 10, 300, 100)
        noStroke()
        fill(125, 100)
        rect(30,120,220,130)
        rect(1030,120,220,130)
        textSize(50)
        fill(0,0,125)
        text('Score:'+str(self.snowball_1.score), 1050, 180)
        text('Score:'+str(self.snowball_2.score), 50, 180)
        text('Coin:'+str(self.snowball_1.coin), 1060, 230)
        text('Coin:'+str(self.snowball_2.coin), 60, 230)
            
        
    
    def display(self):  
        
        # graphic design at the starting scene
        if self.state == -1:
            image(self.img_init, 0, 0)
            textSize(70)
            fill(255,127,80)
            text('CLICK MOUSE TO START', 250, 600)
        else:
            image(self.img_on, 0, 0)
            
            # detects if the round is over (to state 1) or the game is over (to state 2)
            if (self.arena.round_over(self.snowball_1) != None or self.arena.round_over(self.snowball_2)) != None:
                if self.state == 0:
                    if self.arena.round_over(self.snowball_1) == 'Lose' or self.arena.round_over(self.snowball_2) == 'Win' :
                        self.snowball_2.score += 1
                    elif self.arena.round_over(self.snowball_2) == 'Lose' or self.arena.round_over(self.snowball_1) == 'Win' :
                        self.snowball_1.score += 1
                    if self.snowball_1.score >= 2 or self.snowball_2.score >=2:
                        self.gameover_sound.rewind()
                        self.gameover_sound.play()
                        self.state = 2
                    else:
                        self.end_sound.rewind()
                        self.end_sound.play()
                        self.state = 1
                        
                # graphic design at the roundover scene
                elif self.state == 1:
                    self.scoreboard()
                    image(self.img_mid, RESOLUTION_W/2-300, RESOLUTION_H/2-500, 600, 600)
                    
                # graphic design at the gameover scene
                elif self.state == 2:
                    if self.snowball_1.score >= 2:
                        image(self.img_p1, RESOLUTION_W/2-400, RESOLUTION_H/2+170)
                    if self.snowball_2.score >= 2:
                        image(self.img_p2, RESOLUTION_W/2-400, RESOLUTION_H/2+170)
                    image(self.img_end, RESOLUTION_W/2-300, RESOLUTION_H/2-500, 600, 600)
                    image(self.img_wins, RESOLUTION_W/2, RESOLUTION_H/2, 400, 400)
                    
            else:  
                
                # the main display of the gaming stage
                
                # collision and bounce back of snowballs if there is one
                if self.snowball_1.collide_ball(self.snowball_2) == False:
                    self.snowball_1.update()
                    self.snowball_2.update()
                else:
                    self.snowball_1.bounce(self.snowball_2)
                    
                # generate a random item every 3 seconds
                if frameCount % 180 == 0:
                    self.generate()
                if self.item != None:
                    self.item.update()
                    if self.item.collision(self.snowball_1) or self.item.collision(self.snowball_2):
                        if self.item.overlap(self.snowball_1) <= self.item.overlap(self.snowball_2):
                            self.item.upgrade(self.snowball_1)
                            self.item = None
                        else:
                            self.item.upgrade(self.snowball_2)
                            self.item = None

                            
                            

                self.scoreboard()
                self.arena.display()
                self.snowball_1.display()
                self.snowball_2.display()
                if self.item != None:    
                    self.item.display()
            

def setup():
    size(RESOLUTION_W, RESOLUTION_H)
    background(255,255,255)
    
def draw():
    background(255,255,255)
    game.display()

def keyPressed():
    if keyCode == LEFT:
        game.snowball_1.key_handler[0][LEFT] = True
    if keyCode == RIGHT:
        game.snowball_1.key_handler[0][RIGHT] = True
    if keyCode == UP:
        game.snowball_1.key_handler[0][UP] = True
    if keyCode == DOWN:
        game.snowball_1.key_handler[0][DOWN] = True
    if key == 'a':
        game.snowball_2.key_handler[1]['a'] = True
    if key == 'd':
        game.snowball_2.key_handler[1]['d'] = True
    if key == 'w':
        game.snowball_2.key_handler[1]['w'] = True
    if key == 's':
        game.snowball_2.key_handler[1]['s'] = True

# click the mouse continues the game and reset the scene.
def mouseClicked():
    if game.state == -1:
        game.state = 0
    if game.arena.round_over(game.snowball_1) or game.arena.round_over(game.snowball_2):
        game.reset()
        if game.state == 2:
            game.state = -1
        else:
            game.state = 0
    

        
def keyReleased():
    if keyCode == LEFT:
        game.snowball_1.key_handler[0][LEFT] = False
    if keyCode == RIGHT:
        game.snowball_1.key_handler[0][RIGHT] = False  
    if keyCode == UP:
        game.snowball_1.key_handler[0][UP] = False
    if keyCode == DOWN:
        game.snowball_1.key_handler[0][DOWN] = False
    if key == 'a':
        game.snowball_2.key_handler[1]['a'] = False
    if key == 'd':
        game.snowball_2.key_handler[1]['d'] = False
    if key == 'w':
        game.snowball_2.key_handler[1]['w'] = False
    if key == 's':
        game.snowball_2.key_handler[1]['s'] = False
    
game = Game(RESOLUTION_W, RESOLUTION_H)
