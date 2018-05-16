
class Agent:
    @staticmethod
    def action(percept):
        return percept.get_direction()