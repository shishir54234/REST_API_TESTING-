#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

double f(double x) {
  return 4.0 / (1.0 + x*x);
}

int main(int argc, char** argv) {
  int rank, size, tag = 0;
  double pi, sum, local_sum, x;
  int n = 1000000;
  double start_time, end_time;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  start_time = MPI_Wtime();

  local_sum = 0.0;
  for (int i = rank; i < n; i += size) {
    x = (i + 0.5) / n;
    local_sum += f(x);
  }

  MPI_Reduce(&local_sum, &sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    pi = sum / n;
    printf("Approximation of pi is: %lf\n", pi);
  }

  end_time = MPI_Wtime();
  if (rank == 0) {
    printf("Time elapsed: %lf seconds\n", end_time - start_time);
  }

  MPI_Finalize();
  return 0;
}

// mpicc -o pi_mpi pi_mpi.c -lm
// mpirun -np 4 ./pi_mpi


