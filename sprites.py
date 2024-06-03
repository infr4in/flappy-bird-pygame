import pygame
from settings import *


class Background(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        bg_image = pygame.image.load("./assets/environment/background-day.png").convert()
        self.image = pygame.transform.scale(bg_image, pygame.math.Vector2(bg_image.get_size()) * scale_factor)

        # position
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)


class Floor(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = "floor"

        # image
        floor_image = pygame.image.load("./assets/environment/floor.png").convert_alpha()
        self.image = pygame.transform.scale(floor_image, pygame.math.Vector2(floor_image.get_size()) * scale_factor)

        # position
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 250 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)


class Bird(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH/20, WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 600
        self.direction = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # sound
        self.jump_sound = pygame.mixer.Sound("./assets/sounds/wing.wav")
        self.jump_sound.set_volume(0.2)

    def import_frames(self, scale_factor):
        self.frames = []

        # get all frames in list
        for i in range(3):
            bird_frame = pygame.image.load(f"./assets/birds/bluebird{i}.png").convert_alpha()
            scaled_frame = pygame.transform.scale(bird_frame, pygame.math.Vector2(bird_frame.get_size()) * scale_factor)
            self.frames.append(scaled_frame)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_bird = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_bird
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = "pipe"

        # image
        pipe_image = pygame.image.load("./assets/pipes/pipe-green.png")
        self.image = pygame.transform.scale(pipe_image, pygame.math.Vector2(pipe_image.get_size()) * scale_factor)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 250 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()


class BottomPipe(Pipe):
    def __init__(self, height, groups, scale_factor):
        super().__init__(groups, scale_factor)

        # position
        self.rect = self.image.get_rect(midtop=(WINDOW_WIDTH + 100, height))
        self.pos = pygame.math.Vector2(self.rect.topleft)


class TopPipe(Pipe):
    def __init__(self, height, groups, scale_factor):
        super().__init__(groups, scale_factor)

        # image
        self.image = pygame.transform.flip(self.image, False, True)

        # position
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH + 100, height - 300))
        self.pos = pygame.math.Vector2(self.rect.topleft)
