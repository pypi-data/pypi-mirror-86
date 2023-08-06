# choco_rocket_beta.py

import pygame
import sys
import os
import random
import time
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_img(name, w, h):
   path = os.path.join(main_dir,"images",name)
   return pygame.transform.scale(pygame.image.load(path), (w,h))

class Enemies:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_img('meteor.png', 80, 55)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Player:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_img('p1.png', 70, 80)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

def main():
    pygame.init()
    pygame.font.init()

    # DISPLAY
    WIDTH, HEIGHT = 700, 400
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ChocoRocket")

    # Background
    BG = pygame.transform.scale(pygame.image.load("images/bg.png"), (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    lives = 3
    score = 0
    font = pygame.font.SysFont("comicsans", 40)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    game_over = font.render("Game Over!", True, WHITE)

    x, y = 0, 200 
    vel = 4.5
    vel_meteor = 4
    player = Player(x, y)
    meteor = Enemies(660, random.randint(15, 345))

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # label score and lives on the screen
        lives_label = font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = font.render(f"Score: {score}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))

        # drawing the player
        player.draw(WIN)
        
        # drawing the meteor
        meteor.draw(WIN)

        pygame.display.update()

    def colision():
        # check for vertical collision
        if meteor.x <= (player.x+70):
            # check for horizontal collision
            if 0 < (player.y - meteor.y) < 50 or 0 < (meteor.y - player.y) < 80:
                return True

        return False

    # Game loop
    while True:
        clock.tick(60)
        redraw_window()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and player.y - vel > 20:
            player.y -= vel
        if keys[pygame.K_DOWN] and player.y + vel + 80 < HEIGHT:
            player.y += vel
        
        meteor.x -= vel_meteor

        if meteor.x == player.x or meteor.x < player.x:
            # check for collision
            if colision():
                lives -= 1

            meteor.y = random.randint(32, 400-55)
            meteor.x = 660
            score += 1
            vel_meteor +=  0.5
            if vel_meteor > 12:
                vel_meteor = 12

        if lives == 0:
            time.sleep(1)

            WIN.fill(BLACK)
            WIN.blit(game_over, (260,180))
            pygame.display.update()

            time.sleep(2)
            
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
    