#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define ARRAY_SIZE 1000

void merge(int *array, int left, int mid, int right) {
    int i, j, k;
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int L[n1], R[n2];

    for (i = 0; i < n1; i++) {
        L[i] = array[left + i];
    }
    for (j = 0; j < n2; j++) {
        R[j] = array[mid + 1 + j];
    }

    i = 0;
    j = 0;
    k = left;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            array[k] = L[i];
            i++;
        } else {
            array[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        array[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        array[k] = R[j];
        j++;
        k++;
    }
}

void merge_sort(int *array, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        merge_sort(array, left, mid);
        merge_sort(array, mid + 1, right);
        merge(array, left, mid, right);
    }
}


int main(int argc, char** argv){
    int size, rank;
    int arr[ARRAY_SIZE];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    for(int i=0;i<ARRAY_SIZE;i++)
    {
        arr[i] = rand()%10 + 1;
    }
    int local_n = ARRAY_SIZE / size;
    int *local_array = (int *)malloc(sizeof(int) * local_n);

    MPI_Scatter(arr, local_n, MPI_INT, local_array, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    merge_sort(local_array, 0, local_n - 1);

    int *sorted_array = NULL;
    if (rank == 0) {
        sorted_array = (int *)malloc(sizeof(int) * ARRAY_SIZE);
    }

    MPI_Gather(local_array, local_n, MPI_INT, sorted_array, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        int l = 0;
        for(int mid=local_n-1;mid<ARRAY_SIZE-local_n;mid+=local_n)
        {
            merge(sorted_array, l, mid, mid+local_n);
        }

        printf("Sorted array:\n");
        for (int i = 0; i < ARRAY_SIZE; i++) {
            printf("%d ", sorted_array[i]);
        }
        printf("\n");
    }

    MPI_Finalize();
    return 0;

}