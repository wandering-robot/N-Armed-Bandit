from random import randrange, random

class Agent:
    epsilon = 0.2      #used for greedy methods (class method b/c need to change it for epsilon trial)
    def __init__(self, machine):
        self.score = 0
        self.pulls = 0
        self.avg_score = 0
        self.memory = []

        self.machine = machine
    
        self.pull_freq = [0 for _ in range(len(self.machine.arms))]
        self.action_values = [0 for _ in range(len(self.machine.arms))]

        # self.epsilon = 0.2      #used for greedy methods

    def __repr__(self):     #used to make function name on graph look nice
        return 'Agent'

    def reset(self):        #creates a new agent for a new attempt
        self.__init__(self.machine)

    def get_reward(self,reward):    #updates the agent's score and adds it to the memory of scores recieved
        self.score += reward
        self.memory.append(self.score)

    def pull_arm(self,arm_id):      #pulls on/activates an arm
        value = self.machine.arms[arm_id].pull()
        self.pulls += 1
        self.get_reward(value)
        return value

    def update_avg_score(self,value):
        self.avg_score = self.avg_score + (value-self.avg_score)/self.pulls

    def update_action_value(self,arm_id,value):
        self.pull_freq[arm_id] += 1
        self.action_values[arm_id] = self.action_values[arm_id] +(value-self.action_values[arm_id])/self.pull_freq[arm_id]

    def find_greedy_action(self):
        max_val = max(self.action_values)
        max_ind = self.action_values.index(max_val)
        return max_ind

    #incremental implementaion for updating action-values
    def pull_and_update(self,arm_id):           #uses pull arm, but additionally updates all the memory banks for the agent 
        value = self.pull_arm(arm_id)
        self.update_avg_score(value)
        self.update_action_value(arm_id, value)

    def pull_arm_greedily(self, num_of_times):
        for _ in range(num_of_times):
            if random() > self.epsilon:
                arm_id = self.find_greedy_action()
            else:
                arm_id = self.random_arm_id()
            self.pull_and_update(arm_id)
       
    #section of code for choosing arms at random with no strategy
    def pull_arm_randomly(self,num_of_times):
        for _ in range(num_of_times):
            arm_id = self.random_arm_id()
            self.pull_and_update(arm_id)

    def random_arm_id(self):
        arm_id = randrange(len(self.machine.arms))
        return arm_id




