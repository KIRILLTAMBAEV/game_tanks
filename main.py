import pgzrun
import pygame.mixer
import random
import os
from math import atan2, cos, sin

TITLE = "Zombies vs Tanks"
WIDTH = 800
HEIGHT = 640

UP = 180
DOWN = 0
LEFT = 270
RIGHT = 90
BULLET_SPEED = 10

background_music = os.path.abspath("sounds/your_background_music.mp3")
pygame.mixer.music.load(background_music)
laser_sound = sounds.laserretro_004
background_menu = pygame.image.load("images/poster.png")
background_game_over = pygame.image.load("images/background_game_over.png")

blue_tank = Actor("tank_blue")
blue_tank.x = WIDTH / 2
blue_tank.y = HEIGHT / 2

bullets = []
bullet_fired = False

zombie_list = []
ZOMBIE_SPEED = 1

score = 0
game_over = False
restart_prompt = False

in_main_menu = True
play_game = False
music_enabled = True
sound_enabled = True

def create_zombies():
    if len(zombie_list) < 50:
        loc_rand = random.randint(0, 3)
        zombie_frames = [f"zombie_{i}.png" for i in range(1, 5)]
        if loc_rand == 0:
            y = random.randint(40, HEIGHT - 40)
            zombie = Actor(zombie_frames[0], (1, y), scale=2)
        elif loc_rand == 1:
            y = random.randint(40, HEIGHT - 40)
            zombie = Actor(zombie_frames[0], (WIDTH - 1, y), scale=2)
        elif loc_rand == 2:
            x = random.randint(40, WIDTH - 40)
            zombie = Actor(zombie_frames[0], (x, 1), scale=2)
        elif loc_rand == 3:
            x = random.randint(40, WIDTH - 40)
            zombie = Actor(zombie_frames[0], (x, HEIGHT - 1), scale=2)
        zombie.images = zombie_frames
        zombie.frame = 0
        zombie_list.append(zombie)
        
        
def draw():
    screen.clear()

    if in_main_menu:
        draw_main_menu()
    elif play_game:
        draw_game()
    if game_over == True:
        draw_game_over()
        
        
x = (WIDTH - background_game_over.get_width()) / 2
y = (HEIGHT - background_game_over.get_height()) / 2


def draw_game_over():
    screen.blit(background_game_over, (x, y))
    screen.draw.text(f"GAME OVER, Your score: {score}", (115, 230), fontsize=60, color="white")
    screen.draw.text("Press ENTER to restart", (235, 280), fontsize=40, color="white")
    
    
x = (WIDTH - background_menu.get_width()) / 2
y = (HEIGHT - background_menu.get_height()) / 2


def draw_main_menu():
    screen.blit(background_menu, (x, y))
    screen.draw.text("Zombies vs Tanks", (215, 150), fontsize=60, color="red")
    screen.draw.text("1. TO Start Game press SPACE", (215, 300), fontsize=30, color="white")
    screen.draw.text("2. TO Toggle Music press M (Currently: {})".format("On" if music_enabled else "Off"), (215, 350), fontsize=30, color="white")
    screen.draw.text("3. TO Quit press Q", (215, 400), fontsize=30, color="white")
    screen.draw.text("4. TO Toggle Sounds press S", (215, 450), fontsize=30, color="white")
    if music_enabled:
        pygame.mixer.music.play(-1)

def draw_game():
    screen.blit("tank.png", (0, 0))
    blue_tank.draw()
    for bullet in bullets:
        bullet.draw()

    for zombie in zombie_list:
        zombie.draw()

    screen.draw.text(f"Score: {score}", (350, 150))

def restart_game():
    global game_over, restart_prompt, score, blue_tank, bullets, zombie_list
    game_over = False
    restart_prompt = False
    score = 0
    blue_tank.x = WIDTH / 2
    blue_tank.y = HEIGHT / 2
    bullets = []
    zombie_list = []
    clock.schedule_interval(create_zombies, zombie_create_interval)

