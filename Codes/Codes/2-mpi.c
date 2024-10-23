#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

#define ARRAY_SIZE 1000

void bubble_sort(int array[], int size) {
  for (int i = 0; i < size - 1; i++) {
    for (int j = 0; j < size - 1 - i; j++) {
      if (array[j] > array[j+1]) {
        int temp = array[j];
        array[j] = array[j+1];
        array[j+1] = temp;
      }
    }
  }
}

void merge(int array[], int size, int temp[]) {
  int i = 0;
  int j = size / 2;
  int k = 0;

  while (i < size / 2 && j < size) {
    if (array[i] <= array[j]) {
      temp[k++] = array[i++];
    } else {
      temp[k++] = array[j++];
    }
  }

  while (i < size / 2) {
    temp[k++] = array[i++];
  }

  while (j < size) {
    temp[k++] = array[j++];
  }

  for (int i = 0; i < size; i++) {
    array[i] = temp[i];
  }
}

int main(int argc, char** argv) {
  int rank, size, tag = 0;
  int array[ARRAY_SIZE];
  int temp[ARRAY_SIZE];
  int subarray_size = ARRAY_SIZE / 2;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  srand(time(NULL) + rank);

  // Generate random numbers
  for (int i = 0; i < ARRAY_SIZE; i++) {
    array[i] = rand() % 100;
  }

  // Sort local subarray
  bubble_sort(array, subarray_size);

  // Exchange and merge sorted subarrays
  for (int i = 1; i < size; i *= 2) {
    if (rank % (2*i) == 0) {
      if (rank + i < size) {
        MPI_Send(&array[subarray_size], subarray_size, MPI_INT, rank+i, tag, MPI_COMM_WORLD);
        MPI_Recv(&temp[subarray_size], subarray_size, MPI_INT, rank+i, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        merge(array, ARRAY_SIZE, temp);
      }
    } else {
      MPI_Recv(&temp[0], subarray_size, MPI_INT, rank-i, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      MPI_Send(&array[0], subarray_size, MPI_INT, rank-i, tag, MPI_COMM_WORLD);
      merge(array, ARRAY_SIZE, temp);
    }
  }

  if (rank == 0) {
    // Print sorted array
    printf("Sorted array:\n");
    for (int i = 0; i < ARRAY_SIZE; i++) {
      printf("%d ", array[i]);
    }
    printf("\n");
  }

  MPI_Finalize();
  return 0;
}

// mpicc -o sort_mpi sort_mpi.c
// mpirun -np 4 ./sort_mpi
