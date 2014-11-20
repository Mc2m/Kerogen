ACTIONS = type('actions', (), {'MOUSEDOWN':1,'MOUSEUP':2,'MOUSEMOVE':3})
FUNCTIONS = type('functions', (), {'RUNSCREEN':1,'CLOSE':2,'LAUNCH':3,'ANCHOR':4,'RESIZE':5,'MAXIMIZE':6,'MINIMIZE':7,'RESTORE':8})
MOUSE = type('mouse', (), {'LEFT':1,'MIDDLE':2,'RIGHT':3,'WHEELUP':4,'WHEELDOWN':5})
SKEY = type('skey', (), {'CTRL':1,'SHIFT':2,'LEFTALT':4,'RIGHTALT':8})
WIDGET = type('comp', (), {'TEXT':0,'PICTURE':1,'SHAPE':2,'DECORATOR':3,'SUB':4,'GROUP':5})
SHAPE = type('shapes', (), {'RECTANGLE':1,'ELLIPSE':4,'POLYGON':2,'CIRCLE':3,'ARC':5,'LINE':6,'AALINE':8,'LINES':7,'AALINES':9})
RESIZE = type('resize', (), {'HORIZONTAL':0,'VERTICAL':1,'DIAGONAL':2})
GRADIENT = type('gradient', (), {'HORIZONTAL':0,'VERTICAL':1,'COORDINATES':2})

LANGUAGE = type('language', (), {'ENGLISH':0,'FRENCH':1})

SYNC_PLUGIN = type('sync_plg', (), {'SQLITE':1})
