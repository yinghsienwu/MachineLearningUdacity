import random
import numpy as np
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        #self.next_waypoint=None
        self.actions=[None, 'forward','left','right']
        self.learning_rate=0.3
        self.state=None
        self.trips=0
        self.q={}
        

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.trips+=1
        if self.trips>=100:
            self.learning_rate=0

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        state = (inputs['light'],inputs['oncoming'],inputs['right'],inputs['left'],self.next_waypoint)
        self.state=state

        # TODO: Select action according to your policy
        
        # update rule


        # Lazy initialization of Q-values
        for action in self.actions:
            if (state,action) not in self.q:
                self.q[(state,action)]=1
        # Select action according to the policy
        prob=[self.q[(state,None)],self.q[(state,'forward')],self.q[(state,'left')],self.q[(state,'right')]]
        # Use the softmax function 
        prob=np.exp(prob)/np.sum(np.exp(prob),axis=0)
        if random.random()< max((100-self.trips)/100,0):
            action=np.random.choice(self.actions,p=prob)
        else:
            action=self.actions[np.argmax(prob)]

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.q[(state,action)]=self.learning_rate*reward+(1-self.learning_rate)*self.q[(state,action)]
       # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.2, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
