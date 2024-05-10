import sys
import os

current_path = os.path.abspath(__file__)
top_path = "\\".join(current_path.split('\\')[:-2])
sys.path.append(top_path)

from share.const import * 

class Game(object):
    def __init__(self):
        self.hasPlant = [ [0]*GRID_COUNT[1] for _ in range(GRID_COUNT[0]) ]

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
        if self.hasPlant[x][y] != 0:
            return msg
        # 金钱判定

        self.hasPlant[x][y] = plant_idx
        msg['code'] = S2C_CODE_SUCCEED
        return msg