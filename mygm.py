import gmxlib
import random


title = "Example Title"


def leq(x, y):
    """
    Reports whether x is less than or equal to y.
    
    :param x: A STRING representation of an element
    :param y: A STRING representation of an element 
    :return: True if x is less than or equal to y, else false
    """

    return False


def new():
    """
    Produces a new element
    
    :return: A STRING representation of an element 
    """

    return ""

gmxlib.run(title=title, leq=leq, new=new)
