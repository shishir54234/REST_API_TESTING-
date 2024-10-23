#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
  int rank, size;
  int left, right;
  int sendbuf[2], recvbuf[2];

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  // Compute left and right neighbors with periodic boundary conditions
  left = (rank - 1 + size) % size;
  right = (rank + 1) % size;

  // Initialize send buffer with rank
  sendbuf[0] = rank;
  sendbuf[1] = rank + 1;

  // Send and receive data with periodic boundary conditions
  MPI_Sendrecv(sendbuf, 2, MPI_INT, right, 0, recvbuf, 2, MPI_INT, left, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

  // Print results
  printf("Process %d sent (%d, %d) to process %d and received (%d, %d) from process %d\n",
         rank, sendbuf[0], sendbuf[1], right, recvbuf[0], recvbuf[1], left);

  MPI_Finalize();
  return 0;
}

// mpicc -o send_recv_periodic send_recv_periodic.c
// And then run it with:
// mpirun -n 4 ./send_recv_periodic
