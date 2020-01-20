class SetRoundness:

    def __init__(self):
        self.values = []
        self.smallest = 10000000
        self.biggest = 0

    def add_value(self, new_val):
        self.values.append(new_val)

        if new_val > self.biggest:
            self.biggest = new_val

        if new_val < self.smallest:
            self.smallest = new_val

    def get_average(self):
        instances_num = len(self.values)

        sum_val = 0
        for r in self.values:
            sum_val += r

        return float(sum_val) / float(instances_num)