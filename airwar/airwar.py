import pygame
import random

#System settings

pygame.init()
fps = pygame.time.Clock()
screenWidth = 1500
screenHeight = 900
screen = pygame.display.set_mode((screenWidth, screenHeight))
timeControl = 30
loseCondition = False

#Game over display function

def gameOverDisplay():
    font = pygame.font.Font("CollegiateFLF.ttf", 50)
    gameOver = font.render("Game over!", True, (255, 255, 255))
    screen.blit(gameOver, (screenWidth/2 - gameOver.get_width()/2, screenHeight/2 - gameOver.get_height()/2))
    

#Title and icon

pygame.display.set_caption("Air war")
gameIcon = pygame.image.load("rv.png")
pygame.display.set_icon(gameIcon)

#Base class game object. Serves as the base for inheritance of other classes

class gameObject:
    def __init__(self, posX, posY, movS, img):
        self.positionX = posX
        self.positionY = posY
        self.movementSpeed = movS
        self.objectImage = pygame.image.load(img)

    def getPositionX(self):
        return self.positionX

    def getPositionY(self):
        return self.positionY

    def getMovementSpeed(self):
        return self.movementSpeed

    def setPositionX(self, pos):
        self.positionX = pos

    def setPositionY(self, pos):
        self.positionY = pos

    def setMovementSpeed(self, ms):
        self.movementSpeed = ms

    def getObjectImage(self):
        return self.objectImage

#Both missile and bullet have same attributes, only their mechanics differ,
#which will be resolved through game logic
class projectileObject(gameObject):
    def __init__(self, posX, posY, movS, img):
        super().__init__(posX, posY, movS, img)
        self.projectileFiredStatus = False

    def setFiredStatus(self, fs):
        self.projectileFiredStatus = fs

    def getFiredStatus(self):
        return self.projectileFiredStatus


#Explosion class, needs additional attribute in order to control vanishing, also explosion sound
class explosionObject(gameObject):
    def __init__(self, posX, posY, movS, img):
        super().__init__(posX, posY, movS, img)
        self.timer = timeControl
        self.explosionSound = pygame.mixer.Sound("explosion.wav")

    def getTimer(self):
        return self.timer

    def setTimer(self, tm):
        self.timer = tm
        
    def getExplosionSound(self):
        return self.explosionSound


#Player class
class playerObject(gameObject):
    def __init__(self, posX, posY, movS, img):
        super().__init__(posX, posY, movS, img)
        self.boundaryLeft = -self.getObjectImage().get_width()/2
        self.boundaryRight = screenWidth - self.getObjectImage().get_width()/2

    def getBoundaryLeft(self):
        return self.boundaryLeft

    def getBoundaryRight(self):
        return self.boundaryRight


#Enemy class
class enemyObject(gameObject):
    def __init__(self, posX, posY, movS, img):
        super().__init__(posX, posY, movS, img)
        self.boundaryBottom = screenHeight + self.getObjectImage().get_height()
        self.boundaryTop = - 3*self.getObjectImage().get_height()

    def getBoundaryBottom(self):
        return self.boundaryBottom

    def getBoundaryTop(self):
        return self.boundaryTop


#Background 
class backgroundObject:
    def __init__(self, posX, posY, movs, img):
        self.backgroundImage = pygame.image.load(img).convert()
        self.movementSpeed = movs
        self.backgroundX = posX
        self.backgroundY = posY
        self.movementSpeed = movs
        self.boundaryBottomBackground = self.backgroundImage.get_height()
        self.boundaryTopBackground = -self.backgroundImage.get_height()

    def getImage(self):
        return self.backgroundImage

    def getBoundaryBottom(self):
        return self.boundaryBottomBackground

    def getBoundaryTop(self):
        return self.boundaryTopBackground

    def getBackgroundX(self):
        return self.backgroundX

    def getBackgroundY(self):
        return self.backgroundY

    def setBackgroundX(self, bg):
        self.backgroundX = bg

    def setBackgroundY(self, bg):
        self.backgroundY = bg

    def getMovementSpeed(self):
        return self.movementSpeed

    def setMovementSpeed(self, ms):
        self.movementSpeed = ms


