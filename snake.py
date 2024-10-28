import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
dt = 0
velocity_y = 0
velocity_x = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.rect(screen, "green", (player_pos.x, player_pos.y, 20, 20))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        velocity_y = -300
        velocity_x = 0
        # player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        velocity_y = 300
        velocity_x = 0
        # player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        velocity_x = -300
        velocity_y = 0
        # player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        velocity_x = 300
        velocity_y = 0
        # player_pos.x += 300 * dt

    player_pos.x += velocity_x * dt
    player_pos.y += velocity_y * dt


    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 2250

pygame.quit()