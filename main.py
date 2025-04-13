from ast import With
import random
import math
import os
import time


class Dealer:
    def __init__(self, actions, game):
        self.game = game
        self.actions = actions
        self.bullet = None
        self.turn = False

    def action_shot(self):
        self.bullet = random.choice([self.game.bullet, "blank", "bang"])
        if self.bullet == "blank":
            print("Dealer: I will shot my self")
            self.turn = self.actions.shot("dealer", "dealer")
        elif self.bullet == "bang":
            print("Dealer: I will shot you")
            self.turn = self.actions.shot("player", "dealer")
        self.bullet = None

    def steps(self, bullets, blanks):
        print("dealer turn")
        print(self.game.healths)
        time.sleep(1)
        chance = math.ceil((bullets / (bullets + blanks)) * 100)
        self.turn = False
        while not self.turn:
            print(" ")

            if (
                "smoke" in self.game.dealer_inventory
                and self.game.healths["dealer"] >= 3
            ):
                print("dealer smokes")
                self.game.dealer_inventory.remove("smoke")
                self.actions.smoke("dealer")
            if "spyglass" in self.game.dealer_inventory:
                print("Dealer: very intesting, (dealer uses a spyglass)")
                self.game.dealer_inventory.remove("spyglass")
                self.bullet = self.actions.spyglass("dealer")
            if chance == 50 and "handcuffs" in self.game.dealer_inventory:
                print("dealer: but this on, (dealer uses handcuffs)")
                self.game.dealer_inventory.remove("handcuffs")
                self.actions.handcuffs("dealer")
            if chance == 50 and "beer" in self.game.dealer_inventory:
                print("dealer: I will remove a bullet, (dealer drinks a beer)")
                self.game.dealer_inventory.remove("beer")
                self.actions.beer()
            if chance >= 50 or not self.bullet == None:
                print("dealer shots")
                self.action_shot()
            else:
                self.action_shot()

        print(" ")
        input("write anything to continue")
        os.system("clear")


class Actions:
    def __init__(self, game):
        self.game = game
        self.skip_turn = False
        self.double_damage = 1

    def shot(self, who_to_hit="dealer", user="player"):
        if not self.game.i % 2 == 0:
            who_to_hit = input("who do you want to shot, player or dealer? ")

        if who_to_hit.lower() == "player":
            self.game.healths["player"] -= (
                self.game.round_value[self.game.bullet] * self.double_damage
            )
            if self.game.bullet == "blank" and self.game.player_turn:
                self.skip_turn = True

        elif who_to_hit.lower() == "dealer":
            self.game.healths["dealer"] -= (
                self.game.round_value[self.game.bullet] * self.double_damage
            )
            if self.game.bullet == "blank" and not self.game.player_turn:
                self.skip_turn = True

        next = None

        if self.skip_turn:
            self.skip_turn = False
            if user == "player":
                self.game.turn = False
            else:
                print("health", self.game.healths)
                next = False
        else:
            self.game.turn = True
            next = True

        self.double_damage = 1
        return next

    def spyglass(self, user="player"):
        if user == "player":
            print("bullet = ", self.game.bullet)

        return self.game.bullet

    def smoke(self, user="player"):
        self.game.healths[user] += 1
        print("health", self.game.healths)

    def beer(self):
        print("bullet", self.game.shell[self.game.i])
        item_to_remove = self.game.shell[self.game.i]
        self.game.shell.remove(item_to_remove)

    def handcuffs(self, user="you"):
        print(user, " will cuff your self")
        self.skip_turn = True
        print("skip turn", self.skip_turn)

    def saw(self):
        self.double_damage = 2
        print("double damage")


class Game:
    def __init__(self, starting_health=3):
        self.actions = Actions(self)
        self.dealer = Dealer(self.actions, self)
        self.player_inventory = []
        self.dealer_inventory = []
        self.player_turn = False
        self.dealer_turn = False
        # give items
        self._healths = {
            "dealer": starting_health,
            "player": starting_health,
        }
        self.actions_name_map = {
            "shot": self.actions.shot,
            "spyglass": self.actions.spyglass,
            "handcuffs": self.actions.handcuffs,
            "beer": self.actions.beer,
            "smoke": self.actions.smoke,
            "saw": self.actions.saw,
        }
        self.round_value = {"blank": 0, "bang": 1}
        self.shell = [
            random.choice(["blank", "bang"]) for _ in range(random.randint(6, 12))
        ]
        self.turn = False

    def distributing_items(self):
        items = [
            "beer",
            "spyglass",
            "handcuffs",
            "smoke",
            "saw",
        ]
        for _ in range(4):
            # players item
            item = random.choice(items)
            print("you got a ", item)
            self.player_inventory.append(item)
            # dealer item
            item = random.choice(items)
            self.dealer_inventory.append(item)

    @property
    def healths(self):
        return self._healths

    @healths.setter
    def healths(self, new_healths):
        return self._healths == new_healths

    def get_user_input(self):
        action = input(
            "Dealer: do you what to shot or a item? (write the name of the item you want to use) "
        )
        if action in self.player_inventory or action == "shot":
            if not action == "shot":
                self.player_inventory.remove(action)
                print("player inventory", self.player_inventory)
            try:
                self.actions_name_map[action]()
            except KeyError:
                print("that is not a action")
                time.sleep(2)
                return
        else:
            print("you do not have a", action)

    def count_bullets(self):
        bullets = 0
        blanks = 0
        for i in self.shell:
            if i == "bang":
                bullets += 1
            else:
                blanks += 1

        return bullets, blanks

    def round(self):
        self.turn = False
        while not self.turn:
            print("invenotry", self.healths)
            print(self.player_inventory)
            self.get_user_input()
            time.sleep(3)
            os.system("clear")

    def steps(self):
        bullets, blanks = self.count_bullets()
        print(f"bullets: {bullets}, blank: {blanks}")
        while self.healths["player"] > 0 and self.healths["dealer"] > 0:
            self.distributing_items()
            for self.i, self.bullet in enumerate(self.shell, start=1):
                if self.i % 2 == 0:
                    self.player_turn = False
                    bullets, blanks = self.count_bullets()
                    self.dealer.steps(bullets, blanks)
                elif not self.i % 2 == 0:
                    self.player_turn = True
                    self.round()

                if self._healths["player"] <= 0:
                    print("you lose")
                    break
                if self._healths["dealer"] <= 0:
                    print("you have won")
                    break


def main():
    game = Game()
    game.steps()


main()
