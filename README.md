# rehs
code is located in /src

#==================================================================================

CRS.py :: converts coordinate form to Compressed Row form CRS_random.py :: converts to compressed row format with randomized columns

VEC.py :: initializes an array/vector of size N contaiing random integers (1-9)

spmv_timer.c :: performs the sparse matrix vector multiplication #==================================================================================

CALLING FUNCTIONS:

***file path example for matrix - ../data/matrix

./CRS.py --input ../data/matrix (output file is written in ../data/matrix.out) **OR ./CRS_random.py --input ../data/matrix (output file is written in ../data/matrix.out) ***(randomized)

./VEC.py --input ../data/matrix (output file is written in ../data/matrix/vector)

gcc -fopenmp -o execute ./spmv_timer.c (compile spmv code) ./execute ../data/matrix.out ../data/matrix.vector
