#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <cuda.h>
#define N (1024)

texture<float> tex_a;
texture<float> tex_b;
texture<float> tex_c;

// CUDA kernel. Each thread takes care of one element of c
__global__ void vecAdd(float *c)
{
    // Get our global thread ID
    int id = blockIdx.x*blockDim.x+threadIdx.x;
    // Make sure we do not go out of bounds
   // if (id < N) {
		
		c[id] = tex1Dfetch(tex_a,id) + tex1Dfetch(tex_b,id);
//	}
        
}

int main( int argc, char* argv[] )
{
    // Size of vectors
    //int n = 10000;
	
    // Host input vectors
    float *h_a;
    float *h_b;
    //Host output vector
    float *h_c;
	
    // Device input vectors
    float *d_a;
    float *d_b;
    //Device output vector
    float *d_c;
	
    // Size, in bytes, of each vector
    size_t bytes = N*sizeof(float);
	
    // Allocate memory for each vector on host
    h_a = (float*)malloc(bytes);
    h_b = (float*)malloc(bytes);
    h_c = (float*)malloc(bytes);
	// Allocate memory for each vector on GPU
    cudaMalloc(&d_a, bytes);
    cudaMalloc(&d_b, bytes);
    cudaMalloc(&d_c, bytes);
	
    int i;
    // Initialize vectors on host
    for( i = 0; i < N; i++ ) {
        h_a[i] = sin(i)*sin(i);
        h_b[i] = cos(i)*cos(i);
		//h_c[i] = 0.0f;
    }
	// bind to texture memory
	cudaBindTexture( NULL, tex_a,
					 d_a,
					 bytes );
	cudaBindTexture( NULL, tex_b,
					 d_b,
					 bytes );
	cudaBindTexture( NULL, tex_c,
					 d_c,
					 bytes );
    // Copy host vectors to device
    cudaMemcpy( d_a, h_a, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy( d_b, h_b, bytes, cudaMemcpyHostToDevice);
	
	
    int blockSize, gridSize;
	
    // Number of threads in each thread block
    blockSize = 1024;
	
    // Number of thread blocks in grid
    gridSize = (int)ceil((float)N/blockSize);
	
    // Execute the kernel
    vecAdd<<<gridSize, blockSize>>>(d_c);
	
    // Copy array back to host
    cudaMemcpy( h_c, d_c, bytes, cudaMemcpyDeviceToHost );
	
    // Sum up vector c and print result divided by n, this should equal 1 within error
    float sum = 0;
    for(i=0; i<N; i++)
        sum += h_c[i];
    printf("final result: %f\n", sum/N);
	
    // Release device memory
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
	
    // Release host memory
    free(h_a);
    free(h_b);
    free(h_c);
	return 0;
}