from pygame import *
from random import randint


# Das ist ein Konflikt

font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))

font2  = font.SysFont("Arial", 36)

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
    def __init__(self, x, y, up_key, down_key):
        super().__init__("paddle.png", x, y, 50, 150, 4)
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        keys = key.get_pressed()
        if keys[self.up_key] and self.rect.x > 5:
            self.rect.y -= self.speed
        if keys[self.down_key] and self.rect.x < win_width - 5:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, image_path, player_x, player_y, size_x, size_y, speed):
        super().__init__(image_path, player_x, player_y, size_x, size_y, speed)
        self.speed_x = speed
        self.speed_y = speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def check_wall_collision(self):
        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.speed_y = -self.speed_y

win_width = 700
win_height = 500

display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

bg_im = image.load("background.jpg")
background = transform.scale(bg_im, (win_width, win_height))

player_left = Player(50, win_height//2 - 75, K_UP, K_DOWN)
player_right = Player(win_width - 100, win_height//2 - 75, K_w, K_s)
ball = Ball("ping_pong_ball.png", win_width//2, win_height//2, 20, 20, 5)   

score = 0
goal = 10
lost  = 0
max_lost = 3
run = True
FPS = 30
clock = time.Clock()
finish = False

while run: 
    for e in event.get():
        if e.type == QUIT:
             run = False
        if not finish:
            window.blit(background, (0,0))
            player_left.update()
            player_right.update()
            player_left.draw()
            player_right.draw()

            ball.update()
            ball.check_wall_collision()
            ball.draw()

    display.update()
    clock.tick(FPS)
