import copy
from queue import PriorityQueue    #main idea of my code, I use use priorityQueue to decide which step to to run 
class Node:                        # node sturct is linkedlist, which will help me to track back my path when I find a solution 
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
        self.depth = 0
        self.priority=0
    def __lt__(self, other):
        return self.priority < other.priority
    def __le__(self, other):
        return self.priority <= other.priority

def checkifexit(current):            #check if XX car exit 
    if ((current[2][4]=="X") and (current[2][5]=="X")):
        return 0
    else:
        return 1
def checkblock(next):  ## help function of the blocking heuritic function, return the number of car blcoked the way 
    blockedcar=[]
    end=-1
    for i in range(6):
        if(next[2][i]=="X"):
            end=i
    for j in range(6):
        if(next[2][j]!="X" and next[2][j]!="-"and end<j):
            blockedcar.append(next[2][j])
    return len(blockedcar)
def heuristic(next1):       #the blocked heuristic function 
    next=copy.deepcopy(next1)
    if (checkifexit(next)==0):
        return 0
    else:
        return 1+checkblock(next)
def secondheuristic(next1): # my blocked heuritic function ; I improve the blocking heuristic by adding the distance of XX to exit 
    next=copy.deepcopy(next1)
    if (checkifexit(next)==0):
        return 0
    else:
        return 1+checklength_to_end(next)+checkblock(next)
def checklength_to_end(next):  ## help function of the my heuritic function, return the distance to the exit  for example -XX--- will return 3 and it doesn't care about blcoked car
    end=-1
    for i in range(6):
        if(next[2][i]=="X"):
            end=i
    return len(next)-end
def findallcar(start):   #help function of generate new state; this would return a list,contain the "car name",car length and direction could move for exmaple ['Bv3', 'Xh2', 'Ah2'] ,B is car, and v or h is direction
    carlist=[]
    for i in range(6):
        # print(start[i])
        for j in range(6):
            if(start[i][j]!="-" and start[i][j] not in carlist):
                carlist.append(start[i][j])
    for i in range(len(carlist)):
        verticalcount=0
        for j in range(6):
            if(start[j].count(carlist[i])>1):
                carlist[i]=carlist[i]+"h"+str(start[j].count(carlist[i]))
            elif(start[j].count(carlist[i])==1):
                verticalcount=verticalcount+1
            if (verticalcount > 1 and j == 5):
                carlist[i] = carlist[i] + "v" + str(verticalcount)
    return carlist
    
def convert2dlist(current1):    # help function, it will convert the input ["--B---",
                                                            #              "--BAAA",
                                                            #              "--XXC-",
                                                            #              "----C-",
                                                            #              "----D-",
                                                            #              "----D-"]
                                                            # to a two demension list, each list contain only len (str) =1 , it will make my code easier to do the state generate
    twoDlist=[]
    current=copy.deepcopy(current1)
    for i in range(len(current)):
        twoDlist.append(list(current[i]))
    return twoDlist
def convertbacklist(current1):      # it will convert back the two demension list back to our input one demension 
    normallist=[]
    current=copy.deepcopy(current1)
    for j in range(len(current)):
        temp=""
        for i in range(len(current[j])):
            temp=temp+"".join(current[j][i])
        normallist.append(temp)
    return normallist

def rightmove(current,oldx,oldy,newx,newy):                     #help function to current_possiblemove()
 #   print(1)
 #   print("rightmove",oldx,oldy,newx,newy)
    TwoD=convert2dlist(current)
    temp="".join(TwoD[oldy][oldx])
    TwoD[oldy][oldx]=TwoD[newy][newx]
    TwoD[newy][newx]=temp
    rightmove=convertbacklist(TwoD)
    return rightmove
def leftmove(current,oldx,oldy,newx,newy): #help function to current_possiblemove()
  #  print(2)
  #  print("leftmove",oldx,oldy,newx,newy)
    TwoD=convert2dlist(current)
    temp="".join(TwoD[oldy][oldx])
    TwoD[oldy][oldx]=TwoD[newy][newx]
    TwoD[newy][newx]=temp
    leftmove=convertbacklist(TwoD)
    return leftmove
def upmove(current,oldx,oldy,newx,newy):#help function to current_possiblemove()
 #   print(3)
  #  print("upmove",oldx,oldy,newx,newy)
    TwoD=convert2dlist(current)
    temp="".join(TwoD[oldy][oldx])
    TwoD[oldy][oldx]=TwoD[newy][newx]
    TwoD[newy][newx]=temp
    upmove=convertbacklist(TwoD)
    return upmove
def downmove(current,oldx,oldy,newx,newy):#help function to current_possiblemove()  The four function are indetntical, it just make debug easier by seperating them 
  #  print(4)
  #  print("downmove",oldx,oldy,newx,newy)
    TwoD=convert2dlist(current)
    temp="".join(TwoD[oldy][oldx])
    TwoD[oldy][oldx]=TwoD[newy][newx]
    TwoD[newy][newx]=temp
    downmove=convertbacklist(TwoD)
    return downmove

