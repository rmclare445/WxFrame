"""

Functions for handling string inputs

"""


def rm_parentheses( string ):
    ''' Remove all content within parentheses '''
    new = ""
    text = True
    for i in string:
        if i == "(":
            text = False
        elif i == ")":
            text = True
        elif text:
            new = new + i
    return new


def remove_html( string ):
    ''' Remove all html commands enclosed by <> '''
    new = ""
    text = True
    for i in string:
        if i == "<":
            text = False
        elif i == ">":
            text = True
        elif text:
            new = new + i
    return new


def cap_first( string ):
    ''' Capitalize the first letter of a string '''
    return string[0].upper()+string[1:]