#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

double function(double num){
    return 4.0 / (1.0 + num*num);
}

int main(int argc, char** argv){
    int rank, num_threads;
    double sum_total;
    int iterations = 100000;

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_threads);

    double sum_local = 0.0;

    for(int i = 0; i < iterations; i += num_threads){
        double x = (i + 0.0) / iterations;
        sum_local += function(x);
    }

    MPI_Reduce(&sum_local, &sum_total, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if(rank == 0){
        double answer = sum_total / iterations;
        printf("Value of pi: %lf\n", answer);
    }

    MPI_Finalize();
}