from ceEntity import CEEntity

class CEWorld(CEEntity):
  def __init__(self):
      super(CEWorld, self).__init__()
      self.sprites = []
      self.stage = None

  def update(self, mils):
      for sprite in self.sprites:
          sprite.update(mils)
      if self.stage:
          self.stage.update(mils)
