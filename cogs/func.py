import cogs.getdata as getdata

def reset(id):
    users = getdata.users.read_info()
    users[id] = {
        #"name":???,
        "moves":[0, 0, 0, 0],
        "stand":0,
        "level":0,
        "exp":0,
        "reqExp":15,
        "battle":True,
        "health":20,
        "maxHealth":20,
        "resets":0,
        "damageMult":1,
        "accMult":1,
        "lastMove":0
    }
    getdata.users.update_info(users)

    return users
