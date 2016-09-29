import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.last_action=None
        ### Initialize q matrix
        self.q={}
        self.alpha=0.9    ###optimal learning rate~1
        self.epsilon=0.1  ###initial stoschasticity
        self.gamma=0.1   ###discount factor: too high, may diverge
        self.last_state=None
        self.state=None
        self.last_reward=None
        self.total_rewards=0

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.last_action=None
        self.state=None
        ###q-learning
        self.epsilon=0.
        self.total_rewards=0

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        
        # TODO: Update state  
        self.state=(self.env.sense(self)['light'],self.planner.next_waypoint(),self.env.sense(self)['oncoming'],self.env.sense(self)['left'])  ###tuple (traffic_light,next_waypoint,oncoming,left)

        # TODO: Select action according to your policy
        action=self.getAction(self.state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        if self.last_reward!=None:
            self.updateQmatrix(self.last_state,self.last_action,self.state,self.last_reward)
        
        self.last_action=action
        self.last_state=self.state
        self.last_reward=reward
        self.total_rewards+=reward
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


    def getAction(self,state):
        ###
        legalActions=[None,'forward','left','right']
        action=None
        if random.random()<self.epsilon: 
            action=random.choice(legalActions)
        else:
            action=self.getBestAction(state)
        return action

    def getBestAction(self,state):
        ### return the best possible action    
        legalActions=[None,'forward','left','right']
        Qmatrix=[self.get_q(state,action) for action in legalActions]
        bestAction=legalActions[np.argmax(Qmatrix)]
        #best_q=np.amax(Qmatrix)
        '''
        bestAction=None
        best_q=-999999
        for action in legalActions:
            if self.get_q(state,action)> best_q: 
                best_q=self.get_q(state,action)
                bestAction=action
            if self.get_q(state,action)==best_q: #50% probability to update the best action if q is the same
                if random.random()<0.5:
                    best_q=self.get_q(state,action)
                    bestAction=action
        '''
        return bestAction
            
    def get_q(self,state,action):
        ###input(state,action), output q value for the (state,action)
        return self.q.get((state,action),100.) 
        
    def updateQmatrix(self,state,action,next_state,reward):
        ###q-value update
        if (state,action) not in self.q:
            self.q[(state,action)]=100.
        else:  ### q-learning algorithm
            self.q[(state,action)]=self.q[(state,action)]+self.alpha*(reward+self.gamma*self.get_qmax(next_state)-self.q[(state,action)])
            '''the Bellman equation (for future reference)
            self.q[(state,action)]=(1.0-self.alpha)*self.q[(state,action)]+self.alpha*(reward+self.gamma*max(self.q[(next_state,next_action)] for next_action in self.actions))    ###if I know what are self.actions
            '''

    def get_qmax(self,state):
        ### return max_action Q(state,action) 
        legalActions=[None,'forward','left','right']
        best_q=-999999
        for action in legalActions:
            if self.get_q(state,action)>best_q:
                best_q=self.get_q(state,action)
        return best_q

    def get_decay_rate(t): ### Decay rate for epsilon
        ###http://stackoverflow.com/questions/22805872/optimal-epsilon-ϵ-greedy-value 
        ### reduce te chances of random exploration over time, as we can get the best of both exploration vs. exploitation
        return 1.0/float(t)


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.002, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
