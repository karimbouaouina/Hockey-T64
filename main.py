import pygame
from pygame.locals import *
from pygame import mixer
import os
import time
pygame.init()
pygame.key.set_repeat(400, 30)
screen_width = 1920
screen_height = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
score1 = 0
score2 = 0
start_time = time.time()
duration = 15
window = pygame.display.set_mode((1920, 1080))
tutorial = pygame.image.load("tutorial.jpg")
mixer.init()
mixer.music.load('mainmenu.mp3')
mixer.music.set_volume(0.35)
mixer.music.play(-1)
print("Press + to unmute music")
print("Press - to mute music")

game_dir = os.path.dirname(__file__)
gamebackground = os.path.join(game_dir, 'newb.jpg')
blue_paddle = pygame.image.load("bluePaddle.png")
blue_paddle = pygame.transform.scale(blue_paddle, (60, 50))
red_paddle = pygame.image.load("redPaddle.png")
red_paddle = pygame.transform.scale(red_paddle, (60, 50))
puck = pygame.image.load("puck.png")
puck = pygame.transform.scale(puck, (110, 110))
puck_x = screen_width // 2
puck_y = screen_height // 2
puck_speed_x = 5.8
puck_speed_y = 5.8
blue_paddle_x = 30
blue_paddle_y = screen_height // 2 - blue_paddle.get_height() // 2
red_paddle_x = screen_width - 30 - red_paddle.get_width()
red_paddle_y = screen_height // 2 - red_paddle.get_height() // 2
clock = pygame.time.Clock()
def main_menu():

    backgrounds = ["mmopt1.jpg", "mmopt2.jpg", "mmopt3.jpg"]
    global current_background
    current_background = 0
    global background
    background = pygame.image.load(backgrounds[current_background])
    window.blit(background, (0, 0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RIGHT:
                current_background = (current_background + 1) % len(backgrounds)
                background = pygame.image.load(backgrounds[current_background])
                window.blit(background, (0, 0))
                pygame.display.update()
            elif ev.key == pygame.K_KP_PLUS:
                mixer.music.unpause()
            elif ev.key == pygame.K_KP_MINUS:
                mixer.music.pause()
            elif ev.key == pygame.K_ESCAPE:
                if current_background == 1:
                    current_background = 0
                    background = pygame.image.load(backgrounds[current_background])
            elif ev.key == pygame.K_RETURN:
                break
        if ev.type == QUIT:
            pygame.quit()
            quit()
    pygame.display.update()

#Loop for the window
running = True
mainmenu = True
while running:
    if mainmenu:
        main_menu()
        mainmenu= False
        background = pygame.image.load(gamebackground)
        background.convert_alpha()
    if current_background == 1:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                background = tutorial
                window.blit(background, (0, 0))
                pygame.display.update()
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainmenu = True
    elif current_background == 0:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_z:
                blue_paddle_y -= 20
            elif ev.key == pygame.K_s:
                blue_paddle_y += 20
            if ev.key == pygame.K_UP:
                red_paddle_y -= 20
            elif ev.key == pygame.K_DOWN:
                red_paddle_y += 20
            if ev.key == pygame.K_ESCAPE:
                mainmenu = True
        if(red_paddle_y + 60 > 1080):
            red_paddle_y = 1080 - 60
        if (red_paddle_y - 10 < 0):
            red_paddle_y = 0 + 10
        if (blue_paddle_y + 60 > 1080):
            blue_paddle_y = 1080 - 60
        if (blue_paddle_y - 10 < 0):
            blue_paddle_y = 0 + 10
        puck_x += puck_speed_x
        puck_y += puck_speed_y
        if puck_y < 0 or puck_y > screen_height - puck.get_height():
            puck_speed_y *= -1
        if puck_x < 0 or puck_x > screen_width - puck.get_width():
            puck_speed_x *= -1
        if (puck_x < blue_paddle_x + blue_paddle.get_width() and
                puck_y + puck.get_height() > blue_paddle_y and
                puck_y < blue_paddle_y + blue_paddle.get_height()):
            puck_speed_x *= -1
        if (puck_x + puck.get_width() > red_paddle_x and
                puck_y + puck.get_height() > red_paddle_y and
                puck_y < red_paddle_y + red_paddle.get_height()):
            puck_speed_x *= -1
        # Collision with walls
        if puck_x < 0:
            score2 += 1
            puck_x = screen_width // 2
            puck_y = screen_height // 2
        if puck_x + puck.get_width() > screen_width:
            score1 += 1
            puck_x = screen_width // 2
            puck_y = screen_height // 2
        if puck_y <= 0:
            puck_y = 0
        elif puck_y + puck.get_height() >= screen_height:
            puck_y = screen_height - puck.get_height()

        if puck_y + puck.get_height() >= screen_height - 1:
            puck_y = screen_height - puck.get_height()

        # Collision with paddles
        if blue_paddle_x + blue_paddle.get_width() > puck_x > blue_paddle_x and blue_paddle_y + blue_paddle.get_height() > puck_y > blue_paddle_y:
            puck_speed_x = abs(puck_speed_x)
        if red_paddle_x < puck_x + puck.get_width() < red_paddle_x + blue_paddle.get_width() and red_paddle_y + blue_paddle.get_height() > puck_y > red_paddle_y:
            puck_speed_x = -abs(puck_speed_x)

        font = pygame.font.Font(pygame.font.match_font('poppins'), 68)

        # Game status depending on score
        if time.time() - start_time > duration:
            window.fill(BLACK)

            if score1 > score2:
                text = "Player 1 wins!"
                text_surface = font.render(text, True, WHITE)
                window.blit(text_surface, (screen_width / 2 - text_surface.get_width() / 2, screen_height / 2 - text_surface.get_height() / 2))
            elif score2 > score1:
                text = "Player 2 wins!"
                text_surface = font.render(text, True, WHITE)
                window.blit(text_surface, (screen_width / 2 - text_surface.get_width() / 2, screen_height / 2 - text_surface.get_height() / 2))
            else:
                text = "It's a tie!"
                text_surface = font.render(text, True, WHITE)
                window.blit(text_surface, (screen_width / 2 - text_surface.get_width() / 2, screen_height / 2 - text_surface.get_height() / 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False
        window.blit(background, (0, 0))
        window.blit(blue_paddle, (blue_paddle_x, blue_paddle_y))
        window.blit(red_paddle, (red_paddle_x, red_paddle_y))
        window.blit(puck, (puck_x, puck_y))

        text = str(score1) + " - " + str(score2)
        text_surface = font.render(text, True, WHITE)  ## True denotes the font to be anti-aliased
        text_rect = text_surface.get_rect()
        text_rect.midtop = (screen_width / 2, 10)
        window.blit(text_surface, text_rect)

        text = str(int(duration - (time.time() - start_time))) + "s"
        text_surface = font.render(text, True, WHITE)  ## True denotes the font to be anti-aliased
        text_rect = text_surface.get_rect()
        text_rect.midtop = (screen_width / 2, 60)
        window.blit(text_surface, text_rect)

        pygame.display.update()
        clock.tick(60)
    elif current_background == 2:
        running = False


pygame.quit()