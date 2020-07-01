import random


class Game():
    state = True

    @staticmethod
    def end(cause="suicide"):
        if cause == "suicide":
            print("You commited suicide")
            exit()
        elif cause == "killed":
            print("You were slained to death")
            exit()
        else:
            exit()


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
        self.alive = True

    # Function for giving damage to Characters
    def hit(self, weapon, target):
        target.live -= weapon.damage
        if target.live <= 0:
            target.die()

    def die(self):
        self.alive = False


# Player class. Subclass of Character
class Player(Charakter):
    inventory = []

    def __init__(self, live=100, position=[0, 0], roomIdle=False):
        Charakter.__init__(self, live)
        if position is None:
            position = [0, 0]
        self.isInBattle = False
        self.position = position
        self.roomIdle = roomIdle

    # Used for handling commands
    def commandHandler(self, command=""):
        if command == "help":
            return "help"
        elif command == "hit" and self.isInBattle:
            return "hit"
        elif command == "right" and self.isInBattle == False:
            return "right"
        elif command == "left" and self.isInBattle == False:
            return "left"
        elif command == "up" and self.isInBattle == False:
            return "up"
        elif command == "down" and self.isInBattle == False:
            return "down"
        elif command == "view" and self.isInBattle == False:
            return "view"
        else:
            return "error"

    # Moves into given direction by changing the players position array
    def move(self, direction=""):
        if direction == "up":
            if self.position[1] < world0.height:
                self.position[1] += 1
                return True
            else:
                return False
        elif direction == "down":
            if self.position[1] >= 1:
                self.position[1] -= 1
                return True
            else:
                return False
        elif direction == "right":
            if self.position[0] < world0.width:
                self.position[0] += 1
                return True
            else:
                return False
        elif direction == "left":
            if self.position[0] >= 1:
                self.position[0] -= 1
                return True
            else:
                return False
        else:
            return False

    def die(self):
        Game.end(cause="killed")


# An example opponent
class Orc(Charakter):
    def __init__(self, live=20, weapon=Swort()):
        Charakter.__init__(self, live)
        self.weapon = weapon


# Map class containing a matrix of fields
class Map():
    def __init__(self, width=5, height=5):
        self.height = height
        self.width = width
        self.mapMatrix = [[0] * width] * height

    # Generates a matrix of fields
    def generate(self):
        for i in range(self.width):
            for j in range(self.height):
                self.mapMatrix[i][j] = Field()

    def view(self, player):
        answer = ""
        if player.position[1] == self.height:
            answer += "The way up is blocked\n"
        else:
            answer += "The way up is opened\n"
        if player.position[1] == 0:
            answer += "The way down is blocked\n"
        else:
            answer += "The way down is opened\n"
        if player.position[0] == self.width:
            answer += "The way right is blocked\n"
        else:
            answer += "The way right is opened\n"
        if player.position[0] == 0:
            answer += "The way left is blocked\n"
        else:
            answer += "The way left is opened\n"
        return answer


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
    while Game.state:
        if world0.mapMatrix[player0.position[0]][player0.position[1]].monsterCount != 0 and \
                world0.mapMatrix[player0.position[0]][player0.position[1]].monster[0].alive == True:
            print("There is an Orc in this room")
            player0.isInBattle = True

            # Continuing battle if the HP of the monster are != 0
            while world0.mapMatrix[player0.position[0]][player0.position[1]].monster[0].alive:
                action = player0.commandHandler(input("Please enter your move: "))
                if action == "help":
                    print("You are in a battle. Possible actions are hit.")

                # Executing a hit with the weapon on the 0. slot of the inventory
                elif action == "hit":
                    player0.hit(player0.inventory[0],
                                world0.mapMatrix[player0.position[0]][player0.position[1]].monster[0])
                    print("A hit! The Orc has",
                          str(world0.mapMatrix[player0.position[0]][player0.position[1]].monster[0].live), "lives left.")
                    world0.mapMatrix[player0.position[0]][player0.position[1]].monster[0].hit(
                        world0.mapMatrix[player0.position[0]][player0.position[1]].monster[0].weapon, player0)
                    print("You got hurt! You have", player0.live, "left.")
                elif action == "error":
                    print("Please enter a valid command! Enter help for help.")
            else:
                print("You killed the Orc!")
                player0.isInBattle = False
                player0.roomIdle = False
        else:
            print("This room is clear")
            player0.roomIdle = True

        while player0.roomIdle:
            action = player0.commandHandler(input("Please enter your command: "))
            if action == "help":
                print("Please enter your movement direction")
            elif action == "error":
                print("This is no valid command. Enter help for help.")
            elif action == "view":
                print(world0.view(player=player0))
            elif action == "up":
                if player0.move(direction="up"):
                    print("Moved up.")
                    player0.roomIdle = False
                else:
                    print("You cant move in this direction")
            elif action == "down":
                if player0.move(direction="down"):
                    print("Moved down.")
                    player0.roomIdle = False
                else:
                    print("You cant move in this direction")
            elif action == "left":
                if player0.move(direction="left"):
                    print("Moved left.")
                    player0.roomIdle = False
                else:
                    print("You cant move in this direction")
            elif action == "right":
                if player0.move(direction="right"):
                    print("Moved right.")
                    player0.roomIdle = False
                else:
                    print("You cant move in this direction")