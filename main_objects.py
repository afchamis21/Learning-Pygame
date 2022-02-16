import pygame
import os

pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


class Spaceship:
    def __init__(self, width: int, height: int, rotation: int, x_pos: int, y_pos: int, speed: int, parent: object, color='red' or 'yellow'):
        match color:
            case 'red':
                spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
                self.spaceship = pygame.transform.rotate(
                    pygame.transform.scale(spaceship_image, (width, height)), rotation)
                self.red = pygame.Rect(x_pos, y_pos, height, width)
            case 'yellow':
                spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
                self.spaceship = pygame.transform.rotate(
                    pygame.transform.scale(spaceship_image, (width, height)), rotation)
                self.yellow = pygame.Rect(x_pos, y_pos, height, width)

        self.x = x_pos
        self.initial_x = x_pos
        self.y = y_pos
        self.initial_y = y_pos
        self.color = color
        self.speed = speed
        self.width = height
        self.height = width
        self.parent = parent
        self.bullet_limit = 5
        self.bullet_list = []
        self.health = 10

    def reset_all(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.bullet_list = []
        self.health = 10

    def handle_movement(self, keys_pressed):
        match self.color:
            case 'red':
                if keys_pressed[pygame.K_LEFT] and self.x - self.speed > self.parent.border.x + self.parent.border.width:  # LEFT
                    self.red.x -= self.speed
                    self.x = self.red.x

                if keys_pressed[pygame.K_RIGHT] and self.x + self.speed < self.parent.width - self.width:  # RIGHT
                    self.red.x += self.speed
                    self.x = self.red.x
        
                if keys_pressed[pygame.K_UP] and self.y - self.speed > 10:  # UP
                    self.red.y -= self.speed
                    self.y = self.red.y

                if keys_pressed[pygame.K_DOWN] and self.y + self.speed < self.parent.height - self.height:  # DOWN
                    self.red.y += self.speed
                    self.y = self.red.y
            
            case 'yellow':
                if keys_pressed[pygame.K_a] and self.x - self.speed > 0:  # LEFT
                    self.yellow.x -= self.speed
                    self.x = self.yellow.x

                if keys_pressed[pygame.K_d] and self.x + self.speed < self.parent.border.x - self.width:  # RIGHT
                    self.yellow.x += self.speed
                    self.x = self.yellow.x
        
                if keys_pressed[pygame.K_w] and self.y - self.speed > 10:  # UP
                    self.yellow.y -= self.speed
                    self.y = self.yellow.y

                if keys_pressed[pygame.K_s] and self.y + self.speed < self.parent.height - self.height:  # DOWN
                    self.yellow.y += self.speed
                    self.y = self.yellow.y


class Window:
    def __init__(self, width: int, height: int, name: str):
        self.width = width
        self.height = height
        self.dependencies = {}
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(name)
        self.border = pygame.Rect((self.width // 2) - 5, 0, 10, self.height)

        red_spaceship = Spaceship(55, 40, 270, 800, 300, 5, self, color='red')
        self.add_dependencies('red_spaceship', red_spaceship)

        yellow_spaceship = Spaceship(55, 40, 90, 100, 300, 5, self, color='yellow')
        self.add_dependencies('yellow_spaceship', yellow_spaceship)

        self.background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (self.width, self.height))

        self.bullet_speed = 8
        self.fps = 60
        self.winner_text = ""

        self.health_font = pygame.font.SysFont('comicsans', 40)
        self.countdown_font = pygame.font.SysFont('comicsans', 60)
        self.winner_font = pygame.font.SysFont('comicsans', 100)

    def draw_window(self):
        self.win.blit(self.background, (0, 0))
        pygame.draw.rect(self.win, BLACK, self.border)

        red_health_text = self.health_font.render(f'Health: {self.dependencies["red_spaceship"].health}', True, WHITE)
        yellow_health_text = self.health_font.render(f'Health: {self.dependencies["yellow_spaceship"].health}', True, WHITE)
        self.win.blit(red_health_text, (self.width - red_health_text.get_width() - 10, 10))
        self.win.blit(yellow_health_text, (10, 10))

        for key, objects in self.dependencies.items():
            if key == 'red_spaceship':
                red_spaceship = objects
                self.win.blit(red_spaceship.spaceship, (red_spaceship.x, red_spaceship.y))
            if key == 'yellow_spaceship':
                yellow_spaceship = objects
                self.win.blit(yellow_spaceship.spaceship, (yellow_spaceship.x, yellow_spaceship.y))

        for bullet in self.dependencies['red_spaceship'].bullet_list:
            pygame.draw.rect(self.win, RED, bullet)

        for bullet in self.dependencies['yellow_spaceship'].bullet_list:
            pygame.draw.rect(self.win, YELLOW, bullet)

        pygame.display.update()

    def draw_winner(self):
        countdown = True
        countdown_time = 5

        while countdown:
            self.draw_window()
            draw_text = self.winner_font.render(self.winner_text, True, WHITE)
            self.win.blit(draw_text, (self.width // 2 - draw_text.get_width() // 2, self.height // 2 - draw_text.get_height() // 2))

            countdown_text = self.countdown_font.render(str(countdown_time), True, WHITE)
            self.win.blit(countdown_text, (self.width // 2 - countdown_text.get_width() // 2, self.height // 2 + draw_text.get_height() // 2))

            pygame.display.update()

            countdown_time -= 1
            if countdown_time == 0:
                countdown = False
            pygame.time.delay(1000)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(self.fps)

            if self.dependencies['red_spaceship'].health <= 0:
                self.winner_text = 'Yellow Wins!'
            if self.dependencies['yellow_spaceship'].health <= 0:
                self.winner_text = 'Red Wins!'

            if self.winner_text:
                self.draw_winner()
                self.winner_text = ''
                self.dependencies['red_spaceship'].reset_all()
                self.dependencies['yellow_spaceship'].reset_all()

                return self.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == RED_HIT:
                    self.dependencies['red_spaceship'].health -= 1
                    # BULLET_HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    self.dependencies['yellow_spaceship'].health -= 1
                    # BULLET_HIT_SOUND.play()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(self.dependencies['yellow_spaceship'].bullet_list) < self.dependencies['yellow_spaceship'].bullet_limit:
                        bullet = pygame.Rect(self.dependencies['yellow_spaceship'].yellow.x + self.dependencies['yellow_spaceship'].yellow.width, self.dependencies['yellow_spaceship'].yellow.y + self.dependencies['yellow_spaceship'].yellow.height // 2 - 2, 10, 5)
                        self.dependencies['yellow_spaceship'].bullet_list.append(bullet)
                        # BULLET_FIRED_SOUND.play()

                    if event.key == pygame.K_RCTRL and len(self.dependencies['red_spaceship'].bullet_list) < self.dependencies['red_spaceship'].bullet_limit:
                        bullet = pygame.Rect(self.dependencies['red_spaceship'].red.x, self.dependencies['red_spaceship'].red.y + self.dependencies['red_spaceship'].red.height // 2 - 2, 10, 5)
                        self.dependencies['red_spaceship'].bullet_list.append(bullet)
                        # BULLET_FIRED_SOUND.play()

            keys_pressed = pygame.key.get_pressed()

            self.dependencies['red_spaceship'].handle_movement(keys_pressed)
            self.dependencies['yellow_spaceship'].handle_movement(keys_pressed)
            self.handle_bullets()

            self.draw_window()

    def add_dependencies(self, dependency_name: str, dependency: object):
        self.dependencies.update({dependency_name: dependency})

    def handle_bullets(self):
        for bullet in self.dependencies['yellow_spaceship'].bullet_list:
            bullet.x += self.bullet_speed
            if bullet.x > self.width:
                self.dependencies['yellow_spaceship'].bullet_list.remove(bullet)

            if self.dependencies['red_spaceship'].red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                self.dependencies['yellow_spaceship'].bullet_list.remove(bullet)

        for bullet in self.dependencies['red_spaceship'].bullet_list:
            bullet.x -= self.bullet_speed
            if bullet.x < 0:
                self.dependencies['red_spaceship'].bullet_list.remove(bullet)

            if self.dependencies['yellow_spaceship'].yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                self.dependencies['red_spaceship'].bullet_list.remove(bullet)


new_window = Window(900, 500, 'Naves são demais')
new_window.run()
