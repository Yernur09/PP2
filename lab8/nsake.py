import pygame
import time
import random

snake_speed = 15

# Window dimensions
window_x = 720
window_y = 480

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialize pygame
pygame.init()

# Initialize the game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
fps = pygame.time.Clock()

# Initial position of the snake
snake_position = [100, 50]

# Initial snake body (4 blocks long)
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# Fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# Initial snake movement direction
direction = 'RIGHT'
change_to = direction

# Initial score and level
score = 0
level = 1
food_count = 0  # Counter for collected food to increase level


# Function to display the score and level
def show_score(choice, color, font, size):
    # Create font object for score and level
    score_font = pygame.font.SysFont(font, size)

    # Create surface object for score and level
    score_surface = score_font.render('Score : ' + str(score), True, color)
    level_surface = score_font.render('Level : ' + str(level), True, color)

    # Create rectangle objects for positioning score and level text
    score_rect = score_surface.get_rect()
    level_rect = level_surface.get_rect()

    # Display score and level on the screen
    game_window.blit(score_surface, score_rect)
    game_window.blit(level_surface, (window_x - level_rect.width - 10, 10))


# Function to end the game and display final score
def game_over():
    # Create font object for game over text
    my_font = pygame.font.SysFont('times new roman', 50)

    # Create surface object for displaying final score
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)

    # Create rectangle object for positioning game over text
    game_over_rect = game_over_surface.get_rect()

    # Position the game over text at the top center of the window
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # Blit the game over text on the screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # Wait for 2 seconds before quitting the game
    time.sleep(2)

    # Deactivate pygame and close the game
    pygame.quit()

    # Exit the program
    quit()


# Main Function
while True:

    # Handle key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Ensure the snake doesn't reverse direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake in the direction chosen
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Add the new head position to the snake body
    snake_body.insert(0, list(snake_position))

    # Check if the snake has eaten the food
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += level * 10  # The score increases based on the level
        food_count += 1
        fruit_spawn = False
    else:
        # Remove the last part of the snake body (tail)
        snake_body.pop()

    # If the food was eaten, generate a new food position
    if not fruit_spawn:
        while True:
            # Ensure the food doesn't spawn on the snake's body
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]
            if fruit_position not in snake_body:
                break

    fruit_spawn = True
    game_window.fill(black)

    # Draw each part of the snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the food
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Check for collisions with the wall
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Check if the snake collides with itself
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Level up after collecting 4 food items (can be adjusted)
    if food_count >= 4:
        level += 1  # Increase level
        snake_speed += 2  # Increase speed for the next level
        food_count = 0  # Reset food counter for the next level

    # Display score and level continuously
    show_score(1, white, 'times new roman', 20)

    # Refresh the game screen
    pygame.display.update()

    # Control the game speed based on the snake's speed
    fps.tick(snake_speed)