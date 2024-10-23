#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

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
  int matrix1[MATRIX_SIZE][MATRIX_SIZE];
  int matrix2[MATRIX_SIZE][MATRIX_SIZE];
  int result[MATRIX_SIZE][MATRIX_SIZE];

  srand(time(NULL));

  // Initialize matrices
  for (int i = 0; i < MATRIX_SIZE; i++) {
    for (int j = 0; j < MATRIX_SIZE; j++) {
      matrix1[i][j] = rand() % 10;
      matrix2[i][j] = rand() % 10;
    }
  }

  // Print matrices
  printf("Matrix 1:\n");
  print_matrix(matrix1, MATRIX_SIZE);
  printf("Matrix 2:\n");
  print_matrix(matrix2, MATRIX_SIZE);

  // Multiply matrices using OpenMP
  #pragma omp parallel for
  for (int i = 0; i < MATRIX_SIZE; i++) {
    for (int j = 0; j < MATRIX_SIZE; j++) {
      int sum = 0;
      for (int k = 0; k < MATRIX_SIZE; k++) {
        sum += matrix1[i][k] * matrix2[k][j];
      }
      result[i][j] = sum;
    }
  }

  // Print result
  printf("Result:\n");
  print_matrix(result, MATRIX_SIZE);

  return 0;
}


// gcc -fopenmp -o matrix_mult_openmp matrix_mult_openmp.c
// And then run it with:
// ./matrix_mult_openmp
