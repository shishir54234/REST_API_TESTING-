#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

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

int main(int argc, char** argv) {
  int num_threads = 4;
  int array[ARRAY_SIZE];

  srand(time(NULL));

  // Generate random numbers
  for (int i = 0; i < ARRAY_SIZE; i++) {
    array[i] = rand() % 100;
  }

  omp_set_num_threads(num_threads);

  // Sort array using OpenMP
  #pragma omp parallel
  {
    int thread_num = omp_get_thread_num();
    int num_threads = omp_get_num_threads();
    int chunk_size = ARRAY_SIZE / num_threads;
    int start_index = thread_num * chunk_size;
    int end_index = (thread_num + 1) * chunk_size;

    if (thread_num == num_threads - 1) {
      end_index = ARRAY_SIZE;
    }

    bubble_sort(&array[start_index], end_index - start_index);
  }

  // Merge sorted subarrays
  int temp[ARRAY_SIZE];
  int chunk_size = ARRAY_SIZE / num_threads;

  for (int i = 1; i < num_threads; i++) {
    int start_index = i * chunk_size;
    int end_index = (i + 1) * chunk_size;

    if (i == num_threads - 1) {
      end_index = ARRAY_SIZE;
    }

    int i1 = 0;
    int i2 = start_index;
    int i3 = start_index;

    while (i1 < chunk_size && i2 < end_index) {
      if (array[i2] < array[i3]) {
        temp[i1++] = array[i2++];
      } else {
        temp[i1++] = array[i3++];
      }
    }

    while (i2 < end_index) {
      temp[i1++] = array[i2++];
    }

    while (i3 < end_index) {
      temp[i1++] = array[i3++];
    }

    for (int j = 0; j < i1; j++) {
      array[start_index+j] = temp[j];
    }
  }

  // Print sorted array
  printf("Sorted array:\n");
  for (int i = 0; i < ARRAY_SIZE; i++) {
    printf("%d ", array[i]);
  }
  printf("\n");

  return 0;
}

// gcc -o sort_omp sort_omp.c -fopenmp
// ./sort_omp

