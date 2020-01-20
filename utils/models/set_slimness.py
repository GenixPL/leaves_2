class SetSlimness:

    # while check if a given img fts those ratios we have to add some margin for error

    def __init__(self):
        self.values = []
        self.smallest = 100
        self.biggest = 0


    def add_value(self, new_value):
        self.values.append(new_value)

        if new_value > self.biggest:
            self.biggest = new_value

        if new_value < self.smallest:
            self.smallest = new_value

    def get_average(self):
        instances_num = len(self.values)

        sum_val = 0
        for r in self.values:
            sum_val += r

        return float(sum_val) / float(instances_num)