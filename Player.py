class Player:
    # Represents the controllable Player
    def __init__(self, x_change, y_change):
        # --- Class Attributes ---
        # Player position
        self.x = 318
        self.y = 720
        self.x_change = x_change
        self.y_change = y_change

    def move_right(self):
        self.x += self.x_change

    def move_left(self):
        self.x -= self.x_change

    def move_up(self):
        self.y -= self.y_change

    def fall(self):
        self.y += self.y_change

    #def sneak(self):

