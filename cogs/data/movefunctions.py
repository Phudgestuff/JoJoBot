import random
import math

def doesMoveHit(accuracy):
    rand = random.randint(0,100)
    moveHits = (rand <= accuracy)
    return moveHits

class physical:

    def punch(self, damage, accuracy, level, accmult, damagemult=1, lastmove=0):
        moveHits = doesMoveHit(accuracy)
        moveDamage = math.floor(random.randint(damage[0], damage[1]) * (1 + (level-1)/5))

        if moveHits:
            bracks = "{}"
            return {"hit":True, "userDamage":0, "enemyDamage":moveDamage, "accMult":1, "damageMult":1, "text":f"Hit {bracks} for {moveDamage} damage"}
        else:
            return {"hit":False, "userDamage":0, "enemyDamage":0, "accMult":1, "damageMult":1, "text":"Missed!"}

    def boostedPunch(self, damage, accuracy, level, accmult, damagemult=1, lastmove=0):
        c = physical
        #print(accuracy*accmult, "boosted accuracy")
        if lastmove == 3:
            bpunch = physical.punch(self, damage, accuracy*accmult, level, accmult, damagemult, lastmove)
        else:
            bpunch = physical.punch(self, damage, accuracy, level, accmult, damagemult, lastmove)
        accmult *= 0.7

        bpunch['accMult'] *= accmult
        return bpunch
    
    def starFinger(self, damage, accuracy, level, accmult, damagemult=1, lastmove=0):
        moveHits = doesMoveHit(accuracy)
        moveDamage = math.floor(random.randint(damage[0], damage[1]) * (1 + (level-1)/5))

        #print('lastmove:', lastmove)
        if lastmove == 4:
            return {"hit":False, "userDamage":0, "enemyDamage":0, "accMult":accmult, "damageMult":1, "text":"Hold on! Allow star finger to calm down."}
        else:
            if moveHits:
                bracks = "{}"
                return {"hit":True, "userDamage":0, "enemyDamage":moveDamage, "accMult":1, "damageMult":1, "text":f"Finger shot {bracks} right in the head for {moveDamage} damage"}
            else:
                return {"hit":False, "userDamage":0, "enemyDamage":0, "accMult":1, "damageMult":1, "text":"Missed!"}            

        
    

class special:

    def takeDamage(self, damage, accuracy, level, accmult, damagemult=1, lastmove=0):
        moveDamage = math.floor(random.randint(damage[0], damage[1]) * (1 + (level-1/10)))
        return {"hit":True, "userDamage":moveDamage, "enemyDamage":0, "accMult":1, "damageMult":1, "text":f"Took {moveDamage} damage"}
    
class nomove:
    def nomove(self, damage, accuracy, level, accmult, damagemult=1, lastmove=0):
        return False
    
