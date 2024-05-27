#Создай собственный Шутер!
from time import *
from pygame import *
from random import randint
font.init()
font1 = font.SysFont('Arial', 100)
font2 = font.SysFont("Arial", 36)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOOSE!', True, (180, 0,0))
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#нам нужны такие картинки:
img_back = "meshh.jpg" #фон игры
img_bullet = "bullet.png" #пуля
img_hero = "krosh.gif" #герой
img_enemy = "025.png" #враг
img_meteor = 'asteroid.png'
score = 0 #сбито кораблей
goal = 20 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 3 #проиграли, если пропустили столько
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)


#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдёт до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
#класс спрайта-пули  
class Bullet(GameSprite):
   # движение врага
   def update(self):
       self.rect.y += self.speed
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()
#создаём окошко
win_width = 700
win_height = 500
display.set_caption("космосмеш")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#создаём спрайты
ship = Player(img_hero, 5, win_height - 110, 100, 120, 10)
#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 10):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
bullets = sprite.Group()
meteors = sprite.Group()
for i in range (1,4):
    meteor = Enemy(img_meteor, randint(80, win_width - 80), -40,80,50, randint(1,3))
    meteors.add(meteor)
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
   #событие нажатия на кнопку Закрыть
while run:
    for e in event.get():
            if e.type == QUIT:
                run = False
        #событие нажатия на пробел - спрайт стреляет
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    fire_sound.play()
                    ship.fire()
            
            
 #сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
       #обновляем фон
        window.blit(background,(0,0))


       #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        meteors.update()


       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        meteors.draw(window)
       #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
           #этот цикл повторится столько раз, сколько монстров подбито
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
        if sprite.spritecollide(ship, meteors, False):
            finish = True
            window.blit(lose, (200,200))
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
        if score >= goal:
            finish = True
            window.blit(win,(200,200))


       #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        display.update()
    time.delay(50)