#Game menu
menuProcess = True
selectedPlane = None
startButton = pygame.image.load("start.png")
menuBackground = pygame.image.load("menubackground.png").convert()
pygame.mixer.music.load("backgroundmusic.mp3")
pygame.mixer.music.play(-1)


#Menu drawing function. We define the font we wish to use, then we render it, so blit() function can present it on screen.
#2nd parameter determines if anti-aliasing should be done, and 3rd parameter is text color
def menuDraw():
    screen.blit(menuBackground, (0,0))
    screen.blit(startButton, (2*screenWidth/3, screenHeight/2))
    font = pygame.font.Font("CollegiateInsideFLF.ttf", 30)
    instructionGiver = font.render("Press key to select plane:", True, (255, 255, 255))
    firstPlane = font.render("1. MIG-29", True, (255, 255, 255))
    secondPlane = font.render("2. Su-35", True, (255, 255, 255))
    thirdPlane = font.render("3. MIG-31", True, (255, 255, 255))
    fourthPlane = font.render("4. F-14", True, (255, 255, 255))
    fifthPlane = font.render("5. F/A-18", True, (255, 255, 255))
    screen.blit(instructionGiver, (0, screenHeight/7))
    screen.blit(firstPlane, (screenWidth/7, 2*screenHeight/7))
    screen.blit(secondPlane, (screenWidth/7, 3*screenHeight/7))
    screen.blit(thirdPlane, (screenWidth/7, 4*screenHeight/7))
    screen.blit(fourthPlane, (screenWidth/7, 5*screenHeight/7))
    screen.blit(fifthPlane, (screenWidth/7, 6*screenHeight/7))

#Menu functon. Same as the game loop, save for mouse. NOTE: It's important to prevent error if no plane is selected
while menuProcess:
    menuDraw()
    pygame.display.update()
    fps.tick(60)
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            selectedPlane = "mig29.png"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            selectedPlane = "su35.png"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            selectedPlane = "mig31.png"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            selectedPlane = "f14.png"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            selectedPlane = "fa18.png"
        elif event.type == pygame.MOUSEBUTTONDOWN and mouseX >= 2*screenWidth/3 and mouseX <= 2*screenWidth/3  + startButton.get_width() and mouseY >= screenHeight/2 and mouseY<= screenHeight/2 + startButton.get_height():
            if selectedPlane != None:
                menuProcess = False
                

#Generating objects, int() functions are being used because we often need to divide by 2, and randint function
#only takes int numbers, not floating point ones
background1 = backgroundObject(0, 0, 2, "background1.png")
background2 = backgroundObject(0, -background1.getImage().get_height(), 2, "background2.png")
player = playerObject(screenWidth/2, screenHeight - 250 , 10, selectedPlane)
bullet = projectileObject(player.getPositionX() + player.getObjectImage().get_width()/2 , player.getPositionY() + player.getObjectImage().get_height()/2, 0, "bullet.png")
bulletEnemy = projectileObject(0, -2*player.getObjectImage().get_height(), 0, "bullet.png")
missile = projectileObject(player.getPositionX() + player.getObjectImage().get_width()/2 , player.getPositionY() + player.getObjectImage().get_height()/2, 0, "missile.png")    
enemy = enemyObject(0, -screenHeight, 3, "f4.png")
explosion = explosionObject(-200, -300, 2, "explosion.png")


#Draw function for objects
def draw(background1, background2, bullet, bulletEnemy, missile, enemy, player):
    screen.blit(background1.getImage(), (background1.getBackgroundX(), background1.getBackgroundY()))
    screen.blit(background2.getImage(), (background2.getBackgroundX(), background2.getBackgroundY()))
    screen.blit(bullet.getObjectImage(), (bullet.getPositionX(), bullet.getPositionY()))
    screen.blit(bulletEnemy.getObjectImage(), (bulletEnemy.getPositionX(), bulletEnemy.getPositionY()))
    screen.blit(missile.getObjectImage(), (missile.getPositionX(), missile.getPositionY()))
    screen.blit(enemy.getObjectImage(), (enemy.getPositionX(), enemy.getPositionY()))
    screen.blit(player.getObjectImage(), (player.getPositionX(), player.getPositionY()))
    screen.blit(explosion.getObjectImage(), (explosion.getPositionX(), explosion.getPositionY()))


