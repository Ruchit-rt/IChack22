from cmath import sqrt
import random

class Blob(ObjectRenderer):
    """Used to represent the concept of a player.
    """
    def __init__(self, surface, camera, name = ""):
        super().__init__(surface, camera)
        self.x = random.randint(-WIDTH/2 + 1, WIDTH/2 - 1)
        self.y = random.randint(-HEIGHT/2 + 1, HEIGHT/2 - 1)
        self.size = random.randint(10, 20)     ## this needs to come from the twitter data 
        if name: self.name = name
        else: self.name = "Anonymous"
