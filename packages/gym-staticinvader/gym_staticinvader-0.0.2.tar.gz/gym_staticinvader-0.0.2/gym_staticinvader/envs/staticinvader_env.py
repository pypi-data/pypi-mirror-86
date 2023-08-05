import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

# 7X5 grid
# We consider a transition function
# 4 = invaders, 1 = shot, 3 = shuttle, 7 = walls (identifiers)
# 1 left, 2 right, 3 shot (discrete actions)

class StaticinvaderEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    
    def __init__(self):
        self._init_state
        self._current_state
        self._set_init_space()
        self._current_state = np.copy(self._init_space)
      
    # set self._init_state:
    # There can be different initial states for each static invaders env, just to test
    # the policy iteration algorithm with different static enviroment settings. What doesn't change among intial states:
    # the first 3 rows are always with 3 invaders per row displayed on random columns
    # in the middle row there are 3 walls displayed randomly
    # in the last row central column there is our space ship
    def _set_init_space(self):
        self._init_state = np.zeros(7,5)
        idx1 = np.random.rand(3,5).argsort(1)[:,:3]
        self._init_state[np.arange(3,5)[:,None],idx1] = 4
        idx2 = np.random.rand(1,5).argsort(1)[:,:3]
        self._init_state[np.arange(3,7)[1],idx2] = 7
        self._init_state[6][2] = 3
  
  # give me a state and an action i will return a new state
    def _transition(self,current_state, action):
        new_state = np.copy(current_state)
      
        #update according to the shots
        for i in range(6):
            for j in range(5):
                if i == 0 and new_state[i][j] == 1:
                    new_state[i][j] = 0
                elif new_state[i][j] == 4 or new_state[i][j] == 7:
                    if new_state[i+1][j] == 1:
                        new_state[i][j] = 0
                        new_state[i+1][j] = 0
                elif new_state[i][j] == 0:
                    if new_state[i+1][j] == 1:
                      new_state[i+1][j] = 0
                      new_state[i][j] = 1
        idx = -1
        for i in range(5):
            if new_state[6][i] == 3:
                idx = i
                break
                
        if action == 1:#go to left
            new_state[6][idx] = 0
            new_state[6][max(0,idx-1)] = 3
      
        elif action == 2:#go to right
            new_state[6][idx] = 0
            new_state[6][min(4,idx+1)] = 3
      
        elif action == 3:#shot
            new_state[5][idx] = 1
        
        else:
            return current_state

        return new_state
    
    #uniform sampling actions
    def sample(self):
        r = np.random.rand()
        if r < 3.33:
            return 1
        elif r < 6.67:
            return 2
        return 3
       
    #returns 1 if we are in terminal state, 0 otherwise
    def is_terminal_state(current_state):
        if 4 in current_state:
            return 0
        return 1
       
   # returns a list of all possible states given the old state and an action
    def get_all_possible_new_states(self,old_state, action):
        return [self._transition(old_state,action)]
   
   # get the probability to get the "new state" from "old state and action" (transition function) 
    def get_probability_of_new_state(self,new_state,old_state,action):
        if(new_state == self._transition(old_state,action)).all():
            return 1
        return 0
       
  # compare old state and new state and i will give you the reward (difference of invaders)
    def get_reward(self,old_state,new_state):
        unique, counts = numpy.unique(old_state, return_counts=True)
        d1 = dict(zip(unique, counts))
      
        unique, counts = numpy.unique(new_state, return_counts=True)
        d2 = dict(zip(unique, counts))
      
        return d2[4]-d1[4]
        
    def step(self, action):
        old_state = self._current_state
        new_states = self.get_all_possible_new_states(old_state,action)
        l = []
        for i in new_states:
            l.append(self.get_probability_of_new_state(i,old_state,action))
        new_state = np.random.choice(new_states,p=l)
        self._current_state = new_state
        reward = self.get_reward(old_state,self._current_state)
        done = self.is_terminal_state(self._current_state)
        d = {}
        d['probability of being in this state given the old state and the action taken'] =  self.get_probability_of_new_state(self._current_state,old_state,action)
        return np.copy(self._current_state), reward, done, d
        
    def reset(self):
        self._current_state = np.copy(self._init_state)
    def render(self, mode='human'):
        for i in range(7):
            for i in range(5):
                print(str(self._current_state[i][j]) + " ")
            print("\n")
     
    def close(self):
        pass
