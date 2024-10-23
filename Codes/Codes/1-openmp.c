#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

double f(double x) {
  return 4.0 / (1.0 + x*x);
}

int main(int argc, char** argv) {
  int num_threads = 4;
  int n = 1000000;
  double pi, sum = 0.0, x, start_time, end_time;

  omp_set_num_threads(num_threads);

  start_time = omp_get_wtime();

  #pragma omp parallel for private(x) reduction(+:sum)
  for (int i = 0; i < n; i++) {
    x = (i + 0.5) / n;
    sum += f(x);
  }

  pi = sum / n;

  end_time = omp_get_wtime();

  printf("Approximation of pi is: %lf\n", pi);
  printf("Time elapsed: %lf seconds\n", end_time - start_time);

  return 0;
}

// gcc -o pi_omp pi_omp.c -fopenmp -lm
// ./pi_omp
