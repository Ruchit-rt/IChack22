from cmath import sqrt
import math
import pygame;

class Player(ObjectRenderer):
    """Used to represent the concept of a player.
    """
    def __init__(self, surface, camera, collided = False, name = ""):
        super().__init__(surface, camera)
        self.x = 0
        self.y = 0
        self.collided = collided 
        self.size = 15
        self.speed = 4
        if name: self.name = name
        else: self.name = "Anonymous"
        self.pieces = []

    def collisionDetection(self, blobs):
        for blob in blobs:
            d = sqrt((blob.x - self.x)**2 + (blob.y - self.y)**2)
            if(d <= blob.radius/2):
                self.collided = True


    def move(self):
        """Updates players current position depending on player's mouse relative position.
        """
        
        dX, dY = pygame.mouse.get_pos()
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        rotation = math.atan2(dY - float(HEIGHT)/2, dX - float(WIDTH)/2)
        # Convert radians to degrees [-180, 180]
        rotation *= 180/math.pi
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (90 - math.fabs(rotation))/90
        vx = self.speed*normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX
        self.y = tmpY
