import pygame
import random
import math

from scipy import rand
import twitter_api as twit
import poisson_disc

WIDTH, HEIGHT = 1024, 768
FONT_SIZE = 20
pygame.font.init()
FONT = pygame.font.Font("Unique.ttf", FONT_SIZE)
COLLISION_RATIO = 0.6

### Pygame stuff
pygame.init()
pygame.display.set_caption("Twitter game")
time = pygame.time.Clock()

### Surface Definitions
MAIN_SURFACE = pygame.display.set_mode((WIDTH,HEIGHT))
SCORE_SURFACE = pygame.Surface((100,30),pygame.SRCALPHA)
SCORE_SURFACE.fill((50,50,50,80))

### Auxiliary Functions
def render_text(message, pos, colour=(255,255,255)):
    MAIN_SURFACE.blit(FONT.render(message, 1, colour), pos)

def distance(p1, p2):
    diff_x = math.fabs(p1[0] - p2[0])
    diff_y = math.fabs(p1[1] - p2[1])
    return ((diff_x**2) + (diff_y**2))**(0.5)

### Handles the rendering of all objects in the scene
class RenderManager:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def render(self):
        for obj in self.objects:
            obj.render()
    
    def rockets(self):
        for obj in self.objects:
            obj.trigger_rockets()

### Stores data about where in the scene we are looking        
class Camera:
    def __init__(self, zoom):
        self.x = 0
        self.y = 0
        self.width = WIDTH
        self.height = HEIGHT
        self.zoom = zoom

    def centre(self, player):
        x, y = player.x, player.y
        self.x = (WIDTH/2) - x*self.zoom
        self.y = (HEIGHT/2) - y*self.zoom

class VisualObject:
    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def render(self):
        pass

    def trigger_rockets(self):
        pass

class Background(VisualObject):
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.colour = (230,240,240)

    def render(self):
        ### A Background is a set of horizontal and prependicular lines
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0,2001,25):
            pygame.draw.line(self.surface,  self.colour, (x, i*zoom + y), (2001*zoom + x, i*zoom + y), 3)
            pygame.draw.line(self.surface, self.colour, (i*zoom + x, y), (i*zoom + x, 2001*zoom + y), 3)

class HUD(VisualObject):
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        
    def render(self):
        w,h = FONT.size("Score: "+str(SCORE//100)+" ")
        MAIN_SURFACE.blit(pygame.transform.scale(SCORE_SURFACE, (w, h)), (8,HEIGHT-30))
        render_text("Score: " + str(SCORE//100),(10,HEIGHT-30))

class Player(VisualObject):    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(100,400)
        self.y = random.randint(100,400)
        self.size = 20
        self.speed = 4
        self.colour = (200, 50, 30)
        self.outlinecolour = (255, 150, 140)
        self.collided = False
        self.health = 100

    def collisionDetection(self, blobs):
        for blob in blobs:
            if(distance((blob.x, blob.y), (self.x,self.y)) <= blob.size * COLLISION_RATIO):
                self.collided = True

    def move(self):
        dX, dY = pygame.mouse.get_pos()
        rotation = math.atan2(dY - float(HEIGHT)/2, dX - float(WIDTH)/2)
        rotation *= 180/math.pi
        normalized = (90 - math.fabs(rotation))/90
        vx = self.speed*normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX % WIDTH
        self.y = tmpY % HEIGHT

    def render(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        glow = ((math.sin(SCORE / 100) ** 2) * 255) // 1
        pygame.draw.circle(self.surface, (255, glow, glow), center, int((self.size/2 + 3)*zoom))
        pygame.draw.circle(self.surface, self.colour, center, int(self.size/2*zoom))

class Blob(VisualObject):
    def __init__(self, surface, camera, position, name):
        super().__init__(surface, camera)
        self.x = position[0] * WIDTH
        self.y = position[1] * HEIGHT
        self.size = len(name) * 4
        self.name = name
        self.colour = (0, 255, 0)

    def trigger_rockets(self):
        dirx = random.randint(-WIDTH/2, WIDTH/2)
        diry = random.randint(-HEIGHT/2, HEIGHT/2)
        angle = (diry - self.y) / (dirx - self.x)
        rocket = Rocket (MAIN_SURFACE, cam, self.x, self.y, angle)
        rockets.addrocket(rocket)

    def render(self):
        zoom = self.camera.zoom
        x,y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        pygame.draw.circle(self.surface, self.colour, center, int(self.size*zoom))
        render_text(self.name, (int(self.x*zoom + x - self.size * 1.5), int(self.y*zoom + y - self.size / 2)), (125, 125, 125))
        
class BlobManager(VisualObject):
    ### Add Twitter code here
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.blob_list = []
        self.tweets = twit.get_trends()
        print(self.tweets)
        self.poissons = self.make_poissondisc()
        randompositions = random.sample(range(0, len(self.poissons)-1), len(self.tweets))
        for i in range(len(self.tweets)): self.blob_list.append(Blob(self.surface, self.camera, self.poissons[randompositions[i]], str(self.tweets[i][0])))

    def make_poissondisc(self):
        return poisson_disc.Bridson_sampling(radius=0.1)

    def render(self):
        for blob in self.blob_list:
            blob.render()

class Rocket(VisualObject):
    def __init__(self, surface, camera, x, y, angle, speed):
        super().__init__(surface, camera)
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.size = 3
        self.colour = (0, 255, 0)
    
    def render(self):
        zoom = self.camera.zoom
        x,y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        pygame.draw.circle(self.surface, self.colour, center, int(self.size*zoom))

    def move(self):
        theta = self.angle
        self.x = self.x + math.cos(theta) * self.speed * time.get_rawtime
        self.y = self.y + math.sin(theta) * self.speed * time.get_rawtime


class RocketManager(VisualObject):
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.rocket_list = []
        
    def addrocket(self, rocket):
        self.rocket_list.append(rocket)

    def render(self):
        for rocket in self.rocket_list:
            rocket.move()
            rocket.render()

### Initialize essential entities
cam = Camera(1)

background = Background(MAIN_SURFACE, cam)
blobs = BlobManager(MAIN_SURFACE, cam)
player = Player(MAIN_SURFACE, cam)
hud = HUD(MAIN_SURFACE, cam)
rockets = RocketManager(MAIN_SURFACE, cam)

RenderManager = RenderManager()
RenderManager.add(background)
RenderManager.add(blobs)
RenderManager.add(player)
RenderManager.add(hud)
RenderManager.add(rockets)

### Game main loop
SCORE = 0
while(True):
    time.tick(70)
    if(SCORE//100 == 24):
        print("Hello")
        RenderManager.rockets()
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        if(e.type == pygame.QUIT):
            pygame.quit()
            quit()
    SCORE += int(time.get_time())
    player.move()
    player.collisionDetection(blobs.blob_list)
    MAIN_SURFACE.fill((242,251,255))
    RenderManager.render()
    pygame.display.flip()