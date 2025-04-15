"my version of BuckShotRoulette"

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

    def action_shoot(self):
        self.bullet = random.choice([self.game.bullet, "blank", "bang"])
        if self.bullet == "blank":
            print("Dealer: I will shoot my self")
            self.turn = self.actions.shoot("dealer", "dealer")
        elif self.bullet == "bang":
            print("Dealer: I will shoot you")
            self.turn = self.actions.shoot("player", "dealer")
        self.bullet = None

    def step(self, bullets, blanks):
        print("dealer turn")
        print(self.game.healths)
        time.sleep(1)
        chance = math.ceil((bullets / (bullets + blanks)) * 100)
        self.turn = False
        while not self.turn:
            print(" ")

            if (
                "smoke" in self.game.dealer_inventory
                and self.game.healths["dealer"] < 4
            ):
                print("dealer smokes")
                self.game.dealer_inventory.remove("smoke")
                self.actions.smoke("dealer")
                continue
            if chance == 50 and "beer" in self.game.dealer_inventory:
                print("dealer: I will remove a bullet, (dealer drinks a beer)")
                self.game.dealer_inventory.remove("beer")
                self.actions.beer()
                continue
            if "spyglass" in self.game.dealer_inventory:
                print("Dealer: very intesting, (dealer uses a spyglass)")
                self.game.dealer_inventory.remove("spyglass")
                self.bullet = self.actions.spyglass("dealer")
            if chance == 50 and "handcuffs" in self.game.dealer_inventory:
                print("dealer: but this on, (dealer uses handcuffs)")
                self.game.dealer_inventory.remove("handcuffs")
                self.actions.handcuffs("you")

            if chance >= 50 or self.bullet is not None:
                print("dealer shoots")
                self.action_shoot()
            else:
                self.action_shoot()

        print(" ")
        input("write anything to continue")
        os.system("clear")


class Actions:
    def __init__(self, game):
        self.game = game
        self.skip_turn = False
        self.double_damage = 1

    def shoot(self, who_to_hit="dealer", user="player"):
        if not self.game.shell_index % 2 == 0:
            who_to_hit = input("who do you want to shoot, player or dealer? ")

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

        switch = False

        if self.skip_turn:
            self.skip_turn = False
            if user == "player":
                self.game.turn = False
            else:
                print("health", self.game.healths)
                switch = False
        else:
            self.game.turn = True
            switch = True

        self.double_damage = 1
        print(self.game.bullet)
        return switch

    def spyglass(self, user="player"):
        if user == "player":
            print("bullet = ", self.game.bullet)

        return self.game.bullet

    def smoke(self, user="player"):
        if self.game.healths[user] <= 4 and user == "player":
            self.game.healths[user] = 4
            self.game.player_inventory.append("smoke")
            print("you have full health")
        else:
            self.game.healths[user] += 1

        print("health", self.game.healths)

    def beer(self):
        print("bullet", self.game.shell[self.game.shell_index])
        item_to_remove = self.game.shell[self.game.shell_index]
        self.game.shell.remove(item_to_remove)

    def handcuffs(self, user="dealer"):
        print(user, " is cuff ")
        self.skip_turn = True

    def saw(self):
        self.double_damage = 2
        print("double damage")


class Game:
    def __init__(self, starting_health=4):
        self.actions = Actions(self)
        self.dealer = Dealer(self.actions, self)
        self.player_inventory = []
        self.dealer_inventory = []
        self.player_turn = False
        self.dealer_turn = False
        self.shell_index = None
        self.bullet = None
        # give items
        self._healths = {
            "dealer": starting_health,
            "player": starting_health,
        }
        self.actions_name_map = {
            "shoot": self.actions.shoot,
            "spyglass": self.actions.spyglass,
            "handcuffs": self.actions.handcuffs,
            "beer": self.actions.beer,
            "smoke": self.actions.smoke,
            "saw": self.actions.saw,
        }
        self.round_value = {"blank": 0, "bang": 1}
        self.shell = [
            random.choice(["blank", "bang"]) for _ in range(random.randint(4, 6))
        ]
        self.turn = False

    def rules(self):
        os.system("clear")
        print("""
        Rules

        You and the dealer (a robot) take turns exchanging a gun.
        This gun contains a mix of bullets and blanks.

        When you shoot the dealer or yourself with a **bullet**, it becomes the other person's turn.
        If you shoot yourself with a **blank**, you get to keep playing.
        If you shoot yourself with a **bullet**, you lose 1 health

        You and the dealer continue taking turns until one of you run out of health.
        If the gun runs out of ammunition, it will be reloaded.

        Items & Actions

        Beer
        Drink a beer to remove the next incoming bullet.

        Handcuffs
        Use handcuffs to restrain the dealer, allowing you to keep playing after having shot someoe once.
        If you shoot yourself with a blank while the dealer is handcuffed, you still keep playing.

        Saw
        Cut off the barrel of the gun to double the damage when you shoot.

        Shoot
        Fire the gun. If you shoot someone with a bullet, they take 1 damage.
        If the gun is empty, no damage is dealt.
        If you shoot yourself and it’s a blank or the gun is empty, you keep playing.

        Smoke
        Heal yourself by 1 point (max health is 3).

        Spyglass
        Use the spyglass to see the next round in the chamber.
        """)

        print(" ")
        input("write anything to continue")
        os.system("clear")

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
        print("whrite `help` if you want to read the rules")
        action = input(
            "Dealer: do you what to shoot or use a item? (write the name of the item you want to use or 'shoot') "
        )
        if action.lower() == "help":
            self.rules()
            return

        if action in self.player_inventory or action == "shoot":
            if not action == "shoot":
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
            print("healths", self.healths)
            print("invenotory", self.player_inventory)
            self.get_user_input()
            time.sleep(3)
            os.system("clear")

    def step(self):
        self.distributing_items()
        bullets, blanks = self.count_bullets()
        print("reload the gun")
        print(f"bullets: {bullets}, blank: {blanks}")
        for self.shell_index, self.bullet in enumerate(self.shell, start=1):
            if self.shell_index % 2 == 0:
                self.player_turn = False
                bullets, blanks = self.count_bullets()
                self.dealer.step(bullets, blanks)
            elif not self.shell_index % 2 == 0:
                self.player_turn = True
                self.round()

            if self._healths["player"] <= 0:
                print("you lose")
                break
            if self._healths["dealer"] <= 0:
                print("you have won")
                break

    def run(self):
        while self.healths["player"] > 0 and self.healths["dealer"] > 0:
            self.step()


def main():
    game = Game()
    game.rules()
    game.run()


main()
