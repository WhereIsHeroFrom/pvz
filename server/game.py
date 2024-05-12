from share.const import * 
from const import *
import pymysql
import json

class Game(object):
    def __init__(self):
        self.plantInfo = [ [0]*GRID_COUNT[1] for _ in range(GRID_COUNT[0]) ]
        self.connectMysql()
        self.loadPlantInfo()

    def connectMysql(self):
        config = {
            'host': DB_HOST,
            'port': DB_PORT,
            'user': DB_USER,
            'password': DB_PASS,
            'db': 'pvzdb',
            'charset': 'utf8mb4'
        }
        self.connection = pymysql.connect(**config)

    def executeSql(self, sqlcmd):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlcmd)
            self.connection.commit()
            results = cursor.fetchall()
            return results
        except Exception as e:
            print("execute failed!", sqlcmd, e)
            return []
    
    def loadPlantInfo(self):
        results = self.executeSql("select * from game;")
        if len(results) == 0:
            self.savePlantInfo()
        else:
            self.plantInfo = json.loads( results[0] )

    def savePlantInfo(self):
        plantInfo = json.dumps(self.plantInfo)
        self.executeSql( "INSERT INTO game (id, plantInfo) VALUES (0, '%s') ON DUPLICATE KEY UPDATE plantInfo = '%s';" % (plantInfo, plantInfo) )
        
    def checkAddPlant(self, pos, plant_idx):
        msg = {
            'type' : S2C_ADD_PLANT,
            'code' : S2C_CODE_FAILED,
            'pos' : pos,
            'plant_idx': plant_idx,
        }

        x, y = pos
        if x < 0 or x >= GRID_COUNT[0]:
            return msg
        if y < 0 or y >= GRID_COUNT[1]:
            return msg
        if self.plantInfo[x][y] != 0:
            return msg
        # 金钱判定

        self.plantInfo[x][y] = plant_idx
        self.savePlantInfo()
        msg['code'] = S2C_CODE_SUCCEED
        return msg