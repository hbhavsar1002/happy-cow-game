'''Name: Harsh Hirenkumar Bhavsar'''

#Importing required packed
from queue import LifoQueue
import copy, sys


#Function definitions

#Function to get user input or arguments
def user_input():
    
    #sys.argv[0] = puzzle2.py3
    input_file = sys.argv[1]    #$1
    output_file = sys.argv[2]   #$2
    
    return input_file,output_file

#Function to fetch the data from input file and store it into 
def input_data(input_filename):
    
    with open(input_filename) as f:
        lines = [line.rstrip() for line in f]
    
    list_lines = []

    for i in lines:
        a = list(i.rstrip())
        list_lines.append(a)
        
    return list_lines

#Function to check if the position is valid or not
def isValidPos(i, j, n, m):
 
    if (i < 0 or j < 0 or i > n - 1 or j > m - 1):
        return 0
    return 1

#Function to count score of a cow
def CountScore(arr, i, j):
    offsets = [[-1,-1],[-1,0],[-1,1],
               [0,-1],         [0, 1],
               [ 1,-1],[1, 0],[1,1]]
    
 # Size of given 2d array
    n = len(arr)
    m = len(arr[0])

#Initialize the variables before loop
    CowScore = 0
    another_cow = False
    haystack = False
    pond = False
    
    for off in range(0,8):
    
        
        row = i + offsets[off][0]
        col = j + offsets[off][1]
        
        #Check if the index is orthogonal, since we need to find haystack and pond in vertical and horizontal positions
        total = sum(offsets[off])
        
        #The sum of row and column index of orthogonal positions are either -1 or 1
        if total == -1 or total == 1:
            orthogonal = True
        else:
            orthogonal = False
        
        #Check if the index is a valid position or not 
        if (isValidPos(row,col,n,m)):
        
        #Check if the object is present or not and accordingly change the boolean flag
            if arr[row][col] == 'C':
                another_cow = True
            elif orthogonal:
                if arr[row][col] == '@':
                    haystack = True
                if arr[row][col] == '#': 
                    pond = True
                    
    #Calculate the score of cow based on the objects adjacent to them
    if another_cow:
        CowScore -= 3
    if haystack:
        CowScore += 1
        if pond:
            CowScore += 2
        
    return CowScore
    

#Function to create output file in local drive
def output_data(lines, filename):
    with open(filename, 'w') as file:
        for item in lines:
            for i in range(len(item)):
                file.write("%s" % item[i])
            file.write("\n")
        file.close()
        
        
#Function to process the depth first search
def process_data(depth_limit, gameboard, farm_size_int):

    #Define Queue for frontier to hold all the actions or positions where cow will be placed, including the path
    game_actions = LifoQueue()
    
    found = False
    
    depth = 1
    
    #Using DFS algorithm to find the correct path
    #Initialize frontier will all the possible actions
    for i in reversed(range(0,farm_size_int)):
        for j in reversed(range(0,farm_size_int)):
            if gameboard[i][j] == ".":
                game_actions.put([(i,j)])
                
    
    #Run the loop while frontier is not empty
    while not game_actions.empty():
        
        #Get the action
        try:
            action = game_actions.get_nowait()
            depth = len(action)
        except:
            break
        
        #Initializing the total cow score for a single path
        Total_Cow_Score = 0
        
        #Creating a temporary copy of farm for calculations
        temp_farm  = copy.deepcopy(gameboard)
        
        #Place the cows based on the action path
        for i in action:
            row = i[0] 
            col = i[1]
            
            if temp_farm[row][col] == "." :
                temp_farm[row][col]= "C"
        
        #Calculate the score of based on cow position 
        for i in action:
            row = i[0] 
            col = i[1]
            
            Total_Cow_Score += CountScore(temp_farm, row, col)
        
        #Our goal is to file the first path which is a total cow score of atleast 7
        if Total_Cow_Score >= 7:
            found = True
            final_gameboard = temp_farm[:]
            print("Path", action)
            break
        
        #Enqueue the frontier with next paths
        if depth_limit != 1:
            #Check if the depth limit is reached, if that is the case then do not go to next level
            if depth < depth_limit:
                #Find the actions on next level
                for i in reversed(range(0,farm_size_int)):
                    for j in reversed(range(0,farm_size_int)):
                        temp = action[:]
                        if (i,j) > action[-1] and farm_grid[i][j] == '.':
                        
                            temp.append((i,j))
                            game_actions.put(temp)
        
    #Return the parameters based on the processed data
    if found:
        return final_gameboard, True, Total_Cow_Score
    else:
        return gameboard,False, Total_Cow_Score
                

#Get the filename from user
input_filename,output_filename = user_input()

#Get farm data from input file
farm = input_data(input_filename)

farm_grid = farm[1:]

#Pop the first element from list to process
farm_size = farm.pop(0)

farm_size_int = int(farm_size[0])

limit = 1

solution_found = False
            
final_farm = []
            
while solution_found is False:
    final_farm, found, final_score = process_data(limit, farm_grid, farm_size_int)
    solution_found = found
    if solution_found is True:
        break
    else:
        #Increase the limit if the solution is not found
        limit += 1
    
    
#add the farm size back to data
final_farm.insert(0,farm_size)

#append the total cow score into the data
final_farm.append([str(final_score)])

#create an output file 
output_data(final_farm,output_filename)
