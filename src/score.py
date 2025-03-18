class ScoreManager:
    def __init__(self):
        self.score = 1000

    def add_bonus(self, bonus):

        self.score += bonus

    def deduct_penalty(self, penalty):
        self.score -= penalty

    def get_score(self):
        return self.score
