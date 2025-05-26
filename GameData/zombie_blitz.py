import pygame

#vector class used for giving game objects a velocity/position
class Vector: 
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def add(self, other):
        self.x += other.x
        self.y += other.y

#player class 
class Player:
    def __init__(self, position, weapon, sprite):
        self.speed = 0
        self.position = position
        self.weapon = weapon
        self.inventory = []
        self.sprite = sprite

    def move():
        None
        
    def shoot():
        None

#weapons used by the player
class Weapon:
    def __init__(self, name, damage, attack_pattern, sprite, cost):
        self.name = name
        self.damage = damage
        self.attack_pattern = attack_pattern
        self.sprite = sprite
        self.cost = cost

#interactable button to allow the user to interact with the gmae 
class Button: 
    def __init__(self, color, position, size, text, on_click): #on_click determines what happens when the button is clicked
        self.color = color
        self.position = position #position is the bottom left x and y coordinate
        self.size = size #size is the dimenstions of the triangle 

        self.font = pygame.font.SysFont('Corbel',30)
        self.text = self.font.render(text, True, color)
        
        self.on_click = on_click
        
    #loads the button onto the frame
    def load(self):
        pygame.draw.rect(screen, self.color, [self.position.x, self.position.y, self.size.x, self.size.y], 2, 3)
        
        #load text inside the button
        screen.blit(self.text , ((self.position.x + 10,
                                self.position.y + (self.size.y / 4))))

class Images: 
    def __init__(self, dest, position, size):
        self.image = pygame.image.load(dest).convert_alpha() #loads image from the destination
        self.scale = (size) #size given as a vector is the scale of the image 

        self.image = pygame.transform.scale(self.image, self.scale)

        self.position = position #the coordinates it will spawn at (given as a vector)
    
    def load(self):
        screen.blit(self.image, self.position)


#handles switching between different scenes (main menu, settings etc)
class SceneHandler:
    def __init__(self):
        self.current = None
        self.previous = None #used to go back to the previous scene 

    #loads the current scene
    def load(self):
        self.current.load()

    #swaps out the current scene with a 'new' scene 
    def update(self, new):
        self.previous = self.current
        self.current = new

class Scene:
    def __init__(self, background):
        self.background = pygame.image.load(background).convert()
        self.default_bg_size = (500,500) #the size of the canvas
        self.background = pygame.transform.scale(self.background, self.default_bg_size)

        self.assets = [] #holds the buttons that will appear on the scene

    #load in the assets of that scene 
    def load(self):
        screen.blit(self.background, (0,0))

        for asset in self.assets:
            asset.load()
        
        pygame.display.flip() #update scene
    
    def update(self):
        None

#called when the start button is pressed
def start_game():
    scene_handler.update(pre_game) #swaps the current scene out for the game scene 
    scene_handler.load()

def open_settings(): #opens settings menu
    scene_handler.update(settings) 
    scene_handler.load()

def open_help(): #opens help menu
    scene_handler.update(help)  
    scene_handler.load()

def open_credits(): #opens credits menu
    scene_handler.update(credits) 
    scene_handler.load()

def go_back(): #goes back to the previous scene
    scene_handler.update(scene_handler.previous)
    scene_handler.load()


#initialise pygame
pygame.init()

#set up game window
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Zombie Blitz")

#start clock
clock = pygame.time.Clock()

#set the games icon
pygame_icon = pygame.image.load('zb logo.png')
pygame.display.set_icon(pygame_icon)

#instantiate scene handler
scene_handler = SceneHandler()

#generate scenes
game = Scene("MenuAssets/game bg.jpg")
main_menu = Scene("MenuAssets/main menu bg.jpg")
pre_game = Scene("MenuAssets/pre game bg.jpg")
settings = Scene("MenuAssets/settings bg.jpg")
credits = Scene("MenuAssets/default bg.jpg")
help = Scene("MenuAssets/default bg.jpg")

#generate player
player = Player(None, None, "Sprites/player.png")

#instantiate scene handler
scene_handler.update(main_menu)

#generate buttons
main_menu.assets = [
    Button((0,0,0), Vector(260,180), Vector(200,50), "START", start_game), #start button
    Button((0,0,0), Vector(260,240), Vector(200,50), "SETTINGS", open_settings), #settings button
    Button((0,0,0), Vector(260,300), Vector(200,50), "HELP", open_help), #help button
    Button((0,0,0), Vector(260,360), Vector(200,50), "CREDITS", open_credits), #credits button
    Button((0,0,0), Vector(260,420), Vector(200,50), "QUIT", None), #quit button
]

credits.assets = [
    Button((255,255,255), Vector(0,50), Vector(10,10), "programmed by Nathan Uphill", None),
    Button((255,255,255), Vector(0,150), Vector(10,10), "sprites drawn by Nathan Uphill", None),
    Button((255,255,255), Vector(0,250), Vector(10,10), "@nathanuph on github", None),
    Button((255,255,255), Vector(0,350), Vector(10,10), "Backgrounds generated by Google Gemini", None),

    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back) #back button
]

settings.assets = [
    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back) #back button
]

help.assets = [
    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back) #back button
]

pre_game.assets = [
    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back), #back button
    Images(player.sprite, (0,0), (250,250))
]


scene_handler.load()

#game loop 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            #stores the location of the mouse position in a tuple
            mouse = pygame.mouse.get_pos()

            #check if the mouse is clicked on a button

            #validate there is any asset to click
            if len(scene_handler.current.assets) != 0:
                for asset in scene_handler.current.assets:
                    #check that the asset is a button
                    if isinstance(asset, Button):
                        #check if mouse click occurs within bounds of the button
                        if ((asset.position.x <= mouse[0] <= (asset.position.x + asset.size.x)) 
                            and (asset.position.y <= mouse[1] <= (asset.position.y + asset.size.y))):
                            
                            asset.on_click()
    
    dt = clock.tick(60) / 1000 #caps frame rate at 60fps

pygame.quit()

'''
All zombies can be a subclass of the enemy class
We also need a player class 
Need multiple menus
Maybe even room for mulitple skins
Game continues forever
Can even end up spawning multiple King Zombies
King Zombie drops gems - which are used to buy cosmetics

Main character moves with WASD, points gun with mouse have a pointer on the screen
'''