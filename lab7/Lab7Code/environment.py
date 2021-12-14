import util


class Environment:

    def getCurrentState(self):
        """
        Returns the current state of enviornment
        """
        util.raiseNotDefined()

    def getPossibleActions(self, state):
        """
          Returns possible actions the agent
          can take in the given state. Can
          return the empty list if we are in
          a terminal state.
        """
        util.raiseNotDefined()

    def doAction(self, action):
        """
          Performs the given action in the current
          environment state and updates the enviornment.

          Returns a (reward, nextState) pair
        """
        util.raiseNotDefined()

    def reset(self):
        """
          Resets the current state to the start state
        """
        util.raiseNotDefined()

    def isTerminal(self):
        """
          Has the enviornment entered a terminal
          state? This means there are no successors
        """
        state = self.getCurrentState()
        actions = self.getPossibleActions(state)
        return len(actions) == 0
