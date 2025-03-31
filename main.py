import random


class Dealer:
    def steps(self, bullet):
        print("dealer turn")
        if bullet == "blank":
            print("Dealer: I will shot my self")
            actions.shot()
        elif bullet == "bang":
            print("Dealer: I will shot you")
            actions.shot("you")


class Actions:
    def shot(self, who_to_hit="me"):
        print(game.round[game.bullet])
        if who_to_hit == "you":
            game.healths["player"] -= game.round[game.bullet]
        if who_to_hit == "me":
            game.healths["dealer"] -= game.round[game.bullet]


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
            random.choice(["blank", "bang"]) for _ in range(random.randint(3, 9))
        ]

    @property
    def healths(self):
        return self._healths

    @healths.setter
    def healths(self, new_healths):
        return self._healths == new_healths

    def get_user_input(self):
        action = input("Dealer: do you what to shot or a item?")
        if action.lower() == "shot":
            who_to_hit = input("Dealer: who do you want to shot you or me")
            self.actions_name_map[action](who_to_hit)

    def count_bullets(self):
        bullets = 0
        blank = 0
        for i in self.shell:
            if i == "bang":
                bullets += 1
            else:
                blank += 1

        print(f"bullets: {bullets}, blank: {blank}")

    def steps(self):
        while True:
            for self.bullet in self.shell:
                self.count_bullets()
                print(self.healths)
                dealer.steps(self.bullet)
                self.get_user_input()


game = Game()
actions = Actions()
dealer = Dealer()
game.steps()
