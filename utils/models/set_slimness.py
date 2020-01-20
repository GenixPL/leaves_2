class SetSlimness:

    # while check if a given img fts those ratios we have to add some margin for error

    def __init__(self):
        self.ratios = []
        self.smallest_ratio = 100
        self.biggest_ratio = 0


    def add_value(self, new_ratio):
        self.ratios.append(new_ratio)

        if new_ratio > self.biggest_ratio:
            self.biggest_ratio = new_ratio

        if new_ratio < self.smallest_ratio:
            self.smallest_ratio = new_ratio