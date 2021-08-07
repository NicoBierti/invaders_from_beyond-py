import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Creating the window
screen = pygame.display.set_mode((800,600)) # Window size, x and y from left top corner

# Background
background = pygame.image.load('Art\\background_0.jpg')

# Background Music
mixer.music.load('Sounds\\background.mp3')
mixer.music.play(-1) # -1 is to play song in an endless loop

# Title and Icon
pygame.display.set_caption('Invaders from Beyond')
icon = pygame.image.load('Art\\icon.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('Art\\player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('Art\\enemy.png'))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

# Bullet
bullet_image = pygame.image.load('Art\\bullet.png')
bullet_x = 0
bullet_y = 480
bullet_y_change = 0.75
bullet_state = "ready" # Ready - you cant see the bullet

# Score Text
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 30)
text_x = 10 # x coordinate
text_y = 10 # y coordinate

# Game Over Text
game_over_font = pygame.font.Font("freesansbold.ttf", 70)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text,(200, 250))

def player(x, y):
    screen.blit(player_image,(x, y)) # Draw the player imagine on our window

def enemy(x, y, i):
    screen.blit(enemy_image[i],(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image,(x + 16, y + 10)) # 16 and 10 are the position where the bullet begins

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x,2)) + (math.pow(enemy_y - bullet_y,2)))
    if distance < 27:
        return True
    else:
        return False



# Game main loop
running = True
while running:
    # Background color (RGB)
    screen.fill((211,211,211))
    # Background Image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # If a key is pressed check whether its to the right or the left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('Sounds\\laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    # Movement Boundaries
    if player_x <= -4:
        player_x = -4
    elif player_x >= 740: # 800 - x (x is aprox. the size of the ship)
        player_x = 740

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000 # make enemy dissapear from the screen by moving them to 2000 coordinate
            show_game_over()
            break

        enemy_x[i] += enemy_x_change[i]
        # Movement Boundaries
        if enemy_x[i] <= -4:
            enemy_x_change[i] = 0.2
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 740: # 800 - x (x is aprox. the size of the ship)
            enemy_x_change[i] = -0.2
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('Sounds\\hit.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0,735)
            enemy_y[i] = random.randint(50,150)

        enemy(enemy_x[i], enemy_y[i], i)


    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    player(player_x, player_y) # loads player into window
    show_score(text_x, text_y)
    pygame.display.update()