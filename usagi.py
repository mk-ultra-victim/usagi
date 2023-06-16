class Usagi_Game:
    def __init__(self):
        self.levels = []
        self.players = []

    def update(self):
        pass

    def main_menu(self):
        pass

    def play_level(self, number):
        pass

class Level:
    def __init__(self):
        self.background = None
        self.enemies = []
        self.friendly = []

    def update(self):
        pass

    
class Actor:
    def __init__(self):
        pass

    def update(self):
        pass

    def update_action(self, new_action):
        pass

    def attack(self, target):
        pass

    def interact(self, target):
        pass

    def take_damage(self, damage):
        pass

    def die(self):
        pass

    
class Player(Actor):
    def __init__(self, controls):
        super().__init__()
        self.controls = controls
        

    def update(self):
        pass
        

class 
