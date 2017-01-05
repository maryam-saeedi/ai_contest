# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveDummyAgent', second = 'DefensiveDummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """


  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)


  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start, pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    myself = self.getSuccessor(gameState, Directions.STOP)
    a= myself.getAgentState(self.index).numCarrying
    print "carrying ", a
    threshold = 5

    if a > threshold:
      if self.red:
        nextMove = gameState.getLegalActions
        print nextMove
        if Directions.WEST in nextMove:
          return Directions.WEST
        if Directions.NORTH in nextMove:
          return Directions.NORTH
        if Directions.SOUTH in nextMove:
          return Directions.SOUTH
        if Directions.EAST in nextMove:
          return Directions.EAST

    return random.choice(bestActions)

  def scape(self, gameState, ):
    actions = gameState.getLegalActions(self.index)
    values = [self.abort(gameState, a) for a in actions]

    return

  def abort(self, gameState, action, enemy):

    return

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features


  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveDummyAgent(DummyAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    features['successorScore'] = -len(foodList)#self.getScore(successor)
    myPos = successor.getAgentState(self.index).getPosition()

    # Computes distance to invaders we can see. it must be negative
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if not a.isPacman and a.getPosition()  != None]
    # features['numInvaders'] = len(invaders)
    # TODO: serveral enemies!
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
      print "me to enemy %d" , features['invaderDistance']




    # Compute distance to the nearest food
    # minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])

    if len(invaders) > 0:
        enemy = [a for a in enemies if not a.isPacman and a.getPosition() != None and self.getMazeDistance(myPos, a.getPosition()) == min(dists)]

    tmpValue = -9999
    for food in foodList:
        # distance to us
        tmpToMe = self.getMazeDistance(myPos, food)
        # distance to enemy
        if len(invaders) > 0 and len(enemy) > 0:
            tmpToEnemy = self.getMazeDistance(myPos, enemy.__getitem__(0).getPosition())
            print "enemy pos ", enemy.__getitem__(0).getPosition()
        else:
            tmpToEnemy = 0
        # -1 to us && 1 to enemy and use max of them
        if tmpToEnemy - tmpToMe > tmpValue:
            print " food to enemy : %d\n", tmpToEnemy
            # print " food to me : %d\n", tmpToMe
            # print "bye"
            tmpValue = tmpToEnemy - tmpToMe
            bestFood = food

    # raw_input("pause")
    features['foodEvaluation'] = tmpValue

    # compute distance between food and enemies
    # tmpDistance = 9999
    # enemy = enemies.__getitem__(0)
    # for e in enemies:
    #     if self.getMazeDistance(myPos, e)<tmpDistance:
    #         tmpDistance = self.getMazeDistance(myPos, e.getPosition())
    #         enemy = e

    # probably useless !
    # tmpDistance = 9999
    # for f in foodList:
    #     if self.getMazeDistance(myPos, f)<tmpDistance:
    #         tmpDistance=self.getMazeDistance(myPos, f)
    #         food = f
    # food = [f for f in foodList if self.getMazeDistance(enemy[0].getPosition(), f.getPosition())==minDistance]
    # if enemy.__len__() > 0:
    #     print "hiiii"
    #     features['foodToEnemyDistance'] = self.getMazeDistance(enemy.__getitem__(0).getPosition(), food)
    #     a = raw_input("pause")
    #     print " food to enemy : %d\n" ,features['foodToEnemyDistance']
    #     print " enemy : %d\n", features['invaderDistance']
    #     print " food : %d\n", features['distanceToFood']
    #     print "bye"

    # go to region that have more food than other
    # foodMatrix = self.getFood(gameState)
    # for f in foodList:
    #     if self.getMazeDistance(myPos, f)== minDistance:
    #         food = f
    #         break

    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'foodEvaluation': 1, 'invaderDistance': 1}

class DefensiveDummyAgent(DummyAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
