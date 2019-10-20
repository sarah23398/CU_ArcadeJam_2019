import pygame
import os
pygame.init()
vec = pygame.math.Vector2

playerHeight = 150
playerWidth = 150
x_change = 20
y_change = 20
PLAYER_ACC = 15
PLAYER_FRICTION = -1
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

class Player(pygame.sprite.Sprite):
    # Represents the controllable Player
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.load_images()
        # --- Class Attributes ---
        # Player position
        self.x = 318
        self.y = 515+114-playerWidth
        self.game = game

        self.image = self.standRight
        self.rect = self.image.get_rect()
        self.rect.center = (318, 515+114-playerWidth)

        self.pos = vec(318, 515+114-playerWidth)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.isJump = False
        self.standR = False
        self.left = False
        self.right = False
        self.still = False
        self.walkCount = 0
        self.jumpCount = 10



    def load_images(self):
        self.walkRight = [
            pygame.image.load(os.path.join(os.path.dirname(__file__),'resources/images/sprites/r1.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/r2.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/r3.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/r4.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/r5.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/r6.png'))]
        self.walkRight = [pygame.transform.scale(self.walkRight[0], (playerHeight, playerWidth)),
                     pygame.transform.scale(self.walkRight[1], (playerHeight, playerWidth)),
                     pygame.transform.scale(self.walkRight[2], (playerHeight, playerWidth)),
                     pygame.transform.scale(self.walkRight[3], (playerHeight, playerWidth)),
                     pygame.transform.scale(self.walkRight[4], (playerHeight, playerWidth)),
                     pygame.transform.scale(self.walkRight[5], (playerHeight, playerWidth))]

        self.walkLeft = [
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/l1.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/l2.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/l3.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/l4.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/l5.png')),
            pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/l6.png'))]

        self.walkLeft = [pygame.transform.scale(self.walkLeft[0], (playerHeight, playerWidth)),
                    pygame.transform.scale(self.walkLeft[1], (playerHeight, playerWidth)),
                    pygame.transform.scale(self.walkLeft[2], (playerHeight, playerWidth)),
                    pygame.transform.scale(self.walkLeft[3], (playerHeight, playerWidth)),
                    pygame.transform.scale(self.walkLeft[4], (playerHeight, playerWidth)),
                    pygame.transform.scale(self.walkLeft[5], (playerHeight, playerWidth))]

        self.standRight = pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/standr.png'))
        self.standRight = pygame.transform.scale(self.standRight, (playerHeight, playerWidth))

        self.standLeft = pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/standl.png'))
        self.standLeft = pygame.transform.scale(self.standLeft, (playerHeight, playerWidth))

        self.jumpRight = pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/jumpr.png'))
        self.jumpRight = pygame.transform.scale(self.jumpRight, (playerHeight, playerWidth))

        self.jumpLeft = pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/jumpl.png'))
        self.jumpLeft = pygame.transform.scale(self.jumpLeft, (playerHeight, playerWidth))

        self.standStill = pygame.image.load(os.path.join(os.path.dirname(__file__), 'resources/images/sprites/still.png'))
        self.standStill = pygame.transform.scale(self.standStill, (playerHeight, playerWidth))

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if not self.still:
                self.acc.x = PLAYER_ACC
                self.right = True
                self.left = False
                self.standR = True
        if keys[pygame.K_a]:
            if not self.still:
                self.acc.x = -PLAYER_ACC
                self.left = True
                self.right = False
                self.standR = False

            # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > 1280:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = 1280

        self.rect.midbottom = self.pos

    def jump(self):
        if not self.still:
            self.rect.y += 1
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.y -= 1
            if hits:
                self.vel.y = -PLAYER_JUMP

    def while_jump(self):
        if self.jumpCount >= -10:
            neg = 2
            if self.jumpCount < 0:
                neg = -2
            self.pos.y -= (self.jumpCount ** 2) * 0.5 * neg
            self.jumpCount -= 1
            self.still = False
        else:
            self.isJump = False
            self.jumpCount = 10

    def sneak(self):
        self.still = True;

    def fall(self):
        self.y += self.y_change

    def default(self):
        self.left = False
        self.right = False
        self.still = False
        self.walkCount = 0

    def draw(self, screen):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0
        if self.still:
            screen.blit(self.standStill, (self.pos.x, self.pos.y))
        elif self.isJump:
            if self.standR:
                screen.blit(self.jumpRight, (self.pos.x, self.pos.y))
            else:
                screen.blit(self.jumpLeft, (self.pos.x, self.pos.y))
        elif self.left:
            screen.blit(self.walkLeft[self.walkCount//3], (self.pos.x, self.pos.y))
            self.walkCount += 1
        elif self.right:
            screen.blit(self.walkRight[self.walkCount//3], (self.pos.x, self.pos.y))
            self.walkCount += 1
        elif self.standR:
            screen.blit(self.standRight, (self.pos.x, self.pos.y))
        else:
            screen.blit(self.standLeft, (self.pos.x, self.pos.y))