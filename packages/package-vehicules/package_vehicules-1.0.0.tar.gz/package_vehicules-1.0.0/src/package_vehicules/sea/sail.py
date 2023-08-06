"""
A python module to keep on sailing
"""

SAIL_TYPE="spinaker"
POINT="reaching"

def dinghy():
    """
    Sailing a single hull light boat
    """
    SAIL_TYPE="tormentine"
    print("Single hull");

def hobie_cat():
    """
    Sailing a fast boat
    """
    print("Two hulls or more");

if __name__ == '__main__':
    print("Sailing is enjoying life!")