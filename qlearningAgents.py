# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        "*** YOUR CODE HERE ***"
        self.Q_VALUES = {}

    # state = GameState in pacman.py
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if (state, action) not in self.Q_VALUES:
          self.Q_VALUES[(state,action)] = 0.0
          return 0.0
        else:
          return self.Q_VALUES[(state,action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        max_q = 0.0
        for action in self.getLegalActions(state):
          curr_q = self.getQValue(state, action)
          if curr_q >= max_q:
            max_q = curr_q
        return max_q

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        max_q = 0.0
        max_action = None
        if len(self.getLegalActions(state)) != 0:
          max_action = random.choice(self.getLegalActions(state)) # in case of negative q
        # print("legal actions:", self.getLegalActions(state))
        for action in self.getLegalActions(state):
          curr_q = self.getQValue(state, action)
          # print("max [", max_q, "] Q value for ", action, " is ", curr_q)
          if curr_q >= max_q:
            max_q = curr_q
            max_action = action
        return max_action

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        "*** YOUR CODE HERE ***"
        # if not self.epsilon:
        #   util.raiseNotDefined() # no epislon defined
        if util.flipCoin(self.epsilon): # epsilon greedy with some probability
          return random.choice(legalActions)
        else:
          return self.computeActionFromQValues(state)

    
    def getMaxQFuture(self, nextState):
      future_max_q = max(
        [
          self.getQValue(nextState, action_new) for 
          action_new in self.getLegalActions(nextState)
        ]
      )
      return future_max_q

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        """
          source: https://en.wikipedia.org/wiki/Q-learning
          Q-Value update function: 
              Q_new = Q(s,a) + ( alpha * [ Reward_action + gamma * maxQ_new - Q(s,a) ] )
          =
              Q_new = [ (1-alpha) * Q(s,a)] + [alpha * reward] + [alpha * gamma * maxQ_new]
        """
        # if not self.alpha:
        #   util.raiseNotDefined()
        if not self.discount:
          util.raiseNotDefined()
        if len(self.getLegalActions(nextState)) == 0:
          future_max_q = 0.0
        else:
          future_max_q = self.getMaxQFuture(nextState)

        sum_1 = (1 - self.alpha) * self.getQValue(state, action)
        sum_2 = self.alpha * reward
        sum_3 = self.alpha * self.discount * future_max_q

        # print("last action:", self.lastAction)
        self.Q_VALUES[(state, action)] = sum_1 + sum_2 + sum_3
        # print("Updating q value to: ", sum_1, " + ", sum_2, " + ", sum_3, " = ", self.Q_VALUES[(state,action)])
        # print(self.Q_VALUES)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='SimpleExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()



    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"

        final_q = 0
        features = self.featExtractor.getFeatures(state, action)
        for feature in features:
          final_q += features[feature] * self.weights[feature]
        return final_q

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
          
        """
          Update weights via.:
              w_i = w_i + alpha * difference * feature[i]
          difference:
              difference = [reward + gamma * maxQ_new] - Q(s,a)
        """
        for feature in features:
            difference = 0

            if len(self.getLegalActions(nextState)) == 0:
                difference = reward - self.getQValue(state, action)
            else:
                difference = (reward + self.discount * self.getMaxQFuture(nextState) ) - self.getQValue(state, action)

            sum_2 = self.alpha * difference * features[feature]
            self.weights[feature] = self.weights[feature] + sum_2

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
