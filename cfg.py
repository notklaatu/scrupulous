# see fileformat.txt for more detailed information about the various
# defines found here.

from error import *

# linebreak types
LB_AUTO_SPACE = 1
LB_AUTO_NONE = 2
LB_FORCED = 3
LB_LAST = 4

# mapping from character to linebreak
_text2lb = {
    '>' : LB_AUTO_SPACE,
    '&' : LB_AUTO_NONE,
    '|' : LB_FORCED,
    '.' : LB_LAST
    }

# reverse to above, filled in _init
_lb2text = { }

# line types
SCENE = 1
ACTION = 2
CHARACTER = 3
DIALOGUE = 4
PAREN = 5
TRANSITION = 6

# mapping from character to line type
_text2linetype = {
    '\\' : SCENE,
    '.' : ACTION,
    '_' : CHARACTER,
    ':' : DIALOGUE,
    '(' : PAREN,
    '/' : TRANSITION
    }

# reverse to above, filled in init
_linetype2text = { }

# what's the next type from this type. used in figuring out what type
# of element to insert when user presses enter.
_nextType = {
    SCENE : ACTION,
    ACTION : ACTION,
    CHARACTER : DIALOGUE,
    DIALOGUE : CHARACTER,
    PAREN : DIALOGUE,
    TRANSITION : SCENE
    }

# what's next in physical position when using normal margins. used for
# figuring out next element when user hits tab.
_nextTypeTab = {
    SCENE : ACTION,
    ACTION : DIALOGUE,
    DIALOGUE : PAREN,
    PAREN : CHARACTER,
    CHARACTER : TRANSITION,
    TRANSITION : SCENE
    }

# type configs, key = line type, value = Type
_types = { }


# various non-user configurable (for now anyway) settings

# font size values in pixels
fontY = 14
fontX = 9

# vertical distance between rows, in pixels
fontYdelta = 18

# offsets from upper left corner of main widget, ie. this much empty
# space is left on the top and left sides.
offsetY = 10
offsetX = 10

# base font from which style-specific fonts are constructed
baseFont = None

class Type:
    def __init__(self):
        self.linetype = None
        self.emptyLinesBefore = 0
        self.indent = 0
        self.width = 0
        self.isCaps = False

def _init():
    for k, v in _text2lb.items():
        _lb2text[v] = k

    for k, v in _text2linetype.items():
        _linetype2text[v] = k

    t = Type()
    t.linetype = SCENE
    t.emptyLinesBefore = 1
    t.indent = 0 
    t.width = 60
    t.isCaps = True
    _types[t.linetype] = t
    
    t = Type()
    t.linetype = ACTION
    t.emptyLinesBefore = 1
    t.indent = 0
    t.width = 60
    _types[t.linetype] = t
    
    t = Type()
    t.linetype = CHARACTER
    t.emptyLinesBefore = 1
    t.indent = 25
    t.width = 20
    t.isCaps = True
    _types[t.linetype] = t
    
    t = Type()
    t.linetype = DIALOGUE
    t.emptyLinesBefore = 0
    t.indent = 10
    t.width = 35
    _types[t.linetype] = t
    
    t = Type()
    t.linetype = PAREN
    t.emptyLinesBefore = 0
    t.indent = 20
    t.width = 25
    _types[t.linetype] = t
    
    t = Type()
    t.linetype = TRANSITION
    t.emptyLinesBefore = 1
    t.indent = 55
    t.width = 15
    t.isCaps = True
    _types[t.linetype] = t
    

_init()

def _conv(dict, key):
    val = dict.get(key)
    if val == None:
        raise CfgError("key '%s' not found from '%s'" % (key, dict))
    
    return val

def _convPrev(dict, value):
    for (k,v) in dict.iteritems():
        if v == value:
            return k

    raise CfgError("value '%s' not found from '%s'" % (value, dict))
    
def text2lb(str):
    return _conv(_text2lb, str)

def lb2text(lb):
    return _conv(_lb2text, lb)

def text2linetype(str):
    return _conv(_text2linetype, str)

def linetype2text(type):
    return _conv(_linetype2text, type)

def getTypeCfg(type):
    return _types[type]

def getNextType(type):
    return _conv(_nextType, type)

def getNextTypeTab(type):
    return _conv(_nextTypeTab, type)

def getPrevTypeTab(type):
    return _convPrev(_nextTypeTab, type)
