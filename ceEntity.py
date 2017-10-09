class CEEntity(object):

    '''
    A CEEntity is anything that has variables (including a timer, which is always there by default).
    This includes all sprites and the current stage, and possibly other things as needed. Scripts
    are always run relative to an instance of CEEntity; this is how we can use the same language to
    refer to either sprites or stages.

    CEEntity variables are arbitrary strings. CEEntity values are arbitrary objects, including
    other CEEntity instances.
    
    Some variables have special extra handling; see the set method for details.
    '''

    def __init__(self):
        self.timer = 0
        self.vars = {}

    def set(self, name, val):
        self.vars[name] = val
        if name == 'x':
            self.vars['tilex'] = val/16
            self.vars['physx'] = val*16
        if name == 'y':
            self.vars['tiley'] = val/16
            self.vars['physy'] = val*16

    def get(self, name, default=None):
        if name in self.vars:
            return self.vars[name]
        return default

    def update(self, mils):
        self.timer += mils
