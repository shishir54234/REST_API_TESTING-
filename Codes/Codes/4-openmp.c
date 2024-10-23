#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#define ARRAY_SIZE 1000

int main(int argc, char** argv) {
  int array[ARRAY_SIZE];
  int sum = 0;
  int product = 1;
  int max = 0;
  int min = 10;

  srand(time(NULL));

  // Generate random numbers
  #pragma omp parallel for
  for (int i = 0; i < ARRAY_SIZE; i++) {
    array[i] = rand() % 10;
  }

  // Compute sum, product, max, and min
  #pragma omp parallel for reduction(+:sum) reduction(*:product) reduction(max:max) reduction(min:min)
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

  // Print results
  printf("Array:\n");
  for (int i = 0; i < ARRAY_SIZE; i++) {
    printf("%d ", array[i]);
  }
  printf("\n\n");
  printf("Sum: %d\n", sum);
  printf("Product: %d\n", product);
  printf("Max: %d\n", max);
  printf("Min: %d\n", min);

  return 0;
}

// gcc -fopenmp -o random_numbers_omp random_numbers_omp.c
// And then run it with:
// ./random_numbers_omp
