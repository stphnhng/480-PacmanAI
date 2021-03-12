# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
import random
import game
import util


class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
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


class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action)
                      for action in legal]
        scored = [(self.evaluationFunction(state), action)
                  for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)


def scoreEvaluation(state):
    return state.getScore()

class NEAT_Agent(Agent):
    OFFSET = 4

    def setGenome(self, genome):
        self.genome = genome

    def setNet(self, net):
        self.net = net

    def printGrid(self, grid):
        for i, item in enumerate(grid):
            if i % (self.OFFSET * 2 + 1) == 0:
                print("")
            if item == 0:
                print(" ", end=" ")
            elif item == .5:
                print("O", end=" ")
            elif item == 1:
                print(".", end=" ")
            elif item == -.5:
                print("#", end=" ")
            elif item == -1:
                print("G", end=" ")
        print("")

    def invertY(self, state, y):
        return state.data.layout.height - y

    def headingNorth(self, state):
        grid = []

        pac_x, pac_y = state.getPacmanPosition()
        ghosts = state.getGhostPositions()
        capsules = state.getCapsules()

        for y in reversed(range(pac_y - self.OFFSET, pac_y + self.OFFSET + 1)):
            for x in range(pac_x - self.OFFSET, pac_x + self.OFFSET + 1):
                if y < 0:
                    grid.append(-1)
                elif y >= state.data.layout.height:
                    grid.append(-1)
                elif x < 0:
                    grid.append(-1)
                elif x >= state.data.layout.width:
                    grid.append(-1)
                else:
                    if state.hasWall(x, y):
                        grid.append(-1)
                    elif (x, y) in ghosts:
                        grid.append(-.5)
                    elif state.hasFood(x, y):
                        grid.append(1)
                    else:
                        grid.append(0)

        #self.printGrid(grid)
        return grid

    def headingSouth(self, state):
        grid = []

        pac_x, pac_y = state.getPacmanPosition()
        ghosts = state.getGhostPositions()
        capsules = state.getCapsules()

        for y in range(pac_y - self.OFFSET, pac_y + self.OFFSET + 1):
            for x in reversed(range(pac_x - self.OFFSET, pac_x + self.OFFSET + 1)):
                if y < 0:
                    grid.append(-1)
                elif y >= state.data.layout.height:
                    grid.append(-1)
                elif x < 0:
                    grid.append(-1)
                elif x >= state.data.layout.width:
                    grid.append(-1)
                else:
                    if state.hasWall(x, y):
                        grid.append(-1)
                    elif (x, y) in ghosts:
                        grid.append(-.5)
                    elif state.hasFood(x, y):
                        grid.append(1)
                    else:
                        grid.append(0)

        #self.printGrid(grid)
        return grid

    def headingWest(self, state):
        grid = []

        pac_x, pac_y = state.getPacmanPosition()
        ghosts = state.getGhostPositions()
        capsules = state.getCapsules()

        for x in range(pac_x - self.OFFSET, pac_x + self.OFFSET + 1):
            for y in range(pac_y - self.OFFSET, pac_y + self.OFFSET + 1):
                if y < 0:
                    grid.append(-1)
                elif y >= state.data.layout.height:
                    grid.append(-1)
                elif x < 0:
                    grid.append(-1)
                elif x >= state.data.layout.width:
                    grid.append(-1)
                else:
                    if state.hasWall(x, y):
                        grid.append(-1)
                    elif (x, y) in ghosts:
                        grid.append(-.5)
                    elif state.hasFood(x, y):
                        grid.append(1)
                    else:
                        grid.append(0)

        #self.printGrid(grid)
        return grid

    def headingEast(self, state):
        grid = []

        pac_x, pac_y = state.getPacmanPosition()
        ghosts = state.getGhostPositions()
        capsules = state.getCapsules()

        for x in reversed(range(pac_x - self.OFFSET, pac_x + self.OFFSET + 1)):
            for y in reversed(range(pac_y - self.OFFSET, pac_y + self.OFFSET + 1)):
                if y < 0:
                    grid.append(-1)
                elif y >= state.data.layout.height:
                    grid.append(-1)
                elif x < 0:
                    grid.append(-1)
                elif x >= state.data.layout.width:
                    grid.append(-1)
                else:
                    if state.hasWall(x, y):
                        grid.append(-1)
                    elif (x, y) in ghosts:
                        grid.append(-.5)
                    elif state.hasFood(x, y):
                        grid.append(1)
                    else:
                        grid.append(0)

        #self.printGrid(grid)
        return grid

    def getAction(self, state):

        inputs = []

        direction = state.getPacmanState().getDirection()
        if direction is Directions.NORTH or direction is Directions.STOP:
            inputs = self.headingNorth(state)
        elif direction is Directions.SOUTH:
            inputs = self.headingSouth(state)
        elif direction is Directions.EAST:
            inputs = self.headingEast(state)
        elif direction is Directions.WEST:
            inputs = self.headingWest(state)

        output = self.net.activate(inputs)
        max = 0
        for i in range(len(output)):
            if output[i] > output[max]:
                max = i

        legal = state.getLegalPacmanActions()

        """
        if max == 0:
            print("forward")
        elif max == 1:
            print("back")
        elif max == 2:
            print("right")
        elif max == 3:
            print("left")
        """

        if direction is Directions.NORTH or direction is Directions.STOP:
            if max == 0 and Directions.NORTH in legal:
                #self.genome.fitness += .2
                return Directions.NORTH
            elif max == 1 and Directions.SOUTH in legal:
                #self.genome.fitness += .2
                return Directions.SOUTH
            elif max == 2 and Directions.EAST in legal:
                #self.genome.fitness += .2
                return Directions.EAST
            elif max == 3 and Directions.WEST in legal:
                #self.genome.fitness += .2
                return Directions.WEST
        elif direction is Directions.SOUTH:
            if max == 0 and Directions.SOUTH in legal:
                return Directions.SOUTH
            elif max == 1 and Directions.NORTH in legal:
                return Directions.NORTH
            elif max == 2 and Directions.WEST in legal:
                return Directions.WEST
            elif max == 3 and Directions.EAST in legal:
                return Directions.EAST
        elif direction is Directions.WEST:
            if max == 0 and Directions.WEST in legal:
                return Directions.WEST
            elif max == 1 and Directions.EAST in legal:
                return Directions.EAST
            elif max == 2 and Directions.NORTH in legal:
                return Directions.NORTH
            elif max == 3 and Directions.SOUTH in legal:
                return Directions.SOUTH
        elif direction is Directions.EAST:
            if max == 0 and Directions.EAST in legal:
                return Directions.EAST
            elif max == 1 and Directions.WEST in legal:
                return Directions.WEST
            elif max == 2 and Directions.SOUTH in legal:
                return Directions.SOUTH
            elif max == 3 and Directions.NORTH in legal:
                return Directions.NORTH

        #self.genome.fitness -= .5
        return Directions.STOP
#
