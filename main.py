from slot_machine import Machine
from agent import Agent

from random import randint
from matplotlib import pyplot as plt
import os.path
import pathlib

class Main:
    def __init__(self):
        self.arm_num = 50
        self.machine = Machine(self.arm_num)
        self.agent = Agent(self.machine)
        self.used_arms = []         #used to reference which arms were actually used in gradient method

    @staticmethod
    def get_path(file_name):
        abs_path = pathlib.Path(__file__).parent.absolute()
        complete_name = os.path.join(abs_path,'records',file_name+'.png')
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
            method_str = self.method2str(method)
            plt.plot(self.agent.memory,label=method_str[15:]) 

    def epsilon_trial(self,iter=False,trials=1,tote_pulls=200):
        if iter == True:
            main.agent.epsilon = 0
            while main.agent.epsilon < 1:
                main.trial(main.agent.pull_arm_greedily,trials,tote_pulls)
                print(f'Eps={main.agent.epsilon:.2f} -> {main.agent.score:.0f}')
                main.agent.epsilon += 0.05
        else:
            main.trial(main.agent.pull_arm_greedily,trials,tote_pulls)
            print(f'Eps={main.agent.epsilon:.2f} -> {main.agent.score:.0f}')

    def random_trial(self,trials=1,tote_pulls=200):
        for _ in range(trials):
            main.trial(main.agent.pull_arm_randomly,trials,tote_pulls)
            print(f'Random Walk -> {main.agent.score:.0f}')

    def gradient_trial(self,learning_rate=None,iter=False,trials=1,tote_pulls=200):
        rate = 0.1
        if iter:
            while rate < learning_rate:
                self.agent.time_step = rate
                for _ in range(trials):
                    main.trial(main.agent.pull_arm_gradiently,trials,tote_pulls)
                    print(f'Gradient rate {self.agent.time_step}-> {main.agent.score:.0f}')
                rate += 0.1
        
        elif learning_rate != None:
            main.agent.learning_rate = learning_rate
            main.trial(main.agent.pull_arm_gradiently,trials,tote_pulls)
            print(f'Gradient rate {self.agent.time_step}-> {main.agent.score:.0f}')
        else:
            main.trial(main.agent.pull_arm_gradiently,trials,tote_pulls)
            print(f'Gradient rate {self.agent.time_step}-> {main.agent.score:.0f}')

    def compare_graph(self,tote_pulls):
        plt.clf()
        self.random_trial(tote_pulls=tote_pulls)
        self.epsilon_trial(tote_pulls=tote_pulls)
        self.gradient_trial(tote_pulls=tote_pulls)
        plt.legend()
        plt.suptitle('N Armed Bandit Methods')
        plt.savefig(main.get_path('n_armed_bandit_methods'))

    def preference_graph(self):
        plt.clf()
        for i in range(len(self.agent.probs_mem)):
            flag = False        #use flags to only plot the arms that have non negligable probablities
            for j in self.agent.probs_mem[i]:
                if j > 1/(0.9*len(self.agent.probs_mem)):
                    flag = True
                    self.used_arms.append(self.machine.arms[i])
                    break
            if flag:
                plt.plot(self.agent.probs_mem[i],label=f'Arm {i}')
        plt.legend()
        plt.suptitle('Arm Preferences')
        plt.savefig(main.get_path('arm_preferences'))

if __name__ == "__main__":
    main = Main()
    main.compare_graph(100)
    main.preference_graph()
    for arm in main.used_arms:
        print(arm)


