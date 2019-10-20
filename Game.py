import pygame
import os
from Player import *
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT = (0xF2, 0xF0, 0xAF)

PLATFORM_LIST = [(0, 720 - 300, 1280, 40)]

windowHeight = 114
windowWidth = 114

class Game:
    # Represents a full Game.
    def __init__(self):
        # --- Class Attributes ---
        pygame.init()
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
        self.window1 = Rect(318, 515, windowHeight, windowWidth)
        self.window2 = Rect(848, 515, windowHeight, windowWidth)
        # Initialize light surface
        self.orig_light = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                               "resources/images/light2.png")).convert_alpha()
        self.orig_light = pygame.transform.scale(self.orig_light, (2560, 1440))
        self.orig_light.set_alpha(128)
        self.light_rotation = 0
        self.light_rotation_speed = 360
        self.clockwise = False

        # --- Prepare to start Game ---
        self.done = False
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        # Create Player controller
        self.player = Player(self)
        # Display score
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.text = self.font.render("Score: " + str(self.score), True, BLACK)

        # --- Draw Game ---
        self.draw(self.orig_light)

    def draw(self, light):
        self.screen.blit(self.background_image, [0, 0])
        pygame.draw.rect(self.screen, WHITE, self.window1)
        pygame.draw.rect(self.screen, WHITE, self.window2)
        self.screen.blit(light, [-1280, -720])
        self.screen.blit(self.text, [1100, 650])
        self.player.draw(self.screen)
        pygame.display.update()

    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw(self.orig_light)

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
        self.window1.top -= 20
        self.window2.top -= 20
        # self.draw()

    def move_screen_down(self):
        # Move windows down
        self.window1.top += self.player.d
        self.window2.top += self.player.y_change
        pygame.draw.rect(self.screen, WHITE, self.window1)
        pygame.draw.rect(self.screen, WHITE, self.window2)

    def move_light(self):
        rot_light = pygame.transform.rotate(self.orig_light, self.light_rotation)
        print (rot_light.get_rect().center)
        if not self.clockwise:
            if (self.light_rotation >= 0) and (self.light_rotation < 45):
                self.light_rotation += 1
            else:
                self.light_rotation -= 1
                self.clockwise = True
        else:
            if (self.light_rotation > 0) and (self.light_rotation < 45):
                self.light_rotation -= 1
            else:
                self.light_rotation += 1
                self.clockwise = False
        self.draw(rot_light)

    def quit(self):
        # Close the window and quit.
        pygame.quit()

g = Game()
g.show_start_screen()
while not g.done:
    g.new()
    g.show_go_screen()

g.quit()