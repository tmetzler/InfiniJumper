import pyxel
import json
import os
from random import randint
#Fichier pour l'highscore
highscore = './HighScore.json'

fps = 60

pyxel.init(140, 250, title="InfiniJumper", fps=fps)
#Fichier normal de pyxres
pyxel.load('Moves.pyxres')


#Variables de Start
sprites = []
ground = pyxel.height
difficulty = 1.5
move_down = 250
Invalid_Block = True
new_width = None
gravity = 8

class Block:
    """Rectangle où le sprite saute"""
    def __init__(self, width, height, x, y, color, speed) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed

    def update(self):
        if move_down % 5 == 0:
            self.y = self.y + 1 * self.speed * difficulty
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

def in_rectangle(x, y):
    #Detects if a pixel is inside a block using x and y, in that order
    for block in sprites[0:-2]:
        if y < block.y + block.height and y > block.y and x < block.x + block.width and x > block.x:
            return True


class Sprite:
    """Le Sprite"""
    def __init__ (self):
        """Defines attributes for Sprite"""
        self.w = 8
        self.h = 8
        self.y = pyxel.height/2 - self.h/2 - 50
        self.x = pyxel.width/2 - self.w/2
        self.speed = 0
        self.imgposx = 0
        self.imgposy = 0

    def is_lost(self):
        return self.y + self.h >= ground
    
    def update(self):

        #sideways movement
        if pyxel.btn(pyxel.KEY_LEFT) and not in_rectangle(self.x - 1, self.y) and not in_rectangle(self.x - 1, self.y + self.h) and self.x + 7 <= pyxel.width:
            self.x = self.x - 1
            
        if pyxel.btn(pyxel.KEY_RIGHT) and not in_rectangle(self.x + self.w + 1 , self.y) and not in_rectangle(self.x + self.w, self.y + self.h)  and self.x >= 0:
            self.x = self.x + 1
        #Gets Sprite out of rectangle
        if in_rectangle(self.x, self.y) or self.x + 8 <= pyxel.width:
            self.x = self.x + 1
        if in_rectangle(self.x + self.w + 2, self.y ) or self.x -1 >= 0:
            self.x = self.x - 1

        #Makes sprite follow a fast block
        if in_rectangle(self.x, self.y + self.h + 3) or in_rectangle(self.x + 7, self.y + self.h + 3):
            self.y = self.y + 3
    
        #Makes Sprite fall & ups speed & quits if touch ground
        if self.y + self.h < ground:
            self.speed = self.speed + gravity/fps
        if in_rectangle(self.x, self.y + self.h + self.speed) or in_rectangle(self.x + self.w, self.y + self.h + self.speed):
            while in_rectangle(self.x, self.y + self.h ) or in_rectangle(self.x + 7, self.y + self.h ):
                self.y = self.y - 1
            self.speed = 0

        self.y = self.y + self.speed
        #Jumping
        if pyxel.btnp(pyxel.KEY_SPACE) and  in_rectangle(self.x, self.y + self.h + 6) or pyxel.btnp(pyxel.KEY_SPACE) and in_rectangle(self.x + self.w, self.y + self.h + 6):
            self.speed = -5
        #Stop Clipping
            # Upwards
        if in_rectangle(self.x, self.y + self.speed) or in_rectangle(self.x + 8, self.y + self.speed):
            self.speed = 1
            #Downwards

    
    def draw(self):

        pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h)

class Score:
    """Le Score"""
    def __init__(self) -> None:
        self.current_score = 0
        if os.path.exists(highscore):
            with open (highscore) as h:
                self.high_score = json.load (h)
        else:
            self.high_score = 0
            
    def update(self):
        self.current_score = self.current_score + 1
        

    
    def save_high_score(self):
    
        if self.high_score < self.current_score:
            with open (highscore, 'w') as f:
                json.dump(self.current_score, f)

    def draw(self):
        pyxel.text(10, 10, f"Score: {self.current_score} \n High Score: {self.high_score}", 7)

    
def update():
    global Invalid_Block
    global move_down
    for sprite in sprites:
        sprite.update()

    player = sprites[-1]
    score = sprites[-2]
    
    if player.is_lost():        
        score.save_high_score()
        print("You lose")
        pyxel.quit()

    if move_down % (150 / difficulty) == 0:
        #Makes Sure New Block Isn't in Sprite & Sprite can jump on it
        while Invalid_Block:
            new_width = randint(10, 60)
            new_block = Block(width = new_width, height = randint(10,90), x = randint(1,140) - new_width/2, y = 50, color = randint(1,15), speed = pyxel.rndf(1, 2.5))
            if new_block.y > player.y + 8 or new_block.x > player.x + 8 or new_block.y + new_block.height < player.y or new_block.x + new_block.width < player.x:
                if new_block.x - 70 < player.x + 8 and new_block.x + new_block.width + 70 > player.x:    
                    if new_block.x > player.x + player.w or new_block.x + new_block.width < player.x:
                        Invalid_Block = False
                        sprites.insert(0, new_block)
        Invalid_Block = True
    move_down = move_down + 1

def draw():
    pyxel.cls(0)

    for sprite in sprites:
        sprite.draw()



#Spawning Platform
sprites.append(Block(56, 16, pyxel.width/2 - 56/2, pyxel.height/2, 7, speed = 1))
#Score
sprites.append(Score())
#Sprite
sprites.append(Sprite())

pyxel.playm(1, loop = True)

pyxel.run(update, draw)