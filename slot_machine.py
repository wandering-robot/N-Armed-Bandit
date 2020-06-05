import numpy as np
from matplotlib import pyplot as plt
from random import randint

class Machine:
    def __init__(self, num_of_arms):
        self.num_of_arms = num_of_arms
        self.arms = [Arm(i) for i in range(self.num_of_arms)]

    def __repr__(self):
        return f'Machine: {self.num_of_arms}'

class Arm:
    def __init__(self,name):
        self.name = name
        self.mean = randint(0,9)
        self.std = randint(1,3)

    def __repr__(self):
        return f'Arm {self.name}:mean {self.mean}:std {self.std}'

    def id(self):
        return self.name

    def pull(self, num=1):
        return float(np.random.normal(self.mean, self.std, num))

if __name__ == "__main__":
    machine = Machine(10)
    print(machine)
