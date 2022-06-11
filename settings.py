class Settings():
    def __init__(self):

        # point cell
        self.points_per_default_cell = 10
        self.points_per_gray_cell = 66
        self.multiplier = 1.8

        # information table_data
        self.score = 0
        self.longest_chain = 0
        self.high_score = 0
        with open('cookie.txt', 'r') as cookie:
            self.high_score = cookie.read().split(':')[-1].strip()

        self.lvl = 1
        self.step_to_next_lvl = 30

        self.music = True

        self.flag = False
