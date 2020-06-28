import random


# Item class
class Item():
    def __init__(self, weight, worth):
        self.weight = weight
        self.worth = worth


# Subclass of Item contains values like damage and durability
class Weapon(Item):
    def __init__(self, weight, worth, damage, durability):
        Item.__init__(self, weight, worth)
        self.damage = damage
        self.durability = durability


# Weapon with predefined stats
class Swort(Weapon):
    def __init__(self, weight=50, worth=500, damage=10, durability=100):
        Weapon.__init__(self, weight, worth, damage, durability)


# Character class
class Charakter():
    def __init__(self, live):
        self.live = live

    # Function for giving damage to Characters
    def hit(self, weapon, target):
        target.live -= weapon.damage


# Player class. Subclass of Character
class Player(Charakter):
    inventory = []

    def __init__(self, live=100):
        Charakter.__init__(self, live)
        self.isInBattle = False

    # Used for handling commands
    def commandHandler(self, command=""):
        if command == "help":
            return "help"
        elif command == "hit" and self.isInBattle:
            return "hit"
        else:
            return "error"


# An example opponent
class Orc(Charakter):
    def __init__(self, live=20, weapon=Swort()):
        Charakter.__init__(self, live)
        self.weapon = weapon


# Map class containing a matrix of fields
class Map():
    def __init__(self, width=5, height=5, position=[0, 0]):
        self.position = position
        self.height = height
        self.width = width
        self.mapMatrix = [[0] * width] * height

    # Generates a matrix of fields
    def generate(self):
        for i in range(self.width):
            for j in range(self.height):
                self.mapMatrix[i][j] = Field()


# A field is containing infos abaout monster, items and other stuff
class Field():
    def __init__(self, monsterMin=0, monsterMax=1):
        self.monster = []
        self.monsterCount = 0
        for i in range(random.randint(monsterMin, monsterMax)):
            self.monster.append(Orc())
            self.monsterCount += 1


if __name__ == "__main__":
    # Initialising important objects
    player0 = Player()
    player0.inventory.append(Swort())
    world0 = Map()
    world0.generate()

    # Starting battle if monster in room
    if world0.mapMatrix[world0.position[0]][world0.position[1]].monsterCount != 0:
        print("There is an Orc in this room")
        player0.isInBattle = True

        # Continuing battle if the HP of the monster are != 0
        while world0.mapMatrix[world0.position[0]][world0.position[1]].monster[0].live != 0:
            action = player0.commandHandler(input("Please enter your move: "))
            if action == "help":
                print("You are in a battle. Possible actions are hit.")

            # Executing a hit with the weapon on the 0. slot of the inventory
            elif action == "hit":
                player0.hit(player0.inventory[0], world0.mapMatrix[world0.position[0]][world0.position[1]].monster[0])
                print("A hit! The Orc has",
                      str(world0.mapMatrix[world0.position[0]][world0.position[1]].monster[0].live), "lives left.")
                world0.mapMatrix[world0.position[0]][world0.position[1]].monster[0].hit(world0.mapMatrix[world0.position[0]][world0.position[1]].monster[0].weapon, player0)
                print("You got hurt! You have", player0.live, "left.")
            elif action == "error":
                print("Please enter a valid command! Enter help for help.")
        else:
            print("You killed the Orc!")

    else:
        print("This room is clear")
