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

    # Повертає наступну дію на шляху, обраному раніше.
    def getAction(self, state):
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


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

        return successors
