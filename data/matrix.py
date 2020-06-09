import re
import numpy

fn = './bcsstk15/bcsstk15.mtx'

in_fh = open(fn, 'r')
out_fh = open('log', 'w')

M = 0
N = 0
NUM = 0
VAL = []

for line in in_fh:
    line = line.strip()
    if re.match("^\%", line):
        continue
    
    if NUM == 0:
        toks = line.split(' ')
        M = int(toks[0])
        N = int(toks[1])
        NUM = int(toks[2])
        VAL = [[0]*N]*M
        
    else:
        toks = line.split(' ')
        i = int(toks[0])
        j = int(toks[1])
        #print("[" + line + "]\n")
        VAL[i-1][j-1] = float(toks[2])
in_fh.close()
out_fh.close()
    

