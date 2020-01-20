import numpy as np


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

    def get_mean(self):
        instances_num = len(self.values)

        sum_val = 0
        for r in self.values:
            sum_val += r

        return float(sum_val) / float(instances_num)

    def get_variance(self):
        mean = self.get_mean()

        sum = 0
        for val in self.values:
            sum += (val - mean) ** 2

        return sum / len(self.values)

    def get_prob(self, some_val):
        variance = self.get_variance()
        mean = self.get_mean()

        first = 1 / (np.sqrt(2 * 3.14159 * variance))
        second = np.exp(-1 * ((some_val - mean) ** 2) / (2 * variance))

        return first * second

    def get_average_without_outliers(self):
        self.values.sort()
        instances_num = len(self.values)

        sum_val = 0
        for i in range(1, instances_num - 1):
            sum_val += self.values[i]

        return float(sum_val) / float(instances_num)