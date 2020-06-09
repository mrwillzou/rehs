#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <omp.h>
#include <time.h> 

int DEBUG = 1;

int splitLine (char* line, char toks[3][36]) {
  int n = 0, i = 0, j = 0;
	
  for(i = 0; 1 ; i++) {
    if (line[i] == '\n') {
      line[i] = '\0';
    }
    if(line[i] != ' '){
      toks[n][j++] = line[i];
    } else{
      toks[n][j++]='\0'; // end of a tok
      n++;
      j=0;
    }
    if(line[i] == '\0') {
      break;
    }
  }  
  return n;
}


int populate (char* matrix_file, int** PTR, double** VAL, int** COL) {
  FILE* fp;
  
  char* line = NULL;
  char toks[3][36];
  size_t len = 0;
  ssize_t read;
  int cnt = 0;
  double val;
  
  int data_type = -1;
  int N = 0;

  printf ("Info: read maxtrix file: %s\n", matrix_file);  
  fp = fopen(matrix_file, "r");
  //--------exception case file not found------------------
  if (fp == NULL) {
    printf("ERROR: open file FAILED: %s\n", matrix_file);
    exit(1);
  }
  //-------------------------------------------------------

  while ((read = getline(&line, &len, fp)) != -1) {
    // comment line % ==> get data type and size
    if (line[0] == '%') {
      splitLine(line, toks);
      // based on data size, allocate memory
      N = atoi(toks[2]);      
      cnt = 0;

      if (strcmp(toks[1], "VAL") == 0) {
	data_type = 1;
	*VAL = (double*) malloc(N * sizeof(double));
      } else if (strcmp(toks[1], "COL") == 0) {
	data_type = 2;
	*COL = (int*)    malloc(N * sizeof(int));
      } else if (strcmp(toks[1], "PTR") == 0) {
	data_type = 3;
	*PTR = (int*)    malloc(N * sizeof(int));
      } else {
	printf("Error: invalid input file: %s\n", matrix_file);
      }
      
      continue;
    }

    if (data_type == 1) {
      (*VAL)[cnt] = atof(line);
    }
    else if (data_type == 2) {
      (*COL)[cnt] = atoi(line);
    }
    else if (data_type == 3) {
      (*PTR)[cnt] = atoi(line);
    }
    cnt++;
  }

  fclose(fp);
  return 0;
}

int getVEC (char* vector_file, int** VEC) {
  FILE* fp;

  char* line = NULL;
  char toks[3][36];
  size_t len = 0;
  ssize_t read;
  int cnt = 0;
  double val;

  int data_type = -1;
  int N = 0;

  printf ("Info: read vector file: %s\n", vector_file);
  fp = fopen(vector_file, "r");
  //--------exception case file not found------------------
  if (fp == NULL) {
    printf("ERROR: open file FAILED: %s\n", vector_file);
    exit(1);
  }
  //-------------------------------------------------------

  while ((read = getline(&line, &len, fp)) != -1) {
    // comment line % ==> get data type and size
    if (line[0] == '%') {
      splitLine(line, toks);
      // based on data size, allocate memory
      N = atoi(toks[2]);      
      cnt = 0;
      
      if (strcmp(toks[1], "VEC") == 0) {
	data_type = 1;
	*VEC = (int*) malloc(N * sizeof(int));                //allocate VEC
      } else {
	printf("Error: invalid input file: %s\n", vector_file);
      }
      continue;
    }

    if (data_type == 1) {
      (*VEC)[cnt] = atoi(line);
    }
    cnt++;
  }
  
  fclose(fp);
  return N;
}

int calculate(int N, double** PROD, int* VEC, int* PTR, double* VAL, int* COL) {
  *PROD = (double*) malloc(N * sizeof(double));
  for (int k = 0; k < 10; k++) {
    for (int k = 0; k < N; k++) {
      (*PROD)[k] = 0.0;
    }
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {               // <-- NULL array
      for (int j = PTR[i]; j < PTR[i + 1]; j++) {
	(*PROD)[i] = (*PROD)[i] + (VAL[j] * VEC[COL[j]]);
	//(*PROD)[i] = (*PROD)[i] + (VAL[j]);
      }
    }
  }
  return 0;
}

//=======================================================================
//MAIN
//=======================================================================

int main (int argc, char** argv) {

  double* VAL = NULL;
  int* COL = NULL;
  int* PTR = NULL;
  int* VEC = NULL;
  double* PROD = NULL;
  int N = 0;
  int i = 0;

  double total_time;  //timer

  
  char* matrix_file = argv[1];
  char* vector_file = argv[2]; 

  populate(matrix_file, &PTR, &VAL, &COL);
  N = getVEC(vector_file, &VEC);
  
  PROD = (double*) malloc(N * sizeof(double));         //allocate PROD
  //-------timer start---------
 
  calculate(N, &PROD, VEC, PTR, VAL, COL);
  total_time = omp_get_wtime();
  
  //-------timer end------------
  printf ("Info: SPMV product:\n");
  for (int i = 0; i < N; i++) {
    printf("%.2f\n", PROD[i]);
  }

  printf("runtime: %f sec \n", total_time/10);

  if (VAL)
    free(VAL);
  if (COL)
    free(COL);
  if (PTR)
    free(PTR);
  if (VEC)
    free(VEC);
  if (PROD)
    free(PROD);
}




  

  
