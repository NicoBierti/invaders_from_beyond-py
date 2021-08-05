import pygame
import random
import math

# Initialize pygame
pygame.init()

# Creating the window
screen = pygame.display.set_mode((800,600)) # Window size, x and y from left top corner

# Background
background = pygame.image.load("Art\\background_0.jpg")

# Title and Icon
pygame.display.set_caption("Invasores del Mas Alla")
icon = pygame.image.load('Art\\icon.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('Art\\player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_image = pygame.image.load('Art\\enemy.png')
enemy_x = random.randint(0,735)
enemy_y = random.randint(50,150)
enemy_x_change = 0.3
enemy_y_change = 40

# Bullet
bullet_image = pygame.image.load('Art\\bullet.png')
bullet_x = 0
bullet_y = 480
bullet_y_change = 0.75
bullet_state = "ready" # Ready - you cant see the bullet

score = 0

def player(x, y):
    screen.blit(player_image,(x, y)) # Draw the player imagine on our window

def enemy(x, y):
    screen.blit(enemy_image,(x, y))

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
    enemy_x += enemy_x_change
    # Movement Boundaries
    if enemy_x <= -4:
        enemy_x_change = 0.2
        enemy_y += enemy_y_change
    elif enemy_x >= 740: # 800 - x (x is aprox. the size of the ship)
        enemy_x_change = -0.2
        enemy_y += enemy_y_change

    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Collision
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score += 1
        print(score)
        enemy_x = random.randint(0,735)
        enemy_y = random.randint(50,150)


    player(player_x, player_y) # loads player into window
    enemy(enemy_x, enemy_y)
    pygame.display.update()