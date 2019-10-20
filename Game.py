import pygame
import os
from Player import Player
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT = (0xF2, 0xF0, 0xAF)


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
                                                               "Assets/background1.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, (1280, 720))
        # Initialize windows
        self.window1 = Rect(318, 515, 114, 114)
        self.window2 = Rect(848, 515, 114, 114)
        # Initialize light surface
        self.orig_light = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                               "Assets/light2.png")).convert_alpha()
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
        self.x_change = 20
        self.y_change = 20
        self.player = Player(self.x_change, self.y_change)
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
        pygame.display.update()

    def start(self):
        # --- Start Game ---
        # Loop until the user clicks the close button.

        # -------- Main Program Loop -----------
        while not self.done:
            # --- Main event loop
            self.move_light()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                # --- Game logic should go here
                # User pressed down on a key
                elif event.type == pygame.KEYDOWN:
                    # Figure out if it was an arrow key. If so
                    # adjust coord.
                    if event.key == pygame.K_a:
                        self.player.move_left()
                    elif event.key == pygame.K_d:
                        self.player.move_right()
                    elif event.key == pygame.K_w:
                        self.player.move_up()
                        self.move_screen_up()

                    elif event.key == pygame.K_7:
                        self.player.sneak()

            # --- Drawing code should go here
            # Move light

            # Update score
            # score = self.calculate_score()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self.clock.tick(10)

    # def calculate_score(self):

    def move_screen_up(self):
        # Move windows up
        self.window1.top -= self.y_change
        self.window2.top -= self.y_change
        self.draw()

    def move_screen_down(self):
        # Move windows down
        self.window1.top += self.player.y_change
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

