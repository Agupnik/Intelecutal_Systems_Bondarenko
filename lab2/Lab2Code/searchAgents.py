from random import randrange

from game import Directions
from game import Agent
from game import Actions
import search


# Загальний пошуковий агент, який знаходить шлях за допомогою наданого пошуку алгоритм для заданої проблеми пошуку,
# а потім повертає дії, щоб слідувати цьому шлях.
class SearchAgent(Agent):
    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        super().__init__()
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            self.searchFunction = lambda x: func(x, heuristic=heur)
        self.searchType = globals()[prob]

    # Це перший випадок, коли агент бачить макет ігрового поля. Тут ми обираємо шлях до мети.
    # На цьому етапі агент повинен обчислити шлях до мети та зберегти його у локальній змінній.
    def registerInitialState(self, state):
        problem = self.searchType(state)  # Makes a new search problem
        self.actions = self.searchFunction(problem)  # Find a path
        if '_expanded' in dir(problem): print('Розширено пошукових вузлів: %d' % problem._expanded)

    # Повертає наступну дію на шляху, обраному раніше.
    def getAction(self, state):
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


def manhattan(node_x, goal_x, node_y, goal_y):
    return abs(node_x - goal_x) + abs(node_y - goal_y)


def euclidean(node_x, goal_x, node_y, goal_y):
    return ((node_x - goal_x) ** 2 + (node_y - goal_y) ** 2) ** 0.5


def euclideanSquared(node_x, goal_x, node_y, goal_y):
    return (node_x - goal_x) ** 2 + (node_y - goal_y) ** 2


def manhattanHeuristic(position, problem):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return manhattan(xy1[0], xy2[0], xy1[1], xy2[1])


def euclideanHeuristic(position, problem):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return euclidean(xy1[0], xy2[0], xy1[1], xy2[1])
    # return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


def euclideanHeuristicSquared(position, problem):
    "The Euclidean Squared distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return euclidean(xy1[0], xy2[0], xy1[1], xy2[1])


def cornersManhattanHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    if len(state[1]) == 0:
        return 0

    val = []

    for s in state[1]:
        val.append(manhattan(s[0], state[0][0], s[1], state[0][1]))
        # val.append(abs(s[0] - state[0][0]) + abs(s[1] - state[0][1]))

    return max(val)


def cornersEuclideanHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    if len(state[1]) == 0:
        return 0

    val = []

    for s in state[1]:
        val.append(euclidean(s[0], state[0][0], s[1], state[0][1]))
        # val.append(((s[0] - state[0][0]) ** 2 + (s[1] - state[0][1]) ** 2) ** 0.5)

    return max(val)


def cornersEuclideanSquaredHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    if len(state[1]) == 0:
        return 0

    val = []

    for s in state[1]:
        val.append(euclideanSquared(s[0], state[0][0], s[1], state[0][1]))
        # val.append((s[0] - state[0][0]) ** 2 + (s[1] - state[0][1]) ** 2)

    return max(val)


# PLEASE, WRITE ANOTHER HEURISTICS
def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state

    food = foodGrid.asList()

    if len(food) == 0:
        return 0

    val = []
    for s in food:
        val.append(manhattan(s[0], state[0][0], s[1], state[0][1]))

    return max(val)


# Проблема пошуку визначає простір стану, стартовий стан, перевірку мети, функцію наступника та функцію витрат.
class PositionSearchProblem(search.SearchProblem):
    def __init__(self, gameState, costFn=lambda x: randrange(11), goal=(1, 1), start=None, warn=True, visualize=True):
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start is not None:
            self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    # Повертає стартову позицію Pac-man.
    def getStartState(self):
        return self.startState

    # Повертає булеве значення, яке характеризує, чи буде досягнута перемога, при переході у деякий стан.
    def isGoalState(self, state):
        isGoal = state == self.goal
        return isGoal

    # Повертає можливі наступні стани для Pac-man.
    def getSuccessors(self, state):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        self._expanded += 1  # DO NOT CHANGE

        return successors


class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.
    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        return (self.startingPosition, self.corners)

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        return len(state[1]) == 0

    def getSuccessors(self, state):

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)

            if not self.walls[nextx][nexty]:
                corners = tuple(x for x in state[1] if x != (nextx, nexty))
                successors.append((((nextx, nexty), corners), action, 1))

        self._expanded += 1  # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        """
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
        return len(actions)


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}  # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1  # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions."""
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            cost += 1
        return cost
