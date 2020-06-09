#!/usr/bin/python3

import re
import argparse
import random

def splitLine (line):
    toks = line.split(' ')
    return [int(toks[0]), int(toks[1]), float(toks[2])]

def readInput(in_file):
    fh = open(in_file)
    N = 0
    for line in fh:
        if re.match("%", line):
            continue

        if N == 0:
            cell = splitLine(line)
            N = cell[1]
            fh.close()
            return N

        else:
            fh.close()
            return 0

def createVec(num, out_file):
    VEC = []
    for i in range(num):
        #VEC.append(1)
        VEC.append(random.randint(1, 9))

    import sys
    with open(out_file, 'w') as fh:
        sys.stdout = fh
        print("%BEGIN VEC", len(VEC))
        for val in VEC:
            print(val)

#===============================================
#MAIN
#===============================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sparse Matrix Parser')
    parser.add_argument('--input', type=str, help='input data file')
    args = parser.parse_args()

    num = readInput(args.input)
    createVec(num, args.input + ".vector") 
    
