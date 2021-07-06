# ! my update on the borad evaluation
# (1) I set the stopvalue for win or lose to size**size+1 to accomodate different size of input 
#(2) I update the evaluation of nonstop board with  number difference of pawn + number of new board generate by this board,
#  I only do this when I build the board tree,so I don't look ahead 

# I constrcut a Node structure to help me development the rest of help function 
import copy
player_white=1  # white  pawn's turn 
player_black=0  # black pawn's turn 
default_evaluation=None
MAX=99999      #max turn 
MIN=-99999      #Min turn 

class Node:                        # node sturct is linkedlist, which will help me to track back my path when I find a solution 
    def __init__(self, data):
        self.data = data         #  the list usually to represent the board and the pawns 
        self.child = None          # this attribute will be a list, and each element is a Node 
        self.parent = None
        self.MAX_MIN=None
        self.player=None
        self.childnumber=0          
        self.depth = 0           # will use to determine the depth of the treenode
        self.evaluation=default_evaluation  
        self.needstop=False
    def __lt__(self, other):
        return self.evaluation < other.priority
    def __le__(self, other):
        return self.evaluation <= other.priority

def hexapawn(current1,size,current_player,depth):    
    stopvalue=size**size+1
    # print("stop value is ",stopvalue)
    move=0                          # recursive depth 
    current=Node(current1)
    current.player=player_white     # initialize the  TreeNode, white pawn play first as we assumed
    current.MAX_MIN=MAX             # will use it to track back after build tree 
    build_tree(current,depth,move,current_player,size,stopvalue)       # build_tree include the generate new states and connect child node and parent nodes
    trackback(current,depth,size,move,current_player,stopvalue)                         # MinMax search, after we build tree, we only elvaluate the terminal nodes,
    printfinal(current) #we return the next best move                                   # but trackback function will evaluate every Node above terminal Node
    return 
def convert2dlist(current1):    # (helper function ) it will convert  the one demension list to two demension 
    twoDlist=[]
    current=copy.deepcopy(current1)
    for i in range(len(current)):
        twoDlist.append(list(current[i]))
    return twoDlist
def convertbacklist(current1):      # (helper function ) it will convert back the two demension list back to our input one demension 
    normallist=[]
    current=copy.deepcopy(current1)
    for j in range(len(current)):
        temp=""
        for i in range(len(current[j])):
            temp=temp+"".join(current[j][i])
        normallist.append(temp)
    return normallist

def connect_child_parent(result,current,size,current_player,stopvalue):       # connect the parent and child node together, and also check the if child Node win or lose, so we can stop there
    # print("one two ")
    current.child=result
    current.childnumber=len(result)
    for i in range(len(result)):
        result[i]=Node(result[i])
        child=result[i]
        # print("child 1111111111111111",child.data)
        if(current.player==player_white):
            child.player=player_black
        elif(current.player==player_black):
            child.player=player_white
        if(current.MAX_MIN==MAX):
            child.MAX_MIN=MIN
        else:
            child.MAX_MIN=MAX
        check_if_win_or_lose(child,size,current_player,stopvalue)
        # if(child.needstop):
        #     print("need stop")
        child.parent=current
        child.childnumber=0
        child.child=None
        child.depth=current.depth+1
        child.evaluation=default_evaluation

    return 
def moveahead(current,size):  #(helper function for generate new state)  
    result=[]
    if current.player==player_white:
        board=convert2dlist(current.data)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j]=='w' and (i!=(size-1)):
                    boardnew=copy.deepcopy(board)
                    if(board[i+1][j]=='-'):
                        boardnew[i][j]="-"
                        boardnew[i+1][j]="w"
                        result.append(convertbacklist(boardnew))
        return result
    if current.player==player_black:
        board=convert2dlist(current.data)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j]=='b' and (i!=0):
                    boardnew=copy.deepcopy(board)
                    if(board[i-1][j]=='-'):
                        boardnew[i][j]="-"
                        boardnew[i-1][j]="b"
                        # print('b')
                        result.append(convertbacklist(boardnew))
        return result
    return result
