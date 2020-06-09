#!/usr/bin/python3

import re

fn = './bcsstk15/test.mtx'
#fn = './bcsstk15/bcsstk15.mtx'       #matrix file
in_fh = open(fn, 'r')                #input read file 

M = 0         # number of rows
N = 0         # number of columns
NUM = -1      # total number of non-zero values from input file
dline = 0     # whuch data line the code is on / index of VAL and ROW lists 
LEN = 0

VAL = []      # list of all non-zero values in sequence
ROW = []      # corresponding row index for the value in the VAL
PTR = []      # count of non-zero values per column
              # PTR[5] refers to the total non-zero so far

curr_col = 0  # column number / for loop iteration 
cnt_non_0 = 0 # number of nonzeros per column

diag_cnt = 0  #number of nonzeros on the diagonal

for line in in_fh:                  #***function to determine the number of nonzeros on the diagonal
    line = line.strip()
    if re.match("^\%", line):
        continue
    if NUM == 0:
        NUM+=1
        continue
    else:
        toks = line.split(' ')
        if toks[0] == toks[1]:
            diag_cnt+=1             #***
in_fh.close()

in_fh = open(fn, 'r')       #re-open

for line in in_fh:
    line = line.strip()
    if re.match("^\%", line):           # ignore comment line
        continue

    # decode 1st to extract number of rows and number of columns
    if NUM == 0:                        #store matrix dimensions and initialize PTR[]
        toks = line.split(' ')
        M = int(toks[0])
        N = int(toks[1])
        NUM = int(toks[2])
        LEN = 2*NUM - diag_cnt 

        VAL = [0]*LEN          #initialize VAL   (len = 2nnz - diag_cnt)
        ROW = [0]*LEN          #initialize ROW
        
        PTR = [0]*(M+1)        #initialize PTR   (len = m+1)
        PTR[0] =  1            # 1st index default to 1

        
    # a matrix data point from input file
    else:
        toks = line.split(' ')
        i = int(toks[0]) 
        j = int(toks[1])
        val = float(toks[2])   # matrix value (i,j,val)

        # *** when column change ***
        if j != curr_col:
            print(curr_col)
            PTR[curr_col] += cnt_non_0 + PTR[curr_col - 1]            
            curr_col = j       # change current column
            cnt_non_0 = 0      # reset count to 0

        # (i,j,val)
        VAL[dline] = val        # add value and row number
        ROW[dline] = i
        cnt_non_0 += 1
        
        # (j,i,val): handle symmetric value point
        if i != j:             # if it does not lie on the diagonal
            VAL[LEN - dline - 1] = val    # adding symmetric value (j,i,val)
            ROW[LEN - dline - 1] = j
            PTR[i] += 1        # here i refers to the symmetric point column

        dline += 1       #end of interation increment dline

        
# *** handle after last line in input file ***
print(curr_col)
PTR[curr_col] += cnt_non_0 + PTR[curr_col - 1]
in_fh.close()

with open('log.txt', 'w') as f:
    f.write("=== VAL ======================================================\n")        
    for item in VAL:
        f.write(str(item)+"\n")
    f.write("=== ROW ======================================================\n")
    for item in ROW:
        f.write(str(item)+"\n")
    f.write("=== PTR ======================================================\n")        
    for item in PTR:
        f.write(str(item)+"\n")
f.close()
