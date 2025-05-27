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
    def __init__(self, position, sprite):
        self.speed = 0
        self.position = position
        self.weapon = None
        self.inventory = []
        self.coins = 0
        self.sprite = sprite
        self.days_played = 0
        self.zombies_killed = 0

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

class Images: #images that can be generated onto a scene 
    def __init__(self, dest, position, size):
        self.image = pygame.image.load(dest).convert_alpha() #loads image from the destination
        self.scale = (size) #size given as a vector is the scale of the image 

        self.image = pygame.transform.scale(self.image, self.scale)

        self.position = position #the coordinates it will spawn at (given as a vector)
    
    def load(self):
        screen.blit(self.image, self.position)

class SceneText: #text that can be generated onto a screen
    def __init__(self, text, position, size, color):
        self.position = position #a vector with x and y coordinates
        self.font = pygame.font.SysFont('Corbel',size)
        self.text = self.font.render(text, True, color)

    def load(self):
        #load text onto scene
        screen.blit(self.text , (self.position.x, self.position.y))


#handles switching between different scenes (main menu, settings etc)
class SceneHandler:
    def __init__(self):
        self.current = None

    #loads the current scene
    def load(self):
        self.current.load()

    #swaps out the current scene with a 'new' scene 
    def update(self, new):
        new.previous = self.current #set the new slides previous slide attribute with the old slide 
        self.current = new
        self.load() #load the new screen 

    def previous(self):
        self.current = self.current.previous
        self.load()

class Scene:
    def __init__(self, background):
        self.background = pygame.image.load(background).convert()
        self.default_bg_size = (500,500) #the size of the canvas
        self.background = pygame.transform.scale(self.background, self.default_bg_size)

        self.previous = None #used for going back to the last page

        self.assets = [] #holds the buttons that will appear on the scene

        self.dynamic_assets_loader = None #used for scenes that change their assets dynamically

    #load in the assets of that scene 
    def load(self):
        if self.dynamic_assets_loader: #if a loader function is defined
            self.assets = self.dynamic_assets_loader() #regenerate assets

        screen.blit(self.background, (0,0))

        for asset in self.assets:
            asset.load()
        
        pygame.display.flip() #update scene
    
    def update(self):
        None

#called when the start button is pressed
def start_game():
    scene_handler.update(pre_game) #swaps the current scene out for the game scene 

def open_settings(): #opens settings menu
    scene_handler.update(settings) 

def open_help(): #opens help menu
    scene_handler.update(help)  

def open_credits(): #opens credits menu
    scene_handler.update(credits) 

def open_inventory():
    scene_handler.update(inventory)  

def open_store():
    scene_handler.update(store)

def go_back(): #goes back to the previous scene
    scene_handler.previous()


#used to equip a gun when clicked in the inventory
def equip(new_weapon):
    player.weapon = new_weapon
    print(player.weapon.name+"EQUIPPED")
    load_inventory_assets() #reloads the screen so colors update


def get_pre_game_assets(): #dynamically gets the assets for the pregame
    assets = [
        Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back), #back button
    
        Images(player.sprite, (20,50), (175,175)), #the main characters sprite

        Images("Sprites/coin.png", (250,75), (40,40)), #coin image
        SceneText(str(player.coins), Vector(300,85), 30, (0,0,0)), #amount of coins the player has

        Button((0,0,0), Vector(260,130), Vector(100,50), "STORE", open_store), #shop button
        Button((0,0,0), Vector(260,190), Vector(150,50), "INVENTORY", open_inventory), #shop button

        SceneText("Equipped:"+player.weapon.name, Vector(50,260), 30, (0,0,0)), #'equipped' 
        Images(player.weapon.sprite, (50,270), (100,100)), #image of gun currently equipped

        SceneText("Days: "+str(player.days_played), Vector(260,290), 30, (0,0,0)),
        SceneText("Zombies killed: "+str(player.zombies_killed), Vector(260, 320), 30, (0,0,0)),

        #button to 'enter the wasteland' start game
        Button((0,0,0), Vector(220,400), Vector(300,100), None, None)
    ]
    return assets 

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
pre_game = Scene("MenuAssets/pre game newbg.png")
settings = Scene("MenuAssets/settings bg.jpg")
credits = Scene("MenuAssets/default bg.jpg")
help = Scene("MenuAssets/default bg.jpg")
inventory = Scene("MenuAssets/inventory bg.jpg")
store = Scene("MenuAssets/store bg.png")