def current_possiblemove(current,carlist): # main function to generate new state by current state 
    vertcar=""
    movelist=[]
    rightmove1=copy.deepcopy(current)
    leftmove1=copy.deepcopy(current)
    upmove1=copy.deepcopy(current)
    downmove1=copy.deepcopy(current)
    for i in range(len(carlist)):
        for row in range(len(current)):
            for column in range(len(current[row])):
                # print(current[row][column])
                if current[row][column]==carlist[i][0]:
                    if carlist[i][1]=="h":
                        if((column+int(carlist[i][2]))<=5 and current[row][column+int(carlist[i][2])] == "-"):      ## right shift condition 
                            # print(carlist[i][0])
                            oldx=column
                            oldy=row
                            newx=column+int(carlist[i][2])
                            newy=row
                            movelist.append(rightmove(rightmove1,oldx,oldy,newx,newy))
                            # print(carlist[i])
                            # print(row,column)
                        if(column>0 and current[row][column-1] == "-"):      ## left shift condition 
                            # print(carlist[i][0])
                            oldx=column+int(carlist[i][2])-1
                            oldy=row
                            newy=row
                            newx=column-1
                            # print(carlist[i])
                            # print(row,column)
                            movelist.append(leftmove(leftmove1,oldx,oldy,newx,newy))
                    elif carlist[i][1]=="v":  
                        if(vertcar.count(carlist[i][0])==0):
                            vertcar=carlist[i][0]+vertcar
                            if((row+int(carlist[i][2]))<=5 and current[row+int(carlist[i][2])][column] == "-"):
                                oldx=column
                                oldy=row
                                newy=row+int(carlist[i][2])
                                newx=column
                                # print(carlist[i][0])
                                movelist.append(downmove(downmove1,oldx,oldy,newx,newy))
                            if(row>0 and current[row-1][column]  == "-"):
                                # print(carlist[i][0])
                                oldx=column
                                oldy=row+int(carlist[i][2])-1
                                newx=column
                                newy=row-1
                                movelist.append(upmove(upmove1,oldx,oldy,newx,newy))
                    break
    return movelist
def printfinalpath(currentpath,exploredpath):   # print out the result 
    for i in range(len(currentpath)-1,-1,-1):
        for j in range(len(currentpath[i])):
            if(currentpath[i][j] != None):
                print(currentpath[i][j])
        print("\n")
    print("total moves : ",len(currentpath)-1)
    print("total states explored : ",len(exploredpath))
    return
def convertlisttostr(current):      # help function, convert a input list to a single str, so I can add the str in the set()
    newstr=""
    for i in range(len(current)):
        newstr=newstr+"".join(current[i])
    return newstr
def producefinalresult(currentpath,start):  # track back our exlopred state to get path
    finalpath=[]
    tail=currentpath[-1]
    while(1):
        data=tail.data
        finalpath.append(data)
        if(tail.data!=start):
            tail=tail.prev
        else:
            break
    return finalpath
def getPri(node):   # get priority value for a single state  argument 0
    return heuristic(node.data)+node.depth
def getsecondPri(node): # get priority value for a single state  argument 1
    return secondheuristic(node.data)+node.depth
def rushhour(a,start):  #main function 
    current=start
    initial=Node(current)
    initial.depth = 0
    initial.prev=None       #above is initilize the node 
    frontier=PriorityQueue()
    frontier.put(initial,0)
    exploredpath=set()  # it contain a list converted string, which help me to avoid interate repteated step 
    exploredpath.add(convertlisttostr(initial.data))
    currentpath=[]
    currentpath.append(initial)
    while not frontier.empty():
        current =frontier.get()
        exploredpath.add(convertlisttostr(current.data))
        currentpath.append(current)
        if(checkifexit(current.data)==0):
            break
        for nextstate in current_possiblemove(current.data,findallcar(current.data)):
            if convertlisttostr(nextstate) not in exploredpath:
                node=Node(nextstate)
                node.prev=current
                node.depth=current.depth+1  #update move 
                if(a==0):                   #update get priority 
                    node.priority=getPri(node)
                elif(a==1):
                    node.priority=getsecondPri(node)
                else:
                    return "first argument should be 0 or 1"
                exploredpath.add(convertlisttostr(node.data))
                currentpath.append(node)
                frontier.put(node,node.priority) # enque 
    return printfinalpath(producefinalresult(currentpath,start),exploredpath)

# if __name__ == "__main__":
#     rushhour(0, ["ABB-C-",
#              "ADE-CS",
#              "ADEXXS",
#              "IIIR-S",
#              "--TRKK",
#              "UUTYY-"])

  #  print(checkblock(start2))