def movedioagnlly(current,size):            #(helper function for generate new state)  
    result=[]
    if current.player==player_white:          #if it's white panws turn  to move
        board1=convert2dlist(current.data)
        for i in range(len(board1)):
            for j in range(len(board1[i])):
                if board1[i][j]=='w' and (i!=(size-1)):
                    board=copy.deepcopy(board1)
                    if(j!=0 and j!=size-1):
                        if(board[i+1][j-1]=='b'):
                            board3=copy.deepcopy(board1)
                            board3[i+1][j-1]='w'
                            board3[i][j]='-'
                            result.append(convertbacklist(board3))
                            
                        if(board[i+1][j+1]=='b'):
                            board2=copy.deepcopy(board1)
                            board2[i+1][j+1]='w'
                            board2[i][j]='-'
                            result.append(convertbacklist(board2))
                        # return result
                    if(j==0):
                        if(board[i+1][j+1]=='b'):
                            board[i+1][j+1]='w'
                            board[i][j]='-'
                            result.append(convertbacklist(board))
                        # return result 
                    if(j==size-1):
                        if(board[i+1][j-1]=='b'):
                            board[i+1][j-1]='w'
                            board[i][j]='-'
                            result.append(convertbacklist(board))
                        # return result
        return result
    if current.player==player_black:            #if it's black panws turn  to move
        board1=convert2dlist(current.data)
        for i in range(len(board1)):
            for j in range(len(board1[i])):
                if board1[i][j]=='b' and (i!=0):
                    board=copy.deepcopy(board1)
                    if(j!=0 and j!=size-1):
                        if(board[i-1][j-1]=='w'):
                            board3=copy.deepcopy(board1)
                            board3[i-1][j-1]='b'
                            board3[i][j]='-'
                            result.append(convertbacklist(board3))
                        if(board[i-1][j+1]=='w'):
                            board2=copy.deepcopy(board1)
                            board2[i-1][j+1]='b'
                            board2[i][j]='-'
                            result.append(convertbacklist(board2))
                        # return result
                    if(j==0):
                        if(board[i-1][j+1]=='w'):
                            board[i-1][j+1]='b'
                            board[i][j]='-'
                            result.append(convertbacklist(board))
                        # return result 
                    if(j==size-1):
                        if(board[i-1][j-1]=='w'):
                            board[i-1][j-1]='b'
                            board[i][j]='-'
                            result.append(convertbacklist(board))
                        # return result
        return result
    return result
def generate_new_move(current,size,current_player,stopvalue):   # generate new states and build connection between current state and child state
    result=[]
    if(current.needstop==False):
        result=moveahead(current,size)+movedioagnlly(current,size)
        # print("one two three")
        connect_child_parent(result,current,size,current_player,stopvalue)
    return result
def checkifgotoend(current,size,current_player,stopvalue):      #check the case we reach the end of the board
    for i in range(len(current.data)):
        if 'b' in current.data[0]:
            if (current.player==player_white and current_player=='w'):
                return -stopvalue
            else:
                return stopvalue
        elif 'w' in current.data[size-1]:
            if (current.player==player_black and current_player=='b'):
                return -stopvalue
            else:
                return stopvalue
    return 0   
def checkifstopmove(current,size,current_player,stopvalue): #check the case if we can move or not 
    result=moveahead(current,size)+movedioagnlly(current,size)
    checkvalue=len(result)
    # print("pao")
    if(checkvalue==0):
        if((current.player==player_white and current_player=='w') or (current.player==player_black and current_player=='b')):   # return -10 only if the player are playing this turn 
            return -stopvalue
        else:
            return stopvalue
    else:
        return 0
def check_differentce_pawns(current,current_player):        # helper function for board evaluation, return the num difference of balck and white pawns
    board=convert2dlist(current.data)
    bcount=0
    wcount=0
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j]=='b'):
                bcount=bcount+1
            if(board[i][j]=='w'):
                wcount=wcount+1
    if(current_player=='w'):
        return wcount-bcount
    elif(current_player=='b'):
        return bcount-wcount
    return 0
