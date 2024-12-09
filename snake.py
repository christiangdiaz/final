# Authors   : Christian Diaz
# Emails    : cgdiaz@umass.edu
# Spire IDs : 34834736

import pygame
import pygame.freetype
import random
import os

pygame.init()
screen = pygame.display.set_mode((400, 400))
screen_width, screen_height = screen.get_size()
rect_width, rect_height = 20, 20
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font = pygame.freetype.SysFont("Arial", 24)

def load_scores():
    if not os.path.exists('highscores.txt'):
        open('highscores.txt', 'a').close()
    scores = []
    with open('highscores.txt', 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                name = " ".join(parts[:-1])
                sc = int(parts[-1])
                scores.append((sc, name))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:5]

def draw_text_centered(text, size, color, y_offset=0):
    text_surface, _ = font.render(text, color)
    x = (screen_width - text_surface.get_width()) / 2
    y = (screen_height - text_surface.get_height()) / 2 + y_offset
    screen.blit(text_surface, (x, y))

class SnakeSegment:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
    def draw(self):
        pygame.draw.rect(screen, GREEN, (*self.pos, rect_width, rect_height))

class Snake:
    def __init__(self):
        self.segments = [SnakeSegment(screen_width // 2, screen_height // 2)]
    def move(self, velocity_x, velocity_y):
        if velocity_x == 0 and velocity_y == 0:
            return False, None
        tail_position = self.segments[-1].pos.copy()
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].pos = self.segments[i - 1].pos.copy()
        self.segments[0].pos.x += velocity_x * rect_width
        self.segments[0].pos.y += velocity_y * rect_width
        if (self.segments[0].pos.x < 0 or
            self.segments[0].pos.x >= screen_width or
            self.segments[0].pos.y < 0 or
            self.segments[0].pos.y >= screen_height):
            return True, tail_position
        return False, tail_position
    def grow(self, tail_position):
        self.segments.append(SnakeSegment(tail_position.x, tail_position.y))
    def draw(self):
        for segment in self.segments:
            segment.draw()
    def check_self_collision(self):
        head_pos = self.segments[0].pos
        for segment in self.segments[1:]:
            if segment.pos == head_pos:
                return True
        return False

def generate_fruit_position(snake_positions):
    while True:
        x = random.randint(0, screen_width // rect_width - 1) * rect_width
        y = random.randint(0, screen_height // rect_height - 1) * rect_height
        if (x, y) not in snake_positions:
            return pygame.Vector2(x, y)

def get_snake_positions(snake):
    return {(int(seg.pos.x), int(seg.pos.y)) for seg in snake.segments}

def draw_start_screen(top_scores):
    screen.fill(BLACK)
    draw_text_centered("Snake Game", 64, WHITE, -150)
    draw_text_centered("Press SPACE to Start", 24, WHITE, 150)
    y_offset = -40
    draw_text_centered("Top Scores", 15, WHITE, -75)
    for i, (sc, nm) in enumerate(top_scores):
        draw_text_centered(f"{i+1}. {nm}: {sc}", 10, WHITE, y_offset)
        y_offset += 30
    pygame.display.flip()

def draw_game_screen(snake, fruit_pos, score):
    screen.fill(BLACK)
    snake.draw()
    pygame.draw.rect(screen, RED, (*fruit_pos, rect_width, rect_height))
    score_text = f"Score: {score}"
    text_surface, _ = font.render(score_text, WHITE)
    screen.blit(text_surface, (10, 10))
    pygame.display.flip()

def draw_game_over_screen(score, show_restart, user_text, name_entered):
    screen.fill(BLACK)
    draw_text_centered("Game Over", 32, WHITE, -30)
    draw_text_centered(f"Score: {score}", 24, WHITE, 10)
    if show_restart and not name_entered:
        draw_text_centered("Enter your name:", 16, WHITE, 50)
        input_rect = pygame.Rect((screen_width//2)-70, (screen_height//2)+90, 140, 32)
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        text_surface, _ = font.render(user_text, WHITE)
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        draw_text_centered("Press ENTER to Save Score", 16, WHITE, 140)
    if show_restart and name_entered:
        draw_text_centered("Press R to Restart or Q to Quit", 16, WHITE, 100)
    pygame.display.flip()

def main():
    running = True
    state = "START"
    velocity_x = 0
    velocity_y = 0
    current_direction = None
    score = 0
    snake = None
    fruit_pos = None
    game_over_time = None
    game_over_delay = 2000
    user_text = ""
    name_entered = False

    while running:
        if state == "START":
            top_scores = load_scores()
            draw_start_screen(top_scores)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    score = 0
                    snake = Snake()
                    snake_positions = get_snake_positions(snake)
                    fruit_pos = generate_fruit_position(snake_positions)
                    velocity_x = 0
                    velocity_y = 0
                    current_direction = None
                    name_entered = False
                    user_text = ""
                    state = "GAME"
            clock.tick(10)
            continue

        elif state == "GAME":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
            collision, tail_position = snake.move(velocity_x, velocity_y)
            if collision or snake.check_self_collision():
                state = "GAME_OVER"
                game_over_time = pygame.time.get_ticks()
                user_text = ""
                name_entered = False
            head_rect = pygame.Rect(*snake.segments[0].pos, rect_width, rect_height)
            fruit_rect = pygame.Rect(*fruit_pos, rect_width, rect_height)
            if head_rect.colliderect(fruit_rect):
                score += 1
                snake_positions = get_snake_positions(snake)
                fruit_pos = generate_fruit_position(snake_positions)
                snake.grow(tail_position)
            draw_game_screen(snake, fruit_pos, score)
            clock.tick(10)
            continue

        elif state == "GAME_OVER":
            elapsed = pygame.time.get_ticks() - game_over_time if game_over_time else 0
            show_restart = elapsed > game_over_delay
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if show_restart and event.type == pygame.KEYDOWN:
                    if not name_entered:
                        if event.key == pygame.K_RETURN:
                            if user_text.strip():
                                with open('highscores.txt', 'a') as f:
                                    f.write(f"{user_text.strip()} {score}\n")
                            name_entered = True
                        elif event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            if event.unicode.isprintable():
                                user_text += event.unicode
                    else:
                        if event.key == pygame.K_r:
                            state = "START"
                        elif event.key == pygame.K_q:
                            running = False
            draw_game_over_screen(score, show_restart, user_text, name_entered)
            clock.tick(10)
            continue

    pygame.quit()

if __name__ == "__main__":
    main()
