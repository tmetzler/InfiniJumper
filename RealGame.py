import pyxel
import json
from random import randint
#Fichier pour l'highscore
highscore = '/Users/titouan/Desktop/MyCode/HighScore.json'

fps = 60

pyxel.init(140, 250, title="InfiniJumper", fps=fps)
#Fichier normal de pyxres
pyxel.load('Moves.pyxres')


#Variables de Start
sprites = []
ground = pyxel.height
gravity = 9
move_down = 250
Invalid_Block = True
new_width = None
difficulty = 1.5

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
    for block in sprites[2:]:
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

    def update(self):

        #sideways movement
        if pyxel.btn(pyxel.KEY_LEFT) and not in_rectangle(self.x - 1, self.y) and not in_rectangle(self.x - 1, self.y + self.h) and self.x + 7 <= pyxel.width:
            self.x = self.x - 1
            
        if pyxel.btn(pyxel.KEY_RIGHT) and not in_rectangle(self.x + self.w, self.y) and not in_rectangle(self.x + self.w, self.y + self.h)  and self.x >= 0:
            self.x = self.x + 1
        #Gets Sprite out of rectangle
        if in_rectangle(self.x, self.y) or self.x + 8 <= pyxel.width:
            self.x = self.x + 1
        if in_rectangle(self.x + self.w + 2, self.y ) or self.x -1 >= 0:
            self.x = self.x - 1

        #Makes Sprite fall & ups speed & quits if touch ground
        self.y = self.y + self.speed
        if self.y + self.h < ground:
            self.speed = self.speed + gravity/fps
        if self.y + self.h > ground:
            self.y = ground - 8
        if self.y + self.h >= ground:
            pyxel.quit()
            print("YOU LOSE")
        if in_rectangle(self.x, self.y + self.h) or in_rectangle(self.x + self.w, self.y + self.h):
            self.speed = 0
        #Jumping
        if pyxel.btnp(pyxel.KEY_SPACE) and  in_rectangle(self.x, self.y + self.h + 6) or pyxel.btnp(pyxel.KEY_SPACE) and in_rectangle(self.x + self.w, self.y + self.h + 6):
            self.speed = -5
        #Stop Clipping
            # Upwards
        if in_rectangle(self.x, self.y + self.speed) or in_rectangle(self.x + 8, self.y + self.speed):
            self.speed = 1
            #Downwards
        if in_rectangle(self.x, self.y + 8) and in_rectangle(self.x + 8, self.y + 8):
            self.y = self.y - 3

    
    def draw(self):

        pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h)

class Score:
    """Le Score"""
    def __init__(self) -> None:
        self.current_score = 0

    def update(self):
        self.current_score = self.current_score + 1
        with open (highscore) as h:
            HighScore = json.load(h)
            if HighScore < self.current_score:
                with open (highscore, 'w') as f:
                    json.dump(self.current_score, f)

    
    def draw(self):
        with open (highscore) as h:
            Hscore = json.load (h)
            pyxel.text(10, 10, f"Score: {self.current_score} \n High Score: {Hscore}", 7)

    
def update():
    global Invalid_Block
    global move_down
    for sprite in sprites:
        sprite.update()
    if move_down % (150 / difficulty) == 0:
        #Makes Sure New Block Isn't in Sprite & Sprite can jump on it
        while Invalid_Block:
            new_width = randint(10, 60)
            new_block = Block(width = new_width, height = randint(10,90), x = randint(1,140) - new_width/2, y = 50, color = randint(1,15), speed = pyxel.rndf(1, 2.5))
            if new_block.y > sprites[0].y + 8 or new_block.x > sprites[0].x + 8 or new_block.y + new_block.height < sprites[0].y or new_block.x + new_block.width < sprites[0].x:
                if new_block.x - 70 < sprites[0].x + 8 and new_block.x + new_block.width + 70 > sprites[0].x:    
                    if new_block.x > sprites[0].x + sprites[0].w or new_block.x + new_block.width < sprites[0].x:
                        Invalid_Block = False
                        sprites.append(new_block)
        Invalid_Block = True
    move_down = move_down + 1

def draw():
    pyxel.cls(0)

    for sprite in sprites:
        sprite.draw()
#Sprite
sprites.append(Sprite())
#Score
sprites.append(Score())
#Spawning Platform
sprites.append(Block(56, 16, pyxel.width/2 - 56/2, pyxel.height/2, 7, speed = 1))
pyxel.playm(1, loop = True)
pyxel.run(update, draw)
