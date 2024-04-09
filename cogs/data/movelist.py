import cogs.data.movefunctions as mv

class movelistclass:

    def __init__(self, level, lastMove=0, accmult=1.0, damagemult=1.0):
        self.level = level
        self.lastMove = lastMove
        self.accmult=accmult
        self.damagemult=damagemult
        self.movelist = {
            0:{
                "name":"No move", 
                "level":0, 
                "attack":(0,0), 
                "accuracy":0, 
                #"damage":(0,5),
                'class':mv.nomove,
                "method":mv.nomove.nomove
                },
            1:{
                "name":"Punch", 
                "level":1, 
                "attack":(0, 10), 
                "accuracy":99, 
                #"damage":(0,5),
                'class':mv.physical,
                "method":mv.physical.punch#(self, (0, 5), 99, self.level)
                },
            2:{
                "name":"Take Damage", 
                "level":1, 
                "attack":(0,10), 
                "accuracy":100, 
                #"damage":(0,5),
                'class':mv.special,
                "method":mv.special.takeDamage#(self, (0, 5), 100, self.level)
                },  
            3:{
                "name":"Boosted Punch", 
                "level":4, 
                "attack":(0, 20), 
                "accuracy":80, 
                #"damage":(0,5),
                'class':mv.physical,
                "method":mv.physical.boostedPunch#(self, (0, 5+(self.level*1.3)), 80, self.level, self.accmult, self.lastMove, )
            },
            4:{
                "name":"Star Finger", 
                "level":8, 
                "attack":(5, 15), 
                "accuracy":90, 
                #"damage":(0,5),
                "class":mv.physical,
                "method":mv.physical.starFinger
            }
            
        }