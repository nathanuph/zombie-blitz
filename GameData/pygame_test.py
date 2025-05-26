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

        self.font = pygame.font.SysFont('Corbel',35)
        self.text = self.font.render(text, True, color)
        
        self.on_click = on_click
        
    #loads the button onto the frame
    def load(self):
        pygame.draw.rect(screen, self.color, [self.position.x, self.position.y, self.size.x, self.size.y], 2, 3)
        
        #load text inside the button
        screen.blit(self.text , ((self.position.x + 10,
                                self.position.y + (self.size.y / 4))))


#handles switching between different scenes (main menu, settings etc)
class SceneHandler:
    def __init__(self):
        self.current = None

    #loads the current scene
    def load(self):
        self.current.load()

    #swaps out the current scene with a 'new' scene 
    def update(self, new):
        self.current = new

class Scene:
    def __init__(self, background):
        self.background = pygame.image.load(background).convert()
        self.default_bg_size = (500,500) #the size of the canvas
        self.background = pygame.transform.scale(self.background, self.default_bg_size)

        self.buttons = [] #holds the buttons that will appear on the scene

    #load in the assets of that scene 
    def load(self):
        screen.blit(self.background, (0,0))

        for button in self.buttons:
            button.load()
        
        pygame.display.flip() #update scene
    
    def update(self):
        None

#called when the start button is pressed
def start_game():
    scene_handler.update(game) #swaps the current scene out for the game scene 
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
game = Scene("MenuAssets/background.jpg")
main_menu = Scene("MenuAssets/main menu bg.jpg")

#instantiate scene handler
scene_handler.update(main_menu)

#generate buttons
main_menu.buttons = [
    Button((0,0,0), Vector(260,160), Vector(200,50), "START", start_game), #start button
    Button((0,0,0), Vector(260,220), Vector(200,50), "SETTINGS", None), #settings button
    Button((0,0,0), Vector(260,280), Vector(200,50), "HELP", None), #help button
    Button((0,0,0), Vector(260,340), Vector(200,50), "CREDITS", None), #credits button
    Button((0,0,0), Vector(260,400), Vector(200,50), "QUIT", None), #quit button
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
            #validate there is any buttons to click
            if len(scene_handler.current.buttons) != 0:
                for button in scene_handler.current.buttons:
                    #check if mouse click occurs within bounds of the button
                    if ((button.position.x <= mouse[0] <= (button.position.x + button.size.x)) 
                        and (button.position.y <= mouse[1] <= (button.position.y + button.size.y))):
                        button.on_click()
    
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