from pygame import*
from random import randint
import time as   t   
init()

W = 500
H = 700

window = display.set_mode((W, H))
display.set_caption("shooter")
display.set_icon(image.load("petro.png"))

back = transform.scale(image.load('galaxy.jpg'), (W, H)) 
# clock = time.Clock()
# зміннні для підрахунку вбитих пропузених та життя 
lost = 0
killed = 0
life = 5
"""         ЗВУКИ       """
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
fire = mixer.Sound('fire.ogg')
mixer.music.play()

""""" Шрифти """
font.init()
font1 = font.SysFont("Arial   ",20,bold = True)
font2 = font.SysFont("Arial   ",60,bold = True )

""""        КЛАСИ       """
class GameSprite(sprite.Sprite):#основний клас
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()#відмальовуємо картинки 
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):#метод управління
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0,W-80)
            lost +=1

class Asteroid(Enemy):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0,W-80)
            
                            

class Bullet(GameSprite):
    def update(self):
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.kill()



#створення  гравця
player = Player("petro.png",W/2,H-100,80, 100, 10)#створення об'єктів

monsters = sprite.Group()#створення групри спрайтів 
bullets =  sprite.Group()
asteroids = sprite.Group()

for i in range(5): #створення ворогів 
    monstr = Enemy("bat.png",randint(0,W-80),randint(-50,0),80,50, randint(1,3))
    monsters.add(monstr)


for i in range(3):
    asteroid = Asteroid("asteroid.png",randint(0,W-80),randint(-50,0),80,50, randint(1,3))
    asteroids.add(asteroid)


finish = False
game = True
num_fire = 0
rel_time = False  
color_life = (0,255,0)                   
while game:

    time.delay(10)#затримка
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 7  and rel_time is False:
                    num_fire += 1
                    player.fire()
                    fire.play()
                if num_fire >7 and rel_time is False:
                    rel_time = True
                    last_time = t.time()
                     
    if not finish:

        window.blit(back, (0, 0))#малюємо фон 
        player.reset()#малюємо гравця
        player.update()#рух гравця

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if rel_time:
            new_time = t.time()
            if new_time - last_time <3:
                reload_txt = font1.render("Перезарядка...", True,(255,0,0))
                window.blit(reload_txt,(W/2-100, H/2))
            else:
                rel_time = False
                num_fire = 0


        lost_txt= font1.render(f"Пропущено: {lost}",True,(255,255,255))
        window.blit(lost_txt,(10,10))

        kill_txt= font1.render(f"Збито: {killed}",True,(255,255,255))
        window.blit(kill_txt,(10,40))


        life_txt= font2.render(f"{life}",True,color_life)
        window.blit(life_txt,(450,5))

        if life == 3 or life == 2:
            color_life = 212,174,38
        if life == 1:
            color_life = (255,0,0)   
        if sprite.spritecollide(player,monsters,True):
            life -=1
            monstr = Enemy("bat.png",randint(0,W-80),-50,80,50, randint(1,3))
            monsters.add(monstr)

        colides = sprite.groupcollide(monsters,bullets, True, True)
        for col in colides:
            monstr = Enemy("bat.png",randint(0,W-80),-50,80,50, randint(1,3))
            monsters.add(monstr)
            killed += 1 
        if killed >= 20:
            win = font2.render('U WIN',True, (0,255,0))
            window.blit(win,(W/2-100,H/2))
            finish = True
        if life <= 0:
            lose = font2.render('U LOSE',True, (255,0,0))
            window.blit(lose,(W/2-100,H/2))
            finish = True

        if sprite.spritecollide(player,asteroids,True):
            life -=1
            
           
           

    else:
        keys_pressed =  key.get_pressed()
        if keys_pressed[K_r]:
            life = 5
            killed = 0 
            lost = 0
            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for i in range(5): #створення ворогів 
                monstr = Enemy("bat.png",randint(0,W-80),randint(-50,0),80,50, randint(1,3))
                monsters.add(monstr)
            finish = False
    display.update()#оновлення екрана!
