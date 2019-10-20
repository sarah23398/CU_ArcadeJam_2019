import pygame
import os
from Player import *
from pygame.locals import *
from Platform import Platform

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT = (0xF2, 0xF0, 0xAF)

windowHeight = 114
windowWidth = 114

class Game:
    # Represents a full Game.
    def __init__(self):

        # --- Class Attributes ---
        pygame.init()
        self.windows = [None] * 9
        self.window_platforms = [None] * 9
        self.platforms = [None] * 9
        self.score = 0
        self.size = (1280, 720)
        self.caption = "Diamond Heist"

        # --- Set up Game initials ---
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)

        # Initialize background
        self.background_image = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                               "resources/images/background1.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, (1280, 720))

        # Initialize windows
        self.windows[0] = Rect(318, 685, 114, 114)
        self.windows[1] = Rect(848, 685, 114, 114)
        self.windows[2] = Rect(585, 515, 114, 114)
        self.windows[3] = Rect(318, 345, 114, 114)
        self.windows[4] = Rect(848, 345, 114, 114)
        self.windows[5] = Rect(585, 175, 114, 114)
        self.windows[6] = Rect(318, 5, 114, 114)
        self.windows[7] = Rect(848, 5, 114, 114)
        self.windows[8] = Rect (585, -165, 114, 114)

        # Initialize window platforms
        self.window_platforms[0] = Rect(585, 685, 114, 114)
        self.window_platforms[1] = Rect(318, 515, 114, 114)
        self.window_platforms[2] = Rect(848, 515, 114, 114)
        self.window_platforms[3] = Rect(585, 345, 114, 114)
        self.window_platforms[4] = Rect(318, 175, 114, 114)
        self.window_platforms[5] = Rect(848, 175, 114, 114)
        self.window_platforms[6] = Rect(585, 5, 114, 114)
        self.window_platforms[7] = Rect(318, -165, 114, 114)
        self.window_platforms[8] = Rect(848, -165, 114, 114)

        # Initialize lights
        self.orig_light1 = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                          "resources/images/light.png")).convert_alpha()
        self.orig_light1 = pygame.transform.scale(self.orig_light1, (1400, 900))
        self.orig_light1 = pygame.transform.flip(self.orig_light1, False, True)
        self.orig_light1.set_alpha(150)
        self.orig_light2 = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                          "resources/images/light.png")).convert_alpha()
        self.orig_light2 = pygame.transform.scale(self.orig_light2, (1400, 900))
        self.orig_light2 = pygame.transform.flip(self.orig_light2, True, True)
        self.orig_light2.set_alpha(128)
        self.light_rotation = 0
        self.light_rotation_speed = 360
        self.clockwise = True

        # --- Prepare to start Game ---
        self.done = False

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Create Player controller
        self.x_change = 20
        self.y_change = 20
        self.player = Player(self)

        # Display score
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.text = self.font.render("Score: " + str(self.score), True, BLACK)

        # Create platforms
        for i in range(9):
            self.platforms[i] = Platform(self.window_platforms[i].left - 28, self.window_platforms[i].top + 114)

        # --- Draw Game ---
        self.draw(self.orig_light1, self.orig_light2)

    def draw(self, light1, light2):
        self.screen.blit(self.background_image, [0, 0])

        for i in self.window_platforms:
            pygame.draw.rect(self.screen, WHITE, i)

        for i in self.windows:
            pygame.draw.rect(self.screen, WHITE, i)

        self.screen.blit(self.text, [1100, 650])

        for i in self.platforms:
            self.screen.blit(i.image, [i.rect.x, i.rect.y])

        self.screen.blit(light1, [-50, -200])
        self.screen.blit(light2, [-200, -200])
        self.player.draw(self.screen)

        pygame.display.update()

    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        for plat in self.platforms:
            self.all_sprites.add(plat)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.move_light()
            self.clock.tick(60)
            self.events()
            self.update()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_screen_up()
                    self.player.jump()

    # def calculate_score(self):

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def move_screen_up(self):
        # Move windows up
        for i in self.windows:
            i.top -= self.y_change
            if i.top < -142:
                i.top = 720

        for i in self.window_platforms:
            i.top -= self.y_change
            if i.top < -142:
                i.top = 720

        for i in self.platforms:
            i.rect.y -= self.y_change
            if i.rect.y < -28:
                i.rect.y = 834

    def move_light(self):
        rot_light1 = pygame.transform.rotate(self.orig_light1, self.light_rotation)
        rot_light2 = pygame.transform.rotate(self.orig_light2, self.light_rotation)
        if self.clockwise:
            if (self.light_rotation >= 0) and (self.light_rotation < 45):
                self.light_rotation += 1
            else:
                self.light_rotation -= 1
                self.clockwise = False
        else:
            if (self.light_rotation > 0) and (self.light_rotation < 45):
                self.light_rotation -= 1
            else:
                self.light_rotation += 1
                self.clockwise = True
        self.draw(rot_light1, rot_light2)

    def quit(self):
        # Close the window and quit.
        pygame.quit()

g = Game()
g.show_start_screen()
while not g.done:
    g.new()
    g.show_go_screen()

g.quit()