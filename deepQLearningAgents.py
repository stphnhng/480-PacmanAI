from pacman import Directions
from game import Agent
import random
import game
import util

"""
    Deep Q Learning Agent
"""
class DeepQAgent(Agent):
    

    # Called First
    def registerInitialState(self, state):
        print("Calling RegisterInitialState")

    # Called Second (First in loop)
    # Requries a return of state?
    def observationFunction(self, state):
        """
            This is where we ended up after our last action.
            The simulation should somehow ensure this is called
        """
        print("Calling ObservationFunction")
        return state 

    # Called Third (Second in loop)
    # Requires a return of direction
    def getAction(self, state):
        # hash(state)


        print(hash(state))
        print(type(state))
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP:
            current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal:
            return left
        if current in legal:
            return current
        if Directions.RIGHT[current] in legal:
            return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal:
            return Directions.LEFT[left]
        return Directions.STOP
