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

    def setNet(self, net):
        self.net = net

    def getAction(self, state):

        def invert(x, y):
            x = state.data.layout.width - x
            y = state.data.layout.height - y
            return int(x) - 1, int(y) - 1

        layout = []

        for row in range(state.data.layout.height):
            layout.append([])
        for col in layout:
            col += [0 for _ in range(state.data.layout.width)]

        x, y = state.getPacmanPosition()
        x, y = invert(x, y)

        layout[y][x] = 1

        for pos in state.getGhostPositions():
            x, y = pos
            x, y = invert(x, y)
            layout[y][x] = -10

        for pos in state.getCapsules():
            x, y = pos
            x, y = invert(x, y)
            layout[y][x] = 10

        food = state.getFood().data
        for i in range(len(food)):
            for j in range(len(food[0])):
                x, y = invert(i, j)
                if food[i][j]:
                    layout[y][x] = 5

        walls = state.getWalls().data
        for i in range(len(walls)):
            for j in range(len(walls[0])):
                x, y = invert(i, j)
                if walls[i][j]:
                    layout[y][x] = -5

        #for row in layout:
            #print(row)

        flat = []
        for row in layout:
            for item in row:
                flat.append(item)

        direction = state.getPacmanState().configuration.direction
        if direction == Directions.STOP:
            direction = Directions.NORTH

        if direction == Directions.NORTH:
            flat.append(20)
        elif direction == Directions.SOUTH:
            flat.append(40)
        elif direction == Directions.WEST:
            flat.append(-20)
        elif direction == Directions.EAST:
            flat.append(-40)
        output = self.net.activate(tuple(flat))

        legal = state.getLegalPacmanActions()

        if direction == Directions.NORTH:
            if output[0] > 0.5 and Directions.NORTH in legal:
                return Directions.NORTH
            if output[1] > 0.5 and Directions.SOUTH in legal:
                return Directions.SOUTH
            if output[2] > 0.5 and Directions.EAST in legal:
                return Directions.EAST
            if output[3] > 0.5 and Directions.WEST in legal:
                return Directions.WEST
            return Directions.STOP
        if direction == Directions.SOUTH:
            if output[0] > 0.5 and Directions.SOUTH in legal:
                return Directions.SOUTH
            if output[1] > 0.5 and Directions.NORTH in legal:
                return Directions.NORTH
            if output[2] > 0.5 and Directions.WEST in legal:
                return Directions.WEST
            if output[3] > 0.5 and Directions.EAST in legal:
                return Directions.EAST
            return Directions.STOP
        if direction == Directions.WEST:
            if output[0] > 0.5 and Directions.WEST in legal:
                return Directions.WEST
            if output[1] > 0.5 and Directions.EAST in legal:
                return Directions.EAST
            if output[2] > 0.5 and Directions.NORTH in legal:
                return Directions.NORTH
            if output[3] > 0.5 and Directions.SOUTH in legal:
                return Directions.SOUTH
            return Directions.STOP
        if direction == Directions.EAST:
            if output[0] > 0.5 and Directions.EAST in legal:
                return Directions.EAST
            if output[1] > 0.5 and Directions.WEST in legal:
                return Directions.WEST
            if output[2] > 0.5 and Directions.SOUTH in legal:
                return Directions.SOUTH
            if output[3] > 0.5 and Directions.NORTH in legal:
                return Directions.NORTH
            return Directions.STOP

#
