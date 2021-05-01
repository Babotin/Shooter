from pygame import *
from random import *

mixer.init()
font.init()

scote_font = font.SysFont("Arial", 23)
mixer.music.load("space.ogg")
mixer.music.play(loops = -1)
laser = mixer.Sound("Laser.wav")
AlienExplosion = mixer.Sound("AlienExplosion.wav")

W = 1000
H = 700
window = display.set_mode((W, H))
background = transform.scale(image.load("galaxy.jpg"), (W, H))
display.set_caption("Шутer")

class Game_sprite(sprite.Sprite):
    def __init__(self, file, w, h, x, y, speed):
        #self.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = image.load(file)
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def draw(self):
        window.blit(self.image, self.rect)

class Player(Game_sprite):
    score = 0
    def control(self):
        keys = key.get_pressed()
        if keys[K_RIGHT]:
            if self.rect.x < 960:
                self.rect.x += self.speed
        if keys[K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        self.draw()
 
bullet_list = []
 
class Bullet(Game_sprite):
    def control(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
            for ufo in ufo_list:
                if sprite.collide_rect(self, ufo):
                    AlienExplosion.play()
                    ufo.rect.y = 0
                    ufo.rect.x = randint(100, 900)
                    bullet_list.remove(self)
                    player.score += 1
                    
                    break
            self.draw()
        else: 
            bullet_list.remove(self)
 
ufo_list = []
 
class Ufo(Game_sprite):
    def control(self):
        if self.rect.y < H:
            self.rect.y += self.speed
            self.draw()
        else: 
            self.rect.y = 0
            self.rect.x = randint(100, 900)
            player.score -= 3
 
for i in range(10):
    ufo = Ufo("ufo.png", 45, 60, randint(100, 900), i*-60, 7)
    ufo_list.append(ufo)
    print(ufo.speed)

player = Player("rocket.png", 40, 80, W//2, H-100, 10)
 
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if player.score < 10 and player.score > -10:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    bullet = Bullet("bullet.png", 15, 20, player.rect.centerx-6, player.rect.y, 17)
                    bullet_list.append(bullet)
                    laser.play()
    window.blit(background, (0, 0))
    if player.score >= 10 or player.score <= -10:
        if player.score >= 10:
            text = scote_font.render("WIN", True, (0, 200, 0))
            text_rect = text.get_rect()
            text_rect.center = (W/2, H/2)
        else:
            text = scote_font.render("GAME OVER", True, (200, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (W/2, H/2)
        window.blit(text, text_rect)
    else:
        player.control()
        for bullet in bullet_list:
            bullet.control()
        for ufo in ufo_list:
            ufo.control()
        if player.score >= 0:
            color = ((0, 200, 0))
        else:
            color = ((200, 0, 0))
        text = scote_font.render(str(player.score), True, color)
        window.blit(text, (20, 20))
    display.update()
    time.delay(10)