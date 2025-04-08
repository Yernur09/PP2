from itertools import chain
import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Creating game window with correct dimensions

background = pygame.image.load("C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/images/AnimatedStreet.png")

clock = pygame.time.Clock()
FPS = 60  # setting FPS

player_img = pygame.image.load('C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/images/Player.png')
enemy_img = pygame.image.load('C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/images/Enemy.png')
coin_img = pygame.image.load('C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/images/coin.png')

background_music = pygame.mixer.music.load('C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/sounds/Teriyaki_Boyz_-_Tokyo_Drift-(MyMp3Singer.net).mp3')
crash_sound = pygame.mixer.Sound('C:/Users/ernur/OneDrive/Desktop/PP Labs/lab8/sounds/crash.wav')

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, "black")

pygame.mixer.music.play(-1)  # plays background music in a loop

PLAYER_SPEED = 5
ENEMY_SPEED = 10
score = 0
coin_score = 0

# Player class to control player's movement
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.w // 2
        self.rect.y = HEIGHT - self.rect.h
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0)  # move in place
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)  # move in place
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Enemy class that creates enemies and moves them down
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.generate_random_rect()
    
    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()
    
    def generate_random_rect(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = 0

# Coin class to generate coins that fall down
class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        # Creating a safe range so that coins don't overlap with enemies
        coord_range = list(chain(range(22, enemy.rect.center[0] - 24 - 22), range(enemy.rect.center[0] + 24 + 22, WIDTH - 22)))
        self.rect.center = (random.choice(coord_range), 0)
    
    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED)  # Move the coin down the screen
        if self.rect.top > HEIGHT:  # Reset the coin to the top if it goes off the screen
            coord_range = list(chain(range(22, WIDTH - 22), range(22, WIDTH - 22)))  # Random X position for coin
            self.rect.center = (random.choice(coord_range), 0)  # Place at a random position at the top

# Initializing sprites
player = Player()  # player's sprite
enemy = Enemy()  # enemy's sprite
coin = Coin(enemy)

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
car_sprites = pygame.sprite.Group()

car_sprites.add([player, enemy])
all_sprites.add([player, enemy, coin])
enemy_sprites.add([enemy])
coins_group.add(coin)

# Event for increasing speed (optional for this task)
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

running = True

# Game loop
while running:
    for event in pygame.event.get():  # Event loop
        if event.type == pygame.QUIT:
            running = False
    
    # Move the player and the enemy
    player.move()
    enemy.move()

    # Check for coin collection
    collected_coins = pygame.sprite.spritecollide(player, coins_group, True)  # Check if the player collects any coin
    for collected_coin in collected_coins:
        coin_score += 1  # Increment the coin score
        new_coin = Coin(enemy)  # Create a new coin at a new position
        coins_group.add(new_coin)  # Add the new coin to the group
        all_sprites.add(new_coin)  # Add new coin to all_sprites group

    # Move all coins
    for coin in coins_group:
        coin.move()  # Ensure all coins, including new ones, move down

    # Draw background and sprites
    screen.blit(background, (0, 0))
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # Display the collected coins score in the top right corner
    score_text = font.render(f"Coins: {coin_score}", True, "black")
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))  # Position the score at the top right
    
    # Check if the player collides with the enemy
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        crash_sound.play()
        time.sleep(1)

        screen.fill("red")
        center_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over, center_rect)

        pygame.display.flip()

        time.sleep(2)
        running = False
    
    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()