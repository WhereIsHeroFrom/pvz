import pygame
import image
import sunflower
import peashooter
import zombiebase
import time
import random
import data_object
import asyncclient
import asyncio
from const import *
from share.const import * 

class Game(object):
    def __init__(self, ds):
        self.ds = ds
        self.back = image.Image(PATH_BACK, 0, (0, 0), GAME_SIZE, 0)
        self.lose = image.Image(PATH_LOSE, 0, (0, 0), GAME_SIZE, 0)
        self.plants = []
        self.zombies = []
        self.summons = []
        self.gold = 100
        self.goldFont = pygame.font.Font(None, 60)

        self.zombie = 0
        self.zombieFont = pygame.font.Font(None, 60)

        self.zombieGenertateTime = 0

        self.isGameOver = False
        self.client = asyncclient.AsyncClient(self, SERVER_IP, SERVER_PORT)

    
    def renderFont(self):
        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (0, 0, 0))
        self.ds.blit(textImage, (13, 23))

        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (255, 255, 255))
        self.ds.blit(textImage, (10, 20))

        textImage = self.zombieFont.render("Score: " + str(self.zombie), True, (0, 0, 0))
        self.ds.blit(textImage, (13, 83))

        textImage = self.zombieFont.render("Score: " + str(self.zombie), True, (255, 255, 255))
        self.ds.blit(textImage, (10, 80))

    def draw(self):
        self.back.draw(self.ds)
        for plant in self.plants:
            plant.draw(self.ds)
        for summon in self.summons:
            summon.draw(self.ds)
        for zombie in self.zombies:
            zombie.draw(self.ds)
        self.renderFont()
        if self.isGameOver:
            self.lose.draw(self.ds)

    
    def update(self):
        self.back.update()
        for plant in self.plants:
            plant.update()
            if plant.hasSummon():
                summ = plant.doSummon()
                self.summons.append(summ)
        for summon in self.summons:
            summon.update()
        for zombie in self.zombies:
            zombie.update()
            if zombie.getRect().x < 0:
                self.isGameOver = True
        
        for summon in self.summons: 
            if summon.getRect().x > GAME_SIZE[0] or summon.getRect().y > GAME_SIZE[1]: 
                self.summons.remove(summon) 
                break 
        
        if time.time() - self.zombieGenertateTime > ZOMBIE_BORN_CD:
            self.zombieGenertateTime = time.time()
            self.addZombie(ZOMBIE_BORN_X, random.randint(0, GRID_COUNT[1]-1))
    
        
        self.checkSummonVSZombie()
        self.checkZombieVSPlant()
    
    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if summon.isCollide(zombie):
                    self.fight(summon, zombie)
                    if zombie.hp <= 0:
                        self.zombies.remove(zombie)
                        self.zombie += 1 
                    if summon.hp <= 0:
                        self.summons.remove(summon)
                    return 
        
    def checkZombieVSPlant(self):
        for zombie in self.zombies:
            for plant in self.plants:
                if zombie.isCollide(plant):
                    self.fight(zombie, plant)
                    if plant.hp <= 0:
                        self.plants.remove(plant)
                        return
        
    def getIndexByPos(self, pos):
        x = (pos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (pos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x, y
    
    def addSunFlower(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        sf = sunflower.SunFlower(SUNFLOWER_ID, pos)
        self.plants.append(sf)
    
    def addPeaShooter(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        sf = peashooter.PeaShooter(PEASHOOTER_ID, pos)
        self.plants.append(sf)
    
    def addZombie(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zm = zombiebase.ZombieBase(1, pos)
        self.zombies.append(zm)
    
    def fight(self, a, b):
        while True:
            a.hp -= b.attack
            b.hp -= a.attack
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                return False
        return False
    
    def checkLoot(self, mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect = summon.getRect()
            if rect.collidepoint(mousePos):
                self.summons.remove(summon)
                self.gold += summon.getPrice()
                return True
        return False

    def addPlant(self, pos, objId):
        x, y = pos
        if objId == SUNFLOWER_ID:
            self.addSunFlower(x, y)
        elif objId == PEASHOOTER_ID:
            self.addPeaShooter(x, y)


    def mouseClickHandler(self, btn):
        if self.isGameOver:
            return
        mousePos = pygame.mouse.get_pos()
        if self.checkLoot(mousePos):
            return
        if btn == 1:
            asyncio.run(self.client.c2s( {'type' : C2S_ADD_FLOWER , 'pos' : self.getIndexByPos(mousePos)} ))
        elif btn == 3:
            self.addPlant(self.getIndexByPos(mousePos), PEASHOOTER_ID)
