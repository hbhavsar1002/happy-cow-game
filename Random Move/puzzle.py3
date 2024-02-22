#--------Import required packages-------
import random
import sys



#--------Function definitions--------
#Function to take input from user
def user_input():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    return input_file,output_file
    

#Function to fetch data from input text file into nested list
def input_data(input_filename):
    
    with open(input_filename) as f:
        lines = [line.rstrip() for line in f]
    
    list_lines = []

    for i in lines:
        a = list(i.rstrip())
        list_lines.append(a)
        
    return list_lines
    
        
#Function to enter cow in farm randomly
def enter_cows():
    
    #counting number of @'s
    counter = 0
    for i in range(len(list_lines)):
        counter += list_lines[i].count('@')
    
    #check if the first element digit or not
    if list_lines[0][0].isdigit():
        farm_size = int(list_lines[0][0])
    else:
        print("The first line does not contain a positive number")
    
    #replacing "." with "C"
    i = 1
    while(i<=counter):
            ind_1 = random.randint(1,farm_size)
            ind_2 = random.randint(0,farm_size - 1)
            if list_lines[ind_1][ind_2] == "." :
                list_lines[ind_1][ind_2] = "C"
                i +=1
                

#Function to find the index of a particular character
def find(c):
    for i, line in enumerate(list_lines):
        for j,k in enumerate(line):
            try:
                if k == c:
                    yield i, j
            except ValueError:
                continue
            
            
#Function to check if the postion is valid or not
def isValidPos(i, j, n, m):
 
    if (i < 0 or j < 0 or i > n - 1 or j > m - 1):
        return 0
    return 1
    

#Function to count the score of a cow based on it's position
def count_score(arr, i, j):
    offsets = [[-1,-1],[-1,0],[-1,1],
               [0,-1],         [0, 1],
               [ 1,-1],[1, 0],[1,1]]

    
    #Size of given 2d array
    n = len(arr)
    m = len(arr[0])
    
    #Initialize the variables before loop
    cow_score = 0
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
        cow_score -= 3
    if haystack:
        cow_score += 1
        if pond:
            cow_score += 2
        
         
    return cow_score
    

#Function to write the nested list in output file
def output_data(lines, filename):
    with open(filename, 'w') as file:
        for item in list_lines:
            for i in range(len(item)):
                file.write("%s" % item[i])
            file.write("\n")
        file.close()



#--------Main--------
#Get the filename from user
input_filename,output_filename = user_input()

#Get farm data from input file
list_lines = input_data(input_filename)

#Enter cows in farm randomly
enter_cows()

#Pop the first element from list to process
farm_size = list_lines.pop(0)


#Find the index for all the Cows placed in the farm
matches = [match for match in find('C')]

#Calculate Score of all the cows
total_cow_score = 0
for i,j in matches:
    total_cow_score += count_score(list_lines, i, j)

#add the farm size back to data
list_lines.insert(0,farm_size)

#append the total cow score into the data
list_lines.append([str(total_cow_score)])

#create an output file 
output_data(list_lines,output_filename)
