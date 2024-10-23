#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define MATRIX_SIZE 10

void print_matrix(int matrix[][MATRIX_SIZE], int size) {
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      printf("%d ", matrix[i][j]);
    }
    printf("\n");
  }
  printf("\n");
}

int main(int argc, char** argv) {
  int rank, size, i, j, k, sum;
  int matrix1[MATRIX_SIZE][MATRIX_SIZE];
  int matrix2[MATRIX_SIZE][MATRIX_SIZE];
  int result[MATRIX_SIZE][MATRIX_SIZE];

  MPI_Init(NULL, NULL);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  if (size != 1) {
    printf("This program is designed to run with 1 process\n");
    MPI_Finalize();
    exit(1);
  }

  // Initialize matrices
  srand(time(NULL));
  for (i = 0; i < MATRIX_SIZE; i++) {
    for (j = 0; j < MATRIX_SIZE; j++) {
      matrix1[i][j] = rand() % 10;
      matrix2[i][j] = rand() % 10;
    }
  }

  // Print matrices
  printf("Matrix 1:\n");
  print_matrix(matrix1, MATRIX_SIZE);
  printf("Matrix 2:\n");
  print_matrix(matrix2, MATRIX_SIZE);

  // Multiply matrices
  for (i = 0; i < MATRIX_SIZE; i++) {
    for (j = 0; j < MATRIX_SIZE; j++) {
      sum = 0;
      for (k = 0; k < MATRIX_SIZE; k++) {
        sum += matrix1[i][k] * matrix2[k][j];
      }
      result[i][j] = sum;
    }
  }

  // Print result
  printf("Result:\n");
  print_matrix(result, MATRIX_SIZE);

  MPI_Finalize();
  return 0;
}

// mpicc -o matrix_mult_mpi matrix_mult_mpi.c
// And then run it with:
// mpirun -np 1 ./matrix_mult_mpi

