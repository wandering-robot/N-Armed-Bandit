from slot_machine import Machine
from agent import Agent

from random import randint
from matplotlib import pyplot as plt
import os.path

class Main:
    def __init__(self):
        self.arm_num = 10
        self.machine = Machine(self.arm_num)
        self.agent = Agent(self.machine)

    @staticmethod
    def get_path(file_name):
        save_path = r'C:\Users\ejbra\Desktop\N-Armed-Bandit\records'
        complete_name = os.path.join(save_path,file_name+'.png')
        return complete_name

    @staticmethod
    def method2str(method):
        method_str = str(method)
        method_list = method_str.split(' ')
        return method_list[2]

    def trial(self,method,num_iter,num_pull_per_iter):
        for _ in range(num_iter):
            self.agent.reset()
            method(num_pull_per_iter)
            plt.plot(self.agent.memory)
            method_str = self.method2str(method)

            if method_str[15:] == 'randomly':           #to create the graphs and file names for different methods
                plt.suptitle(f'{method_str}')
                plt.savefig(self.get_path(f'{method_str}'))
            elif method_str[15:] == 'greedily':
                plt.suptitle(f'{method_str} with epsilon = {main.agent.epsilon:.2f}')
                plt.savefig(self.get_path(f'{method_str}_{main.agent.epsilon:.2f}'))

    def epsilon_trial(self):
        main.agent.epsilon = 0
        while main.agent.epsilon < 1:
            main.trial(main.agent.pull_arm_greedily,1,200)
            print(f'Eps={main.agent.epsilon:.2f} -> {main.agent.score:.0f}')
            main.agent.epsilon += 0.1

    def random_trial(self,trials=1):
        for _ in range(trials):
            main.trial(main.agent.pull_arm_randomly,trials,200)

if __name__ == "__main__":
    main = Main()
    main.random_trial()
    main.epsilon_trial()



