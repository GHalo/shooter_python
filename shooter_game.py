#Создай собственный Шутер!
from pygame import *
from random import randint
import time as t
init()
mixer.init()
font.init()
class GameSprite(sprite.Sprite):
    def __init__(self, name ,x , y, speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(name), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def update (self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.x < win_width -200:
            self.rect.y -= self.speed
        if keys[K_s]and self.rect.y < win_height -200:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d]and self.rect.y < 0:
            self.rect.x += self.speed
    
    
    def fire(self):
        bullet1 = Bullet('bullet.png', self.rect.centrex-4, self.rect.y,10,10,30 )
        bullets.add(bullet1)
        global last_fire, fire
        last_fire = t.time(a)
        fire.play()



        
class Enemy(GameSprite):
    global win_width,win_height
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height-150:
            global lost
            lost += 1
            self.kill()        
            monsters.add(Enemy('ufo.png',randint(150,win_width-150),randint(-250,-30),randint(-3,5),45,45))


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()

    
score = 0
lost = 0
window = display.set_mode((0, 0),FULLSCREEN)
win_width , win_height = display.get_surface().get_size()
game = True
finish = False
FPS = 60
timer = time.Clock()

background = transform.scale(image.load('galaxy.jpg'), (1920, 1080))

font0 = font.SysFont('Arial', 12)
font1 = font.SysFont('Arial', 52)

mixer.music.load('space.ogg')
mixer.music.play()

win_image = font0.render('YOU WIN', True ,(0,255,255))
lose_image = font0.render("YOU_LOSE", True, (255,0,0))


player = Player('rocket.png',win_width//2 ,win_height -200,10,65,65)

monsters = sprite.Group()
bullets = sprite.Group()

last_fire = 0
for i in range(5):
    monsters.add( Enemy('ufo.png',  randint(150, win_width -150) ,randint(-250,-30),randint(3,5),45,45))

display.set_caption('gamagey')
while game:
    display.update()
    timer.tick(FPS)
    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            game = False

        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            if t.time() - last_fire > 1 and not(finish):

                play.fire()
    if not (finish):
        player.update()
        monsters.update()
        bullets.update()

        monsters_list = sprite.groupcollide(monsters,bullets,True,True)
        for monst in monsters_list:
            score +=1
            monsters.add (Enemy('ufo.png',  randint(50,win_width-50)  ,randint(-250,-30),randint(3,5),45, 45))

            
        image_score = font1.render('Cчет' +str(score), True, (255,255,255) )
        image_lost = font1.render('пропущенно'+str(lost), True, (255,255,255))


        window.blit(background, ((0,0)))
        window.blit(image_score, ((250,150)))
        window.blit(image_lost, ((150,250)))
        player.reset()

        monsters.draw(window)
        bullets.draw(window)



        

            



   