from ceEntity import CEEntity

class CEWorld(CEEntity):
  def __init__(self):
      super(CEWorld, self).__init__()
      self.sprites = []
      self.mode = None

  def update(self, mils):
      for sprite in self.sprites:
          sprite.update(mils)
      if self.mode:
          self.mode.update(mils)
