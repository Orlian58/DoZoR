from enum import Enum

class Action(Enum):
    ALERT = 1

def action(istr):
    str = istr.lower().strip()
    if (str == "alert"):
        return Action.ALERT
    else:
        raise ValueError("Invalid rule : incorrect action : '" + istr + "'.")
