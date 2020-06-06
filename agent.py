from random import randrange, random
import math as m
from numpy.random import choice

class Agent:

    def __init__(self, machine,epsilon=0.15,opt_val=0,time_step=0.6):
        self.score = 0
        self.pulls = 0
        self.avg_reward = 0
        self.memory = []

        self.machine = machine
        self.epsilon = epsilon          #used for greedy methods (class method b/c need to change it for epsilon trial)
        self.opt_value = opt_val        #used for optomistic initial value approach
        self.time_step = time_step      #used for gradient bandit approach
    
        self.pull_freq = [0 for _ in range(len(self.machine.arms))]
        self.action_values = [self.opt_value for _ in range(len(self.machine.arms))]

        self.prefs = [0 for _ in range(len(self.machine.arms))]
        self.probs = [1/len(self.machine.arms) for _ in range(len(self.machine.arms))]

        self.probs_mem = [[] for _ in range(len(self.machine.arms))]


    def __repr__(self):     #used to make function name on graph look nice
        return 'Agent'

    def reset(self):        #creates a new agent for a new attempt
        self.__init__(self.machine)

    def get_reward(self,reward):    #updates the agent's score and adds it to the memory of scores recieved
        self.score += reward
        self.memory.append(self.score)

    def pull_arm(self,arm_id):      #pulls on/activates an arm -> updates pulls and activates reward function
        value = self.machine.arms[arm_id].pull()
        self.pulls += 1
        self.get_reward(value)
        return value

    def update_avg_reward(self,value):       #updates the agent's average score variable
        self.avg_reward = self.avg_reward + (value-self.avg_reward)/self.pulls

    def update_action_value(self,arm_id,value): #updates pull frequency rates and action values
        self.pull_freq[arm_id] += 1
        self.action_values[arm_id] = self.action_values[arm_id] +(value-self.action_values[arm_id])/self.pull_freq[arm_id]

    def find_greedy_action(self):       #iterates through the actions to determine the greedy one
        max_val = max(self.action_values)
        max_ind = self.action_values.index(max_val)
        return max_ind

    def probability_calc(self):     #iterates through and updates all probabilities based on the current preference
        e_sum  = 0
        for pref in self.prefs:
            e_sum += m.exp(pref)
        for ind in range(len(self.machine.arms)):
            self.probs[ind] = m.exp(self.prefs[ind])/e_sum

    def preference_calc(self,arm_id,reward):        #iterates through and updates all the preferences based on the current action and reward value
        for ind in range(len(self.prefs)):
            if ind == arm_id:
                self.prefs[ind] = self.prefs[ind] + self.time_step*(reward-self.avg_reward)*(1-self.probs[ind])
            else:
                self.prefs[ind] = self.prefs[ind] - self.time_step*(reward-self.avg_reward)*(self.probs[ind])
        
    def archive(self):      #to graph the changes in arm preference over time
        for ind in range(len(self.probs)):
            self.probs_mem[ind].append(self.probs[ind])

    #incremental implementaion for updating action-values
    def pull_and_update(self,arm_id):           #uses pull arm, but additionally updates all the memory banks for the agent 
        value = self.pull_arm(arm_id)
        self.update_avg_reward(value)
        self.update_action_value(arm_id, value)
        return value

    #section of code for using epsilon to make greedy choices
    def pull_arm_greedily(self, num_of_times):
        for _ in range(num_of_times):
            greedy_arm_id = self.find_greedy_action()
            if random() > self.epsilon:
                arm_id = greedy_arm_id
            else:
                arm_id = self.random_arm_id()
                while arm_id == greedy_arm_id:
                    arm_id = self.random_arm_id()
            self.pull_and_update(arm_id)
    
    #dummy method call to make the graphs look nice and not save over one another
    def pull_arm_optomistically(self,num_of_times):
        self.pull_arm_greedily(num_of_times)

    #section of code for using gradient bandit method
    def pull_arm_gradiently(self, num_of_times):
        ind_arr = [i for i in range(len(self.machine.arms))]
        for _ in range(num_of_times):
            self.archive()          #to graph changes in preferences
            if random() < self.epsilon:
                arm_id = self.random_arm_id()
            else:
                arm_id = choice(ind_arr,p=self.probs)
            value = self.pull_and_update(arm_id)
            self.preference_calc(arm_id,value)
            self.probability_calc()

    #section of code for choosing arms at random with no strategy
    def pull_arm_randomly(self,num_of_times):
        for _ in range(num_of_times):
            arm_id = self.random_arm_id()
            self.pull_and_update(arm_id)

    def random_arm_id(self):
        arm_id = randrange(len(self.machine.arms))
        return arm_id




