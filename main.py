import random


class Dealer:
    def __init__(self, actions):
        self.actions = actions

    def steps(self, game):
        print("dealer turn")
        if game.bullet == "blank":
            print("Dealer: I will shot my self")
            self.actions.shot("me")
        elif game.bullet == "bang":
            print("Dealer: I will shot you")
            self.actions.shot("you")
        game.turn = True

        return True


class Actions:
    def __init__(self, game):
        self.game = game
        self.handcuffs_is_on = True

    def shot(self, who_to_hit="me"):
        if who_to_hit.lower() == "you" or "player":
            self.game.healths["player"] -= self.game.round_value[self.game.bullet]
        elif who_to_hit.lower() == "me" or "dealer":
            self.game.healths["dealer"] -= self.game.round_value[self.game.bullet]

        if self.handcuffs_is_on:
            self.game.turn = False
        else:
            self.game.turn = True

    def spyglass(self):
        print("bullet = ", self.game.bullet)

    def handcuffs(self):
        self.handcuffs_is_on = True


class Game:
    def __init__(self, starting_health=3):
        self.actions = actions = Actions(self)
        self.dealer = Dealer(actions)
        self._healths = {
            "dealer": starting_health,
            "player": starting_health,
        }
        self.actions_name_map = {
            "shot": self.actions.shot,
            "spyglass": self.actions.spyglass,
        }
        self.round_value = {"blank": 0, "bang": 1}
        self.shell = [
            random.choice(["blank", "bang"]) for _ in range(random.randint(6, 12))
        ]
        self.turn = False

    @property
    def healths(self):
        return self._healths

    @healths.setter
    def healths(self, new_healths):
        return self._healths == new_healths

    def get_user_input(self):
        action = input(
            "Dealer: do you what to shot or a item? (write the name of the item you want to use)"
        )
        try:
            self.actions_name_map[action]()
        except KeyError:
            print("that is not a action")
            return

    def count_bullets(self):
        bullets = 0
        blank = 0
        for i in self.shell:
            if i == "bang":
                bullets += 1
            else:
                blank += 1

        print(f" totale {bullets+blank}, bullets: {bullets}, blank: {blank}")

    def round(self):
        self.get_user_input()


    def steps(self):
        self.count_bullets()
        for self.i, self.bullet in enumerate(self.shell):
            self.turn = False
            while not self.turn:
                print(self.healths)
                if self.i % 2 == 0:
                    self.turn = self.dealer.steps(self)
                if not self.i % 2 == 0:
                    self.turn = self.round()
                else:
                    RuntimeError("ingen sin turn!")
                


def main():
    game = Game()
    game.steps()


main()
