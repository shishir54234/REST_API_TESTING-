#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

#define ARRAY_SIZE 1000

int main(int argc, char** argv) {
  int rank, size;
  int array[ARRAY_SIZE];
  int sum = 0;
  int product = 1;
  int max = 0;
  int min = 10;

  MPI_Init(NULL, NULL);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  // Generate random numbers
  srand(time(NULL) + rank);
  for (int i = 0; i < ARRAY_SIZE; i++) {
    array[i] = rand() % 10;
  }

  // Compute sum, product, max, and min
  for (int i = 0; i < ARRAY_SIZE; i++) {
    sum += array[i];
    product *= array[i];
    if (array[i] > max) {
      max = array[i];
    }
    if (array[i] < min) {
      min = array[i];
    }
  }

  // Reduce results across all processes
  int global_sum, global_product, global_max, global_min;
  MPI_Reduce(&sum, &global_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
  MPI_Reduce(&product, &global_product, 1, MPI_INT, MPI_PROD, 0, MPI_COMM_WORLD);
  MPI_Reduce(&max, &global_max, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);
  MPI_Reduce(&min, &global_min, 1, MPI_INT, MPI_MIN, 0, MPI_COMM_WORLD);

  // Print results on process 0
  if (rank == 0) {
    printf("Array:\n");
    for (int i = 0; i < ARRAY_SIZE; i++) {
      printf("%d ", array[i]);
    }
    printf("\n\n");
    printf("Sum: %d\n", global_sum);
    printf("Product: %d\n", global_product);
    printf("Max: %d\n", global_max);
    printf("Min: %d\n", global_min);
  }

  MPI_Finalize();
  return 0;
}

// mpicc -o random_numbers_mpi random_numbers_mpi.c
// And then run it with:
// mpirun -n 4 ./random_numbers_mpi