def check_num_pawns(current,current_player,stopvalue):  # check if still have any panws, if 0 pawns left, game over
    board=convert2dlist(current.data)
    bcount=0
    wcount=0
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j]=='b'):
                bcount=bcount+1
            if(board[i][j]=='w'):
                wcount=wcount+1
    if(bcount==0 and current_player=='b'):
        return -stopvalue
    if(wcount==0 and current_player=='w'):
        return -stopvalue
    return 0
def check_if_win_or_lose(current,size,current_player,stopvalue):    # check if we win or lose, if we win or lose, we need to set this state to needstop==True, so we don't move
    if(checkifstopmove(current,size,current_player,stopvalue)!=0 ):     # the board 
        # print("check stop",checkifstopmove(current,size,current_player))
        current.needstop=True
        return -1
    if checkifgotoend(current,size,current_player,stopvalue)!=0 :
        current.needstop=True
        return -2
    if check_num_pawns(current,current_player,stopvalue)!=0:
        current.needstop=True
        return -3
    else:
        current.needstop=False
        return 0
def evaluation(current,size,current_player,stopvalue):          # board evluation : this board evaluation only evaluation the terminal nodes, however, I will use these value to MinMax search 
    check_if_win_or_lose(current,size,current_player,stopvalue) # but I will use child number of current state to update Node's evaluation points above terminal Node
    if(current.needstop):                                        
        if(checkifstopmove(current,size,current_player,stopvalue)==-stopvalue or checkifgotoend(current,size,current_player,stopvalue)==-stopvalue or check_num_pawns(current,current_player,stopvalue)==-stopvalue):
            current.evaluation=-stopvalue
        else:
            current.evaluation=stopvalue
    else:
        current.evaluation=check_differentce_pawns(current,current_player)
def build_tree(current,depth,move,current_player,size,stopvalue): # recursively build tree
    seed=current
    # print(current.data)
    # print("move",move)
    if(move==depth):                                              # entrance of recursive function 
        # print("move",move)
        evaluation(seed,size,current_player,stopvalue)
        return 
    else:
        for i in range(len(generate_new_move(seed,size,current_player,stopvalue))):
            build_tree(seed.child[i],depth,move+1,current_player,size,stopvalue)
        # print("finished")
def printsinglemove(data):              # help function to print a list
    for j in range(len(data)):
        if(data[j] != None):
            print(data[j])
def printlistnode(result):   # (only for testing), print the Node's child's data and depth
    for i in range(len(result)):
        printsinglemove(result[i].data)
        print("depth",result[i].depth)
    return
def printtree(current):# (only for testing) print the whole tree, and terminal Node's evaluation  
    if current.child!=None:
        if(current.MAX_MIN==MAX):
            print("max")
        elif(current.MAX_MIN==MIN):
            print("min")
        print("depth",current.depth)
        if(current.evaluation!=default_evaluation):
            print("evaluation is :",current.evaluation)
        printsinglemove(current.data)
        for i in range((current.childnumber)):
            printtree(current.child[i])
    else:
        if(current.MAX_MIN==MAX):
            print("max")
        elif(current.MAX_MIN==MIN):
            print("min")
        print("depth",current.depth)
        if(current.evaluation!=default_evaluation):
            print("evaluation is :",current.evaluation)
        printsinglemove(current.data)
        
        
def find_MAX_MIN(result,string,size,current_player,stopvalue):       # return the max or min value of current's Node's child's evaluation 
    numlist=[]
    maxnum=MAX
    minnum=MIN
    for i in range((result.childnumber)):
        if(result.evaluation==default_evaluation):
            if(result.child[i].evaluation!=None):
                numlist.append(result.child[i].evaluation)
    if(len(numlist)!=0):
        # print("numlist",numlist,"max or min",result.MAX_MIN)
        if(string==MAX and max(numlist)!=None):
            maxnum=max(numlist)
            return maxnum
        elif(string==MIN and min(numlist)!=None):
            minnum=min(numlist)
            return minnum
    elif(len(numlist)==0):          # No child, then we just update Node's own evaluation
        evaluation(result,size,current_player,stopvalue)
        eva=result.evaluation
        return eva
    return

