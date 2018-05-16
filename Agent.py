import random as ran
import Model
import LiveObject
from Action import Action

class Agent:

    def action(self, model, lo):
        return ran.randint(0, Action.NUM_OF_AVAIL_ACTIONS)



