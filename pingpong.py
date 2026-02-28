from pygame import *
from random import randint


# Das ist ein Konflikt

font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))


font2  = font.SysFont("Arial", 36)

mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, image_path, player_x, player_y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 5:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.x + 40 , win_height - 100, 15, 20, 15)
        bullets.add(bullet)

class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()




win_width = 700
win_height = 500

display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

bg_im = image.load("galaxy.jpg")
background = transform.scale(bg_im, (win_width, win_height))

player_left = Player("paddle.png", 50, win_height - 100 , 80, 100, 10)
player_right = Player("paddle.png", win_width - 130, win_height - 100 , 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(0, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

score = 0
goal = 10
lost  = 0
max_lost = 3
run = True
FPS = 20
clock = time.Clock()
finish = False

while run: 
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(background, (0,0))

    display.update()
    clock.tick(FPS)