#generate player
player = Player(None, "Sprites/player.png")

#generate weapons
pistol = Weapon("Pistol", 1, None, "Sprites/weapons/pistol.png", None)
sniper = Weapon("Sniper", 1, None, "Sprites/weapons/sniper.png", None)
ak47 = Weapon("AK47", 5, None, "Sprites/weapons/ak47.png", None)
rocket_launcher = Weapon("Rocket Launcher", 10, None, "Sprites/weapons/rocket launcher.png", None)
shotgun = Weapon("Shotgun", 3, None, "Sprites/weapons/shotgun.png", None)

#equip default weapon
player.weapon = pistol
player.inventory.append(pistol)
player.inventory.append(sniper)
player.inventory.append(shotgun)
player.inventory.append(rocket_launcher)
player.inventory.append(ak47)


#instantiate scene handler
scene_handler.update(main_menu)

#generate assets for each menu
pre_game.dynamic_assets_loader = get_pre_game_assets #assigns the dynamic loader for pregame

main_menu.assets = [
    Button((0,0,0), Vector(260,180), Vector(200,50), "START", start_game), #start button
    Button((0,0,0), Vector(260,240), Vector(200,50), "SETTINGS", open_settings), #settings button
    Button((0,0,0), Vector(260,300), Vector(200,50), "HELP", open_help), #help button
    Button((0,0,0), Vector(260,360), Vector(200,50), "CREDITS", open_credits), #credits button
    Button((0,0,0), Vector(260,420), Vector(200,50), "QUIT", None), #quit button
]

credits.assets = [
    SceneText(" - programmed by Nathan Uphill", Vector(0,50), 30, (255,255,255)), 
    SceneText(" - sprites drawn by Nathan Uphill", Vector(0,150), 30, (255,255,255)), 
    SceneText(" - @nathanuph on github", Vector(0,250), 30, (255,255,255)), 
    SceneText(" - Backgrounds generated by Google Gemini", Vector(0,350), 30, (255,255,255)), 

    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back) #back button
]

settings.assets = [
    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back) #back button
]

help.assets = [
    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back) #back button
]

store.assets = [
    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back), #back button
]

inventory.assets = [
    Button((255,255,255), Vector(0,460), Vector(100,30), "<<<", go_back), #back button
]

#loop through the players inventory and display a button for each item 
#eqipped weapon will be highlighted in green
def load_inventory_assets():
    static_assets = [inventory.assets[0]] #the back button is static as it always stays the same 

    y_position = 50
    dynamic_assets =[] #holds the buttons for inventory as their color can change

    for item in player.inventory:
        color = (255,255,255) #default color white
        #check if the items the one equipped if so it makes the outline green
        if item == player.weapon:
            color = (50,205,50) 
        dynamic_assets.append(
            #check if the weapons the one equipped if so it makes the outline green
            Button(color, Vector(150,y_position), Vector(200, 40), item.name, lambda current_item=item: equip(current_item))
        )
        y_position += 50 #y position moves the next items button down by 50

    #inventory assets are comprised of the dynamic buttons and the back button
    inventory.assets = static_assets + dynamic_assets

    scene_handler.load()

load_inventory_assets()

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

"""
create a load_assets method in each scene 
This can then be called each time a scene is loaded into scene manager
this allows the scenes to be dynamic and therefore change even after being created the first time
"""