def move_player():
    if keyboard.left:
        blue_tank.x -= 5
        blue_tank.angle = LEFT
    if keyboard.right:
        blue_tank.x += 5
        blue_tank.angle = RIGHT
    if keyboard.up:
        blue_tank.y -= 5
        blue_tank.angle = UP
    if keyboard.down:
        blue_tank.y += 5
        blue_tank.angle = DOWN

    if keyboard.space and not bullet_fired:
        shoot_bullet()

def shoot_bullet():
    global bullet_fired
    if not bullet_fired:
        bullet_fired = True
        sounds.laserretro_004.play()

        bullet = Actor("bulletblue", anchor=("center", "center"))
        bullet.x = blue_tank.x
        bullet.y = blue_tank.y
        bullet.angle = blue_tank.angle
        bullets.append(bullet)

        clock.schedule_unique(reset_bullet_flag, 1.0)

def reset_bullet_flag():
    global bullet_fired
    bullet_fired = False

def move_bullets():
    for bullet in bullets:
        if bullet.angle == LEFT:
            bullet.x -= BULLET_SPEED
        elif bullet.angle == RIGHT:
            bullet.x += BULLET_SPEED
        elif bullet.angle == DOWN:
            bullet.y += BULLET_SPEED
        elif bullet.angle == UP:
            bullet.y -= BULLET_SPEED

        if (
            bullet.x >= WIDTH
            or bullet.x <= 0
            or bullet.y >= HEIGHT
            or bullet.y <= 0
        ):
            bullets.remove(bullet)
            bullet_fired = False

def on_key_down(key):
    global in_main_menu, play_game, music_enabled, sound_enabled
    if in_main_menu:
        if key == keys.SPACE:
            in_main_menu = False
            play_game = True
            start_game()
        elif key == keys.M:
            music_enabled = not music_enabled
            if music_enabled:
                pygame.mixer.music.play(-1)
                if sound_enabled:
                    laser_sound.play()
            else:
                pygame.mixer.music.stop()
                laser_sound.stop()
        elif key == keys.Q:
            quit()
        elif key == keys.S:
            sound_enabled = not sound_enabled
            if not sound_enabled:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()

def update(dt):
    if play_game:
        update_game(dt)

def update_game(dt):
    global game_over, restart_prompt, play_game
    print(f"game_over: {game_over}, restart_prompt: {restart_prompt}")
    if not game_over:
        move_player()
        move_zombies()
        move_bullets()
        check_collisions()
    else:
        restart_prompt = True

        if game_over and restart_prompt:
            if keyboard.RETURN:
                restart_game()
                game_over = False
                restart_prompt = False

    if play_game:
        draw_game()

    if game_over:
        draw_game_over()

def start_game():
    global in_main_menu, play_game, music_enabled, sound_enabled
    in_main_menu = False
    play_game = True

    if music_enabled:
        pygame.mixer.music.play(-1)

def move_zombies():
    for zombie in zombie_list:
        angle = atan2(blue_tank.y - zombie.y, blue_tank.x - zombie.x)
        zombie.x += 2 * ZOMBIE_SPEED * cos(angle)
        zombie.y += 2 * ZOMBIE_SPEED * sin(angle)

        zombie.frame = (zombie.frame + 0.1) % len(zombie.images)
        zombie.image = zombie.images[int(zombie.frame)]

def check_collisions():
    global score, game_over, restart_prompt
    for zombie in zombie_list:
        for bullet in bullets:
            if bullet.colliderect(zombie):
                zombie_list.remove(zombie)
                bullets.remove(bullet)
                score += 1
                break

    for zombie in zombie_list:
        if zombie.colliderect(blue_tank):
            game_over = True
            restart_prompt = True
            draw_game_over() 

zombie_create_interval = 1
clock.schedule_interval(create_zombies, zombie_create_interval)

pgzrun.go()







   


