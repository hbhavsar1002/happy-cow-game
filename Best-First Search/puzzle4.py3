'''
Name :  Harsh Hirenkumar Bhavsar
'''


#Importing required packed
import queue, copy, sys



#------------------------------------------------------------------------------#
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
    
    #Size of given 2d array
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



#------------------------------------------------------------------------------#



#Get the filename from user
input_filename,output_filename = user_input()

#Get farm data from input file
farm = input_data(input_filename)

farm_grid = farm[1:]

#Pop the first element from list to process
farm_size = farm.pop(0)

frontier = queue.PriorityQueue()

start_actions = queue.PriorityQueue()

for i in range(0,int(farm_size[0])):
    for j in range(0,int(farm_size[0])):
        if farm[i][j] == ".":
            start_actions.put([(i,j)])
            
while not start_actions.empty():
    action = start_actions.get()
    Total_Cow_Score = 0
    
    temp_farm  = copy.deepcopy(farm_grid)
    
    for i in action:
        row = i[0]
        col = i[1]
        
        if temp_farm[row][col] == "." :
            temp_farm[row][col]= "C"
            
    for i in action:
        row = i[0] 
        col = i[1]
        
        Total_Cow_Score += CountScore(temp_farm, row, col)
        
    temp = action[:]
    temp.insert(0,-Total_Cow_Score) 
    frontier.put(temp)

#counting number of haystacks
haystack_count= 0
for i in range(len(farm_grid)):
    haystack_count += farm_grid[i].count('@')


while not frontier.empty():
    data = frontier.get()
    action = data[1:]
    
    Total_Cow_Score = 0
    
    temp_farm  = copy.deepcopy(farm_grid)
    
    for i in action:
        row = i[0]
        col = i[1]
        
        if temp_farm[row][col] == "." :
            temp_farm[row][col]= "C"
            
    for i in action:
        row = i[0] 
        col = i[1]
        
        Total_Cow_Score += CountScore(temp_farm, row, col)
    
    if Total_Cow_Score >= 12:
        if haystack_count == len(action):
            farm = temp_farm[:]
            break
    
    if haystack_count == len(action):
        continue
    
    for i in range(0,int(farm_size[0])):
        for j in range(0,int(farm_size[0])):
            temp = action[:]
            if (i,j) > action[-1] and farm_grid[i][j] == '.':
                temp.insert(0,-Total_Cow_Score)
                temp.append((i,j))
                frontier.put(temp)
    
    
#Add the farm size back to data
farm.insert(0,farm_size)

#Append the total cow score into the data
farm.append([str(Total_Cow_Score)])

#Create an output file 
output_data(farm,output_filename)
