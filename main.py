

import pygame
from random import randint
 
pygame.init()
HEIGHT = 900
WIDTH = 1600
display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (WIDTH, HEIGHT))
 
 
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, playerimg, x, y, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(playerimg), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def reset(self):
        display.blit(self.image, (self.rect.x, self.rect.y))
 
 
class Player(GameSprite):
    def move(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            if self.rect.x > 10:
                self.rect.x -= self.speed
        if press[pygame.K_RIGHT]:
            if self.rect.x < WIDTH - 110:
                self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets_group.add(bullet)
 
 
class Enemy(GameSprite):
    def update(self):
        global failed
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            failed += 1
            self.rect.y = 0
            self.rect.x = randint(0, int(WIDTH - 40))
 
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
 
        if self.rect.y < 0:
            self.kill()
 
 
pl = Player("rocket.png", 750, 800, 100, 100, 9)
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group.add(pl)
bullets_group = pygame.sprite.Group()
ENEMIES = 7
 
for i in range(ENEMIES):
    enemy = Enemy("ufo.png", randint(0, int(WIDTH - 50)), 0, 100, 100, randint(1, 5))
    enemy_group.add(enemy)
 

pygame.font.init()
font1 = pygame.font.SysFont('arial.ttf', 72)
font2 = pygame.font.SysFont('arial.ttf', 20)
lose_text = font1.render('YOU LOSE...\nRESTARTING...', True, (246, 14, 14))
win_text = font1.render('YOU WIN...\nRESTARTING...', True, (136, 204, 0))
clock = pygame.time.Clock()
run = True
finish = False
 
score = 0
failed = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pl.fire()
 
    if not finish:
        print(failed)
        display.blit(bg, (0, 0))
 
        score_text = font2.render("Score: " + str(score), True, (255, 249, 166))
        display.blit(score_text, (20, 20))
        failed_text = font2.render("Failed: " + str(failed), True, (255, 249, 166))
        display.blit(failed_text, (20, 45))
 
        pl.reset()
        pl.move()
        enemy_group.draw(display)
        enemy_group.update()
        bullets_group.update()
        bullets_group.draw(display)
        collides = pygame.sprite.groupcollide(player_group, enemy_group, False, False)
        if collides:
            display.blit(lose_text, (350, 400))
            finish = True
 
        bullet_collides = pygame.sprite.groupcollide(bullets_group, enemy_group, True, True)
        for c in bullet_collides:
            score += 1
            enemy = Enemy("ufo.png", randint(0, int(WIDTH - 50)), 0, 100, 100, randint(1, 5))
            enemy_group.add(enemy)
 
        pygame.display.update()
        clock.tick(120)
 
    else:
        failed = 0
        score = 0
        pygame.time.delay(2000)
        for e in enemy_group:
            e.kill()
 
        for b in bullets_group:
            b.kill()
 
        pl.rect.x = 700
        for i in range(ENEMIES):
            enemy = Enemy("ufo.png", randint(0, int(WIDTH - 50)), 0, 100, 100, randint(1, 5))
            enemy_group.add(enemy)
 
        finish = False
 