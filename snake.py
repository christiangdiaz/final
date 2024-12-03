import pygame
import pygame.freetype
import random

pygame.init()

screen = pygame.display.set_mode((400, 400))
screen_width = screen.get_width()
screen_height = screen.get_height()
rect_width, rect_height = 20, 20

clock = pygame.time.Clock()
running = True
dt = 0

velocity_y = 0
velocity_x = 0
player_pos = pygame.Vector2(screen_width / 2, screen_height / 2)

current_direction = None

fruit_pos = pygame.Vector2(
    random.randint(0, screen_width - rect_width),
    random.randint(0, screen_height - rect_height)
)

score = 0
font = pygame.freetype.SysFont("Arial", 24)

def draw_fruit(fruit_pos):
    pygame.draw.rect(screen, "red", (*fruit_pos, rect_width, rect_height))

def check_collision(player_rect, fruit_rect):
    return player_rect.colliderect(fruit_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.draw.rect(screen, "green", (player_pos.x, player_pos.y, rect_width, rect_height))

    draw_fruit(fruit_pos)

    score_text = f"Score: {score}"
    text_surface, _ = font.render(score_text, "white")
    screen.blit(text_surface, (screen_width / 2 - text_surface.get_width() / 2, 10))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and current_direction != "DOWN":  
        velocity_y = -1
        velocity_x = 0
        current_direction = "UP"
    elif keys[pygame.K_DOWN] and current_direction != "UP":  
        velocity_y = 1
        velocity_x = 0
        current_direction = "DOWN"
    elif keys[pygame.K_LEFT] and current_direction != "RIGHT":  
        velocity_x = -1
        velocity_y = 0
        current_direction = "LEFT"
    elif keys[pygame.K_RIGHT] and current_direction != "LEFT":  
        velocity_x = 1
        velocity_y = 0
        current_direction = "RIGHT"

    speed = 150  
    player_pos.x += velocity_x * dt * speed
    player_pos.y += velocity_y * dt * speed

    player_pos.x = max(0, min(player_pos.x, screen_width - rect_width))
    player_pos.y = max(0, min(player_pos.y, screen_height - rect_height))

    player_rect = pygame.Rect(player_pos.x, player_pos.y, rect_width, rect_height)
    fruit_rect = pygame.Rect(fruit_pos.x, fruit_pos.y, rect_width, rect_height)

    if check_collision(player_rect, fruit_rect):
        score += 1
        fruit_pos = pygame.Vector2(
            random.randint(0, screen_width - rect_width),
            random.randint(0, screen_height - rect_height)
        )

    pygame.display.flip()

    dt = clock.tick(60) / 1000  

pygame.quit()
