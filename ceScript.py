import re

def parseStateDef(cmds):
    out = ([],[])
    for cmd in cmds:
        if ':' in cmd:
            out[1].append(tuple(map(lambda x:x.strip(), cmd.split(':', 1))))
        else:
            out[0].append(cmd.strip().split(' '))
    return out

re_num = re.compile('\d+')

def getValue(val, sprite):
    if val[0]=='@':
        return sprite.get(val[1:])
    elif re_num.match(val):
        return int(val)
    else:
        return 0

class CEScript:
    def __init__(self, fn):
        self.states = {} # map of state name to (instructions, transitions)
        script = open('rsrc/script/'+fn+'.sct').read().strip()
        stateDefs = map(lambda x: x.strip().split('\n'), script.split('//'))

        for stateDef in stateDefs:
            if stateDef[0] == '*':
                common = parseStateDef(stateDef[1:])
                for state in self.states.keys():
                    self.states[state][0].extend(common[0])
                    self.states[state][1].extend(common[1])
            else:
                self.states[stateDef[0]] = parseStateDef(stateDef[1:])

    def init(self, sprite):
        self.runState('init', sprite)

    def run(self, sprite):
        self.runState(sprite.state, sprite)

    def runState(self, state, sprite):
        sdef = self.states[state]
        for cmd in sdef[0]:
            if cmd[0]=='set':
                sprite.set(cmd[1], int(cmd[2]))
            elif cmd[0]=='inc':
                sprite.set(cmd[1], sprite.get(cmd[1]) + getValue(cmd[2], sprite))
            elif cmd[0]=='dec':
                sprite.set(cmd[1], sprite.get(cmd[1]) - getValue(cmd[2], sprite))
        for trig in sdef[1]:
            pass