#Weapon impact collision functions, b stands for bullet, m for missile
def collision(enXcoordinate,enYcoordinate,bXcoordinate,bYcoordinate):
    distanceX = abs((enXcoordinate + enemy.getObjectImage().get_width()/2) - bXcoordinate)
    distanceY = abs((enYcoordinate + enemy.getObjectImage().get_height()/2) - bYcoordinate)
    if distanceX < 60 and distanceY < 10:
        return True
    else:
        return False

def missileImpact(enXcoordinate,enYcoordinate,mXcoordinate,mYcoordinate):
    distanceX = abs((enXcoordinate + enemy.getObjectImage().get_width()/2) - mXcoordinate)
    distanceY = abs((enYcoordinate + enemy.getObjectImage().get_height()/2) - mYcoordinate)
    if distanceX <= 80 and distanceY <= 15:
        return True
    else:
        return False


#Game loop
running = True
positionChange = 0
try:
    while running:
        fps.tick(60)
        draw(background1, background2, bullet, bulletEnemy, missile, enemy, player)
        if loseCondition:
            gameOverDisplay()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                positionChange = -player.getMovementSpeed()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                positionChange = player.getMovementSpeed()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bullet.getFiredStatus() == False:
                bullet.setMovementSpeed(32)
                bullet.setFiredStatus(True)
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c and missile.getFiredStatus() == False:
                missile.setMovementSpeed(22)
                missile.setFiredStatus(True)
                
            elif event.type == pygame.KEYUP:
                positionChange = 0
            

        background1.setBackgroundY(background1.getMovementSpeed() + background1.getBackgroundY())
        if background1.getBackgroundY() > background1.getBoundaryBottom():
            background1.setBackgroundY(background1.getBoundaryTop())
            background1.setBackgroundY(background1.getMovementSpeed() + background1.getBackgroundY())
        if background1.getBackgroundY() > background1.getBoundaryBottom():
            background1.setBackgroundY(background1.getBoundaryTop())

        background2.setBackgroundY(background2.getMovementSpeed() + background2.getBackgroundY())
        if background2.getBackgroundY() > background2.getBoundaryBottom():
            background2.setBackgroundY(background2.getBoundaryTop())
            background2.setBackgroundY(background2.getMovementSpeed() + background2.getBackgroundY())
        if background2.getBackgroundY() > background2.getBoundaryBottom():
            background2.setBackgroundY(background2.getBoundaryTop())


        enemy.setPositionY(enemy.getMovementSpeed() + enemy.getPositionY())
        if abs(enemy.getPositionX() - player.getPositionX()) > 30 and enemy.getPositionX() > player.getPositionX():
            enemy.setPositionX(enemy.getPositionX() - enemy.getMovementSpeed())
        elif abs(enemy.getPositionX() - player.getPositionX()) > 30 and enemy.getPositionX() < player.getPositionX():
            enemy.setPositionX(enemy.getPositionX() + enemy.getMovementSpeed())
        if enemy.getPositionY() > enemy.getBoundaryBottom():
            enemy.setPositionY(enemy.getBoundaryTop())
            enemy.setPositionX(random.randint(20, 580))


        player.setPositionX(player.getPositionX() + positionChange)
        if player.getPositionX() <= player.getBoundaryLeft():
            player.setPositionX(player.getBoundaryLeft())
        if player.getPositionX() >= player.getBoundaryRight():
            player.setPositionX(player.getBoundaryRight())

        #Player bullet logic
        if bullet.getFiredStatus() == False:
            bullet.setPositionX(player.getPositionX() + player.getObjectImage().get_width()/2)
        if bullet.getPositionY() > -bullet.getObjectImage().get_height():
            bullet.setPositionY(bullet.getPositionY() - bullet.getMovementSpeed())
        else:
            bullet.setFiredStatus(False)
            bullet.setPositionY(player.getPositionY() + player.getObjectImage().get_height()/2)
            bullet.setMovementSpeed(0)
            
        #Enemy bullet logic
        if enemy.getPositionY() - player.getPositionY() > 0 :
            bulletEnemy.setPositionY(enemy.getPositionY())
            bulletEnemy.setPositionX(enemy.getPositionX() + enemy.getObjectImage().get_width()/2)
            bulletEnemy.setFiredStatus(False)
            bulletEnemy.setMovementSpeed(0)
        if bulletEnemy.getFiredStatus() == False:
            bulletEnemy.setPositionX(enemy.getPositionX() + enemy.getObjectImage().get_width()/2)
        if bulletEnemy.getPositionY() < screenHeight + bulletEnemy.getObjectImage().get_height():
            bulletEnemy.setPositionY(bulletEnemy.getPositionY() + bulletEnemy.getMovementSpeed())
        else:
            bulletEnemy.setFiredStatus(False)
            bulletEnemy.setPositionY(enemy.getPositionY() + enemy.getObjectImage().get_height()/2)
            bulletEnemy.setMovementSpeed(0)
        if abs(enemy.getPositionX() - player.getPositionX()) < 60 :
            bulletEnemy.setFiredStatus(True)
            bulletEnemy.setMovementSpeed(8)


        if missile.getFiredStatus() == True:
            #smoothing out algorithm
            if (missile.getPositionX() - missile.getMovementSpeed()) >= enemy.getPositionX():
                missile.setPositionX(missile.getPositionX() - missile.getMovementSpeed())
            elif (missile.getPositionX() + missile.getMovementSpeed()) < enemy.getPositionX():
                missile.setPositionX(missile.getPositionX() + missile.getMovementSpeed())
                
            if missile.getPositionY() > enemy.getPositionY():
                missile.setPositionY(missile.getPositionY() - missile.getMovementSpeed())
            elif missile.getPositionY() < enemy.getPositionY():
                missile.setPositionY(missile.getPositionY() + missile.getMovementSpeed())

            if missileImpact(enemy.getPositionX(), enemy.getPositionY(), missile.getPositionX(), missile.getPositionY()):
                explosion.setPositionX(enemy.getPositionX())
                explosion.setPositionY(enemy.getPositionY())
                explosion.setTimer(timeControl)
                explosion.getExplosionSound().play()
                enemy.setPositionX(random.randint(int(player.getObjectImage().get_width()), int(screenWidth - player.getObjectImage().get_width())))
                enemy.setPositionY( -4*enemy.getObjectImage().get_height())
                missile.setFiredStatus(False)

        if missile.getFiredStatus() == False:
            missile.setPositionX(player.getPositionX() + player.getObjectImage().get_width()/2)
            missile.setPositionY(player.getPositionY() + player.getObjectImage().get_height()/2)
            missile.setMovementSpeed(0)
        
        if collision(enemy.getPositionX(), enemy.getPositionY(), bullet.getPositionX(), bullet.getPositionY()):
            bullet.setPositionX(player.getPositionX() + player.getObjectImage().get_width()/2)
            bullet.setFiredStatus(False)
            bullet.setPositionY(player.getPositionY() + player.getObjectImage().get_height()/2)
            bullet.setMovementSpeed(0)
            explosion.setPositionX(enemy.getPositionX())
            explosion.setPositionY(enemy.getPositionY())
            explosion.setTimer(timeControl)
            explosion.getExplosionSound().play()
            enemy.setPositionX(random.randint(int(player.getObjectImage().get_width()/2), int(screenWidth - player.getObjectImage().get_width()/2)))
            enemy.setPositionY(-250)
            
        #If this condition is true, player is hit with a bullet and game ends
        if collision(player.getPositionX(), player.getPositionY(), bulletEnemy.getPositionX(), bulletEnemy.getPositionY()):
            bulletEnemy.setPositionX(enemy.getPositionX() + enemy.getObjectImage().get_width()/2)
            bulletEnemy.setFiredStatus(False)
            bulletEnemy.setPositionY(enemy.getPositionY() + enemy.getObjectImage().get_height()/2)
            bulletEnemy.setMovementSpeed(0)
            explosion.setPositionX(player.getPositionX())
            explosion.setPositionY(player.getPositionY())
            explosion.setTimer(timeControl)
            explosion.getExplosionSound().play()
            loseCondition = True
            #Uncomment next line if you want auto-exit from game once hit
            #running = False
        
        #Setting up explosion and it's duration
        explosion.setPositionY(explosion.getPositionY() + explosion.getMovementSpeed())
        explosion.setTimer(explosion.getTimer()-1)
        if explosion.getTimer() <= 0:
            explosion.setPositionX(-explosion.getObjectImage().get_width())
                

    pygame.quit()
except SystemExit:
    pygame.quit()
