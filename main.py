import random
import math


class Dealer:
    def __init__(self, actions, game):
        self.game = game
        self.actions = actions

    def action_shot(self):
        bullet = random.choice([self.game.bullet, "blank", "bang"])
        if bullet == "blank":
            print("Dealer: I will shot my self")
            self.actions.shot("dealer")
        elif bullet == "bang":
            print("Dealer: I will shot you")
            self.actions.shot("player")

    def steps(self, bullets, blanks):
        print("dealer turn")
        chance = math.ceil((bullets / (bullets + blanks)) * 100)
        print("chance", chance)
        # if have smoke and healths is not 3 use smoke
        if chance <= 50:
            pass  # spyglass
        if chance == 50:  # and have cuffs
            pass  # handcuffs 
        elif chance == 50:
            pass # beer
        if chance >= 50:
            self.action_shot()


class Actions:
    def __init__(self, game):
        self.game = game
        self.skip_turn = False
        self.double_damage = 1

    def shot(self, who_to_hit="dealer"):
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
        else:
            print("that is not a answer")
            self.skip_turn = True

        if self.skip_turn:
            self.game.turn = False
            self.skip_turn = False
        else:
            self.game.turn = True
        self.double_damage = 1

    def spyglass(self):
        print("bullet = ", self.game.bullet)

    def smoke(self):
        if self.game.player_turn:
            self.game.healths["player"] += 1
        elif not self.game.player_turn:
            self.game.healths["dealer"] += 1
        else:
            print("somtihing is wrong")

    def beer(self):
        print("bullet", self.game.shell[self.game.i])
        self.game.shell.remove(self.game.i)

    def handcuffs(self):
        print("Dealer: fine I will cuff my self")
        self.skip_turn = True

    def saw(self):
        self.double_attack = 2
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
                print("remove item")
                self.player_inventory.remove(action)
                print("player inventory", self.player_inventory)
            try:
                self.actions_name_map[action]()
            except KeyError:
                print("that is not a action")
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
            self.get_user_input()

    def steps(self):
        bullets, blanks = self.count_bullets()
        print(f"bullets: {bullets}, blank: {blanks}")
        while not self.healths["player"] <= 0 and not self.healths["dealer"] <= 0:
            self.distributing_items()
            for self.i, self.bullet in enumerate(self.shell, start=1):
                print(self.healths)
                if self.i % 2 == 0:
                    self.player_turn = False
                    bullets, blanks = self.count_bullets()
                    self.dealer.steps(bullets, blanks)
                elif not self.i % 2 == 0:
                    self.player_turn = True
                    self.round()
                else:
                    RuntimeError("ingen sin turn!")

                if self._healths["player"] <= 0:
                    print("you lose")
                    break
                elif self._healths["dealer"] <= 0:
                    print("you have won")
                    break
                else:
                    print("no died")


def main():
    game = Game()
    game.steps()


main()