def Min_MAX_search(current,depth,size,move,current_player,stopvalue):       # only update one depth's Node, statring from Depth-1 to Depth==0
    seed=current                                                            # so it will update the terminal Node's parent evluation , 
    if(move==depth-1):                                                         #then next time, it will update terminal's parent's parent and so on 
        eva=find_MAX_MIN(seed,seed.MAX_MIN,size,current_player,stopvalue)
        eva=eva+seed.childnumber                                            # this is part of  my evaluation when I do minisearch, I will add more credit to a state if it has more child
        if(eva>=stopvalue):
            eva=stopvalue-1
        current.evaluation=eva
        # print("eva000",eva)
        return 
    else:
        for i in range(seed.childnumber):
            Min_MAX_search(seed.child[i],depth,size,move+1,current_player,stopvalue)

def trackback(current,depth,size,move,current_player,stopvalue):  # this will update all the node above terminal's layer 
    for i in range(depth):
        Min_MAX_search(current,depth-i,size,move,current_player,stopvalue)
    return

def printfinal(result):                                                 # return the next best step, the result of function hexapawn()
    eva=result.evaluation
    # print("eva",eva)
    for i in range(result.childnumber):
        evaofchild=result.child[i].evaluation+result.childnumber
        # print("ebac",evaofchild)
        if(eva==evaofchild ):
           print(result.child[i].data)
           return
        elif(result.child==None):
            print("no legal next step,because you already lose or win")
            return
    print(result.child[0].data)
    return

# if __name__ == "__main__":
#     # hexapawn(["wwww","----","----","bbbb"],4,'w',4)
#     hexapawn(["www","---","bbb"],3,'b',2)
      
# if __name__ == "__main__":
#     hexapawn(["www","---","bbb"],3,'b',2)
# hexapawn(["www","---","bbb"],3,'w',2)



    # start=["www","---","bbb"]
    # current=Node(start)
    # current.player=player_white
    # current.MAX_MIN=MAX
    # build_tree(current,4,0,'w')
    # # printtree(current)
    # trackback(current,4,3,0,'w')
    # printtree(current)
    # test=['--w', 'wb-', '-bb']
    # test1=Node(test)
    # test1.player=player_black
    # printsinglemove(test)
    # evaluation(test1,3,'w')
    # print(test1.evaluation)


    # print("max",max(1,1))
    # print(current.evaluation)
    # print(current.child[0].evaluation)
    # print(current.child[1].evaluation)
    # print(current.child[2].evaluation)
    # printfinal(current)
    # tes=Node(['ww-', 'b--', '-wb']) 
    # evaluation(test,3,'w')
    # result=generate_new_move(current,3,'w')
    # result2=generate_new_move(result[0],3,'w')
    # result3=generate_new_move(result[1],3,'w')
    # result4=generate_new_move(result[2],3,'w')
    # result3=moveahead(result[0],size)+movedioagnlly(result[0],size)
    # print("size",len(result2))
    # printlistnode(result)
    # printlistnode(result2)
    # printlistnode(result3)
    # printlistnode(result4)
    # print("result3",len(result3))
    # print(result3)
    # printlistnode(result2)
    # print(result[0].data)
    
    # result2=moveahead(result[0],size)+movedioagnlly(result[0],size)
    # print("win",check_if_win_or_lose(result[0],3,'w'))
    # if(result[0].needstop==True):
    #     print("stop")
    # print(check_num_pawns(result[0],'w'))
    # print("go end",checkifgotoend(result[0],size,'w'))

    # print(result2)
    # result1=movedioagnlly(test1,3)
    # build_tree(current,3,0,'w')
# --w
# wwb
# bb-
    # printtree(current)
    # print(result1)
    # print(current.child[2].player)
    # print(moveahead(current,3))
    # print(current.data)
    # build_tree(current,2,0,'w')
    # printtree(current)

