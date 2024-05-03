import objectbase
import sunlight

class SunFlower(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(SunFlower, self).__init__(id, pos)
        self.hasSunlight = False
    
    def hasSummon(self):
        return self.hasSunlight

    def preSummon(self):
        self.hasSunlight = True

    def doSummon(self):
        if self.hasSummon():
            self.hasSunlight = False
            return sunlight.SunLight(2, (self.pos[0]+20, self.pos[1]-10))

