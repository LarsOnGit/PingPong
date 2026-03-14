from pygame import *
from random import randint


# Das ist ein Konflikt

font.init()
font1 = font.SysFont("Arial", 80)
font2  = font.SysFont("Arial", 30)
p1_point_int = 0
p2_point_int = 0
p1_points = font2.render("Points:" + str(p1_point_int), True, (0, 0, 0))
p2_points = font2.render("Points:" + str(p2_point_int), True, (0, 0, 0))



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
        super().__init__("paddle.png", x, y, 50, 150, 5)
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        keys = key.get_pressed()
        if keys[self.up_key] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[self.down_key] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, image_path, player_x, player_y, size_x, size_y, speed):
        super().__init__(image_path, player_x, player_y, size_x, size_y, speed)
        self.speed_x = speed
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def check_wall_collision(self):
        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.speed_y = -self.speed_y

    def check_goal(self, pleft_points, pright_points):
        if self.rect.x <= 0 or self.rect.x >= win_width - self.rect.width:
            if self.rect.x <= 0:
                pright_points += 1
            if self.rect.x >= win_width - self.rect.width:
                pleft_points += 1
            self.rect.x = win_width // 2
            self.rect.y = win_height // 2
            self.speed_x = -self.speed_x
        
    def check_paddle_collision(self, paddle_left, paddle_right):
        if sprite.collide_rect(self, paddle_left):
            if self.speed_x < 0: 
                self.speed_x = -self.speed_x
                hit_pos = (self.rect.centery - paddle_left.rect.centery) / (paddle_left.rect.height / 2)
                self.speed_y = hit_pos * 8
        
        if sprite.collide_rect(self, paddle_right):
            if self.speed_x > 0:  
                self.speed_x = -self.speed_x
                hit_pos = (self.rect.centery - paddle_right.rect.centery) / (paddle_right.rect.height / 2)
                self.speed_y = hit_pos * 8
        

win_width = 700
win_height = 500

pleft_points = 0
pright_points = 0
 
display.set_caption("PingPong")
window = display.set_mode((win_width, win_height))

bg_im = image.load("background.jpg")
background = transform.scale(bg_im, (win_width, win_height))

player_left = Player(50, win_height//2 - 75, K_w, K_s)
player_right = Player(win_width - 100, win_height//2 - 75, K_UP, K_DOWN)
ball = Ball("ping_pong_ball.png", win_width//2, win_height//2, 25, 25, 5)  

p1_points = font1.render(str(pleft_points), True, (0, 0, 0))
p2_points = font1.render(str(pright_points), True, (0, 0, 0))




run = True
FPS = 60
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
        window.blit(p1_points, (100, 50))
        window.blit(p2_points, (win_width - 100, 50))
        ball.update()
        ball.check_wall_collision()
        ball.check_paddle_collision(player_left, player_right)
        ball.check_goal(pleft_points, pright_points)
        ball.draw()

    display.update()
    clock.tick(FPS)
