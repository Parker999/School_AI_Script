import copy

has_Show = set()
def convert(datas):     # covert my 2D array to a single string for comparing later 
    S = ""
    for data in datas:
        for d in data:
            S = S + str(d)
    return S

def tilepuzzle(start, goal):
    return reverse(statesearch(start, goal, [], 0))


def statesearch(unexplored, goal, path, depth):
    if depth > 32:
        return []
    elif goal == unexplored:
        return cons(goal, path)
    else:
        has_Show.add(convert(unexplored))       # collect the state alreadt showed and use this set later 
        for newState in generateNewStates(unexplored):  # check each possible step in future possible list 
            result = statesearch(newState,
                             goal,
                             cons([unexplored], path), depth + 1)
            if result != []:
                return result
    return []


def location0(currentState):    # reture the location of currents' 0
    for i in range(len(currentState)):
        for j in range(len(currentState[i])):
            if currentState[i][j] == 0:
                return (i,j)
    return (-1,-1)


def generateup(currStateA):                     # as the function name 
    currState = copy.deepcopy(currStateA)
    result = []
    lox,loy = location0(currState)
    if lox > 0:
        currState[lox][loy] = currState[lox-1][loy]
        currState[lox-1][loy] = 0
        result.append(currState)
    return result


def generatedown(currStateA):
    currState = copy.deepcopy(currStateA)
    result = []
    lox, loy = location0(currState)
    if lox < 2:
        currState[lox][loy] = currState[lox + 1][loy]
        currState[lox + 1][loy] = 0
        result.append(currState)
    return result


def generateleft(currStateA):
    currState = copy.deepcopy(currStateA)
    result = []
    lox, loy = location0(currState)
    if loy > 0:
        currState[lox][loy] = currState[lox][loy-1]
        currState[lox][loy-1] = 0
        result.append(currState)
    return result


def generateright(currStateA):
    currState = copy.deepcopy(currStateA)
    result = []
    lox, loy = location0(currState)
    if loy < 2:
        currState[lox][loy] = currState[lox][loy + 1]
        currState[lox][loy + 1] = 0
        result.append(currState)
    return result


def generateNewStates(currState):
    datas = generateup(currState) + generateright(currState) + generatedown(currState) + generateleft(currState)
    newDatas = []
    for data in datas:      
        if convert(data) not in has_Show:     # avoid repeated 
            newDatas.append(data)
    return newDatas


def reverseEach(listOfLists):
    result = []
    for st in listOfLists:
        result.append(reverse(st))
    return result


def reverse(st):
    return st[::-1]


def head(lst):
    return lst[0]


def tail(lst):
    return lst[1:]


def take(n, lst):
    return lst[0:n]


def drop(n, lst):
    return lst[n:]


def cons(item, lst):
    return [item] + lst

##-- That wasn't so hard, was it?  Here's the whole thing in action with
##-- one hole.  Add a second hole and it should work just fine.
##--
#print(tilepuzzle([[2,8,3],[1,0,4],[7,6,5]],[[1,2,3],[8,0,4],[7,6,5]]))
##-- ['RR_BB', 'R_RBB', 'RBR_B', 'RBRB_', 'RB_BR', '_BRBR', 'B_RBR', 'BBR_R', 'BB_RR']
"""
2 8 3
1 0 4
7 6 5

2 0 3
1 8 4
7 6 5

0 2 3
1 8 4
7 6 5

1 2 3
0 8 4
7 6 5

1 2 3
7 8 4
0 6 5

1 2 3
7 8 4
6 0 5




"""
