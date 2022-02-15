import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learning Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH//2) - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRED_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
COUNTDOWN_FONT = pygame.font.SysFont('comicsans', 60)

VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
FPS = 60
SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)), 270)

SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE_BG, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f'Health: {red_health}', True, WHITE)
    yellow_health_text = HEALTH_FONT.render(f'Health: {yellow_health}', True, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(text, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    countdown = True
    countdown_time = 5

    while countdown:
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        draw_text = WINNER_FONT.render(text, True, WHITE)
        WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))

        countdown_text = COUNTDOWN_FONT.render(str(countdown_time), True, WHITE)
        WIN.blit(countdown_text, (WIDTH//2 - countdown_text.get_width()//2, HEIGHT//2 + draw_text.get_height()//2))
        pygame.display.update()

        countdown_time -= 1
        if countdown_time == 0:
            countdown = False
        pygame.time.delay(1000)


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - yellow.width:  # RIGHT
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 10:  # UP
        yellow.y -= VEL

    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - yellow.height:  # DOWN
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - red.width:  # RIGHT
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL > 10:  # UP
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - red.height:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if bullet.x < 0:
            red_bullets.remove(bullet)

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(800, 300, SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH)
    yellow = pygame.Rect(100, 300, SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRED_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRED_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = 'Yellow Wins!'
        if yellow_health <= 0:
            winner_text = 'Red Wins!'

        if winner_text:
            draw_winner(winner_text, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    main()


if __name__ == '__main__':
    main()
