#Joshua Greenawalt - CS 3361
from multiprocessing import Pool
import argparse
#I realized too late that I mixed up the rows and columns, but when trying to
#fix it I couldn't get all parts working. Sorry

def main():
    parser = argparse.ArgumentParser(description='Cell Simulation')
    parser.add_argument('-i', action="store", dest="ifilename",type = str)
    parser.add_argument('-o', action="store", dest="ofilename",type = str)
    parser.add_argument('-t', action="store", dest="t", type=int,default = 1)
    args = parser.parse_args()
    ifilename = args.ifilename
    ofilename = args.ofilename
    t = args.t
    print("Life Simulator")
    try:
        f = open(ifilename,'r')
    except FileNotFoundError:
        print("Not a valid file.")
        exit()
    l = [line.split() for line in f]
    matrix = [list(line[0]) for line in l]
    matrixwidth = len(l[0][0]) #get height and width of matrix
    matrixheight = len(l)
    for row in range(matrixwidth): #checks file validity
        for column in range(matrixheight):
            if(matrix[column][row]!= '.' and matrix[column][row]!= 'O' and matrix[column][row]!= '\n'):
                print("Invalid File.")
                exit()
    print("\nSimulating...\n") #starts by printing step 0 then running the simulation
    print("Time Step #0\n")
    for row in matrix:
        print(''.join(map(str,row)))
    runsimul(matrix,matrixwidth,matrixheight,ofilename,t)
    print("Simulation complete. Final result stored in the output file",ofilename+".")


def changecells(matrixData):
    matrix = matrixData[0]
    tempmatrix = matrixData[1]
    matrixwidth = matrixData[2]
    matrixheight = matrixData[3]
    column = matrixData[4]
    row = matrixData[5]
    del(matrixData)
    rowback = 0 #get all the neighbors of current cell
    rowforward = 0
    columnback = 0
    columnforward = 0
    count = 0
    if ((row-1) < 0):
        rowback = matrixwidth-1
    else:
        rowback = row - 1
    if ((row+1) == matrixwidth):
        rowforward = 0
    else:
        rowforward = row + 1
    if ((column-1) < 0):
        columnback = matrixheight-1
    else:
        columnback = column - 1
    if ((column+1) == matrixheight):
        columnforward = 0
    else:
        columnforward = column + 1
    neighbornum = 0 #this and neighborsval get neightbors and check if they are alive using the for loop
    neighborsval = [matrix[columnback][rowback],matrix[column][rowback],matrix[columnforward][rowback],matrix[columnback][row],matrix[columnforward][row],matrix[columnback][rowforward],matrix[column][rowforward],matrix[columnforward][rowforward]]
    for value in neighborsval:
        if (value == 'O'):
            count+=1
    if ((count <= 4 and count >= 2) and (matrix[column][row] == 'O')): #the following if statements are the cell simulation conditions
        tempmatrix = 'O'
    elif(count != 0 and count%2 == 0 and matrix[column][row] == '.'):
        tempmatrix = 'O'
    else:
        tempmatrix = '.'
    return tempmatrix #return value of current cell

def runsimul(matrix,matrixwidth,matrixheight,ofilename,t):
    for run in range(1,101):#runs steps
        tempmatrix = ['.' for j in range(matrixheight)]#makes row to edit current cell row
        finalmatrix = [['.' for j in range(matrixwidth)]for i in range(matrixheight)] #makes matrix to be modified to be the next step
        print('\n')
        MAX_PROCESSES = t
        processPool = Pool(processes=MAX_PROCESSES)#this and the for loop below add data to process
        poolData = list()
        for column in range(matrixheight):
            for row in range(matrixwidth):
                matrixData = [matrix,matrix[column][row],matrixwidth,matrixheight,column,row]
                poolData.append(matrixData)
        matrixcopy = processPool.map(changecells,poolData)#process cell change
        del(poolData)
        print("Time Step #",run,'\n',sep='')#print current step and write matrix
        rowinmc = 0
        for column in range(matrixheight):
            for row in range(matrixwidth):
                finalmatrix[column][row]=matrixcopy[rowinmc]
                rowinmc += 1
        for row in finalmatrix:
            print(''.join(map(str,row)))
        print('\n')
        matrix = finalmatrix
    with open(ofilename, 'w') as output: #output to file
        for row in matrix:
            output.write(''.join(map(str,row)))
            output.write('\n')

if __name__ == "__main__":
    main()



