#!/usr/bin/python3

'''
Parse sparse matrix from data file
'''
import re
import argparse
import random

#=================================================================================
# Utility functions
#=================================================================================
def debug(matrix):
    for col in matrix:
        for cell in col:
            print (cell[0], cell[1], cell[2])    

def splitLine (line):
    toks = line.split(' ')
    if len(toks) == 2:
        toks.append("1.0")
    return [int(toks[0]), int(toks[1]), float(toks[2])]

#=================================================================================
# Read input data from file
#=================================================================================
NUM_ROWS = 0
def readInput(in_file):
    fh = open (in_file)
    # get 1st line matrix size
    M = 0
    for line in fh:
        # skip comments
        if re.match("\%", line):
            continue
    
        if M == 0:                                   # 1st line of data size M N TOTAL
            cell = splitLine(line)
            M = cell[1]
            NUM_ROWS = M
            matrix = [[] for i in range(M + 1)]      # *** index starts from 1
            break

    # read data from file
    for line in fh:
        cell = splitLine(line)
        i = cell[0]
        j = cell[1]
        matrix[i].append(cell)                      # *** add to row MATRIX[i]
        if i > j:
            matrix[j].append([j, i, cell[2]])       # *** add symmetric value if not i == j
    
    fh.close()
    return matrix

#=================================================================================
# Put data into VAL/ROW/PTR
#=================================================================================
def storeData(matrix, out_file):
    VAL = []
    COL = []
    PTR = [0]*len(matrix)
    PTR[0] = 0

    for row in matrix:                              # row is a list of one matrix column non-zero data
        random.shuffle(row)
        for cell in row:
            i = cell[0]
            j = cell[1]
            VAL.append(cell[2])                     # put data into VAL/ROW/PTR
            COL.append(j - 1)
            PTR[i] += 1
             
            
    # process PTR
    for i in range(1, len(PTR)):              #******!!!!!! change from 2 -> 1
        PTR[i] += PTR[i-1]

    # output
    import sys
    with open(out_file, 'w') as fh:
        sys.stdout = fh
        print ("%BEGIN PTR", len(PTR))
        for val in PTR:
            print (val)
        print ("%BEGIN VAL", len(VAL))
        for val in VAL:
            print (val)
        print ("%BEGIN COL", len(COL))
        for val in COL:
            print (val)
        
            
#=================================================================================
# Main
#=================================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sparse Matrix Parser')
    parser.add_argument('--input', type=str, help='input data file')
    args = parser.parse_args()
  
    matrix = readInput(args.input)
    #debug(matrix)
    storeData(matrix, args.input + ".out")
