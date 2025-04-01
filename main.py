import random


class Dealer:
    def steps(self, game):
        print("dealer turn")
        if game.bullet == "blank":
            print("Dealer: I will shot my self")
            actions.shot(game)
        elif game.bullet == "bang":
            print("Dealer: I will shot you")
            actions.shot(game)


class Actions:
    def shot(self, game):
        who_to_hit = input("Dealer: who do you want to shot you or me ")
        if who_to_hit.lower() == "you" or "player":
            game.healths["player"] -= game.round[game.bullet]
        if who_to_hit.lower() == "me" or "dealer":
            game.healths["dealer"] -= game.round[game.bullet]

    def magnifying_glass(self, game):
        print("bullet = ", game.bullet)
        self.i -= 1


class Game:
    def __init__(self, starting_health=3):
        self._healths = {
            "dealer": starting_health,
            "player": starting_health,
        }
        self.actions_name_map = {
            "shot": Actions.shot,
        }
        self.round = {"blank": 0, "bang": 1}
        self.shell = [
            random.choice(["blank", "bang"]) for _ in range(random.randint(6, 12))
        ]

    @property
    def healths(self):
        return self._healths

    @healths.setter
    def healths(self, new_healths):
        return self._healths == new_healths

    def get_user_input(self):
        print("pleas whrite in camelcase")
        action = input(
            "Dealer: do you what to shot or a item? (write the name of the item you want to use)"
        )

        self.actions_name_map[action](self)

    def count_bullets(self):
        bullets = 0
        blank = 0
        for i in self.shell:
            if i == "bang":
                bullets += 1
            else:
                blank += 1

        print(f" totale {bullets+blank}, bullets: {bullets}, blank: {blank}")

    def steps(self):
        self.count_bullets()
        for self.i, self.bullet in enumerate(self.shell):
            print("")
            print(self.healths)
            print("i =", self.i)
            print((len(self.shell) - self.i) % 2 == 0)
            if (len(self.shell) - self.i) % 2 == 0:
                dealer.steps(game)
            if not len(self.shell) % 2 == 0:  # or coin flip
                self.get_user_input()
            else:
                RuntimeError("ingen sin turn!")


game = Game()
actions = Actions()
dealer = Dealer()
game.steps()
