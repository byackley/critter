class DScript:
  def __init__(self, fn):
    self.states = {} # map of state name to (instructions, transitions)
    
