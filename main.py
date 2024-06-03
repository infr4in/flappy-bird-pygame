import pygame, sys, time, random
from settings import *
from sprites import Background, Floor, Bird, BottomPipe, TopPipe


class Game:
    def __init__(self):

        # setup game
        pygame.init()
        pygame.display.set_icon(pygame.image.load("assets/icon/favicon.ico"))
        pygame.display.set_caption("Flappy Bird")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load("./assets/environment/background-day.png").get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        Background(self.all_sprites, self.scale_factor)
        Floor([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.bird = Bird(self.all_sprites, self.scale_factor * 1.2)
        self.pipe_heights = [WINDOW_HEIGHT * 0.3, WINDOW_HEIGHT * 0.5, WINDOW_HEIGHT * 0.7]

        # timer
        self.pipe_spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_spawn_timer, 1400)

        # text
        self.font = pygame.font.Font("./assets/font/04B_19.TTF", 30)
        self.score = 0
        self.high_score = 0
        self.can_score = True  # need to score only 1 time

        # menu
        self.menu_image = pygame.image.load("./assets/ui/menu.png").convert_alpha()
        self.menu_rect = self.menu_image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # sounds
        # self.music = pygame.mixer.Sound("./assets/sounds/secret.mp3")
        # self.music.set_volume(0.2)
        # self.music.play(loops=-1)

        self.collision_sound = pygame.mixer.Sound("./assets/sounds/hit.wav")
        self.collision_sound.set_volume(0.2)

        self.score_sound = pygame.mixer.Sound("./assets/sounds/point.wav")
        self.score_sound.set_volume(0.2)

    def check_collisions(self):
        # if objects collide or a bird flies off the screen
        if (pygame.sprite.spritecollide(self.bird, self.collision_sprites, False, pygame.sprite.collide_mask)
                or self.bird.rect.top <= -100):

            # delete all pipes
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == "pipe":
                    sprite.kill()

            self.collision_sound.play()
            self.active = False
            self.can_score = True
            self.bird.kill()

    def display_score(self):
        if not self.active:
            high_score_surf = self.font.render(f"High Score: {str(self.high_score)}", True, "white")
            high_score_rect = high_score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 7))
            self.screen.blit(high_score_surf, high_score_rect)

            score_surf = self.font.render(f"Score: {str(self.score)}", True, "white")
        else:
            score_surf = self.font.render(str(self.score), True, "white")

        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH/2, WINDOW_HEIGHT/10))
        self.screen.blit(score_surf, score_rect)

    def update_score(self):
        if self.collision_sprites:
            for sprite in self.collision_sprites:
                if (sprite.sprite_type == "pipe"
                        and self.can_score
                        and self.bird.rect.centerx - 5 < sprite.rect.centerx < self.bird.rect.centerx + 5):
                    self.score_sound.play()
                    self.score += 1
                    self.can_score = False
                if sprite.rect.centerx < 0:
                    self.can_score = True

        if self.score > self.high_score:
            self.high_score = self.score

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event listener
            for event in pygame.event.get():

                # quits the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # jumps if the game is running, or restarts the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.active:
                        self.bird.jump()
                    else:
                        self.bird = Bird(self.all_sprites, self.scale_factor * 1.2)
                        self.active = True
                        self.score = 0

                # spawns pipes
                if event.type == self.pipe_spawn_timer and self.active:
                    random_pipe_pos = random.choice(self.pipe_heights)
                    BottomPipe(random_pipe_pos, [self.all_sprites, self.collision_sprites], self.scale_factor * 1.2)
                    TopPipe(random_pipe_pos, [self.all_sprites, self.collision_sprites], self.scale_factor * 1.2)

            # game logics
            self.screen.fill("black")
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.update_score()
            self.display_score()

            if self.active:
                self.check_collisions()
            else:
                self.screen.blit(self.menu_image, self.menu_rect)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
