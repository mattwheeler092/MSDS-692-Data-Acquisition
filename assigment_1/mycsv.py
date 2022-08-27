import sys


def getdata():
    if len(sys.argv) == 1:
        data = sys.stdin.read()
    else:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
    return data.strip()


def readcsv(data):
    """
    Read CSV with header from data string and return a header list
    containing a list of names and also return the list of lists
    containing the data.
    """
    headers, *data = [line.split(",") for line in data.split("\n")]
    return headers, data
