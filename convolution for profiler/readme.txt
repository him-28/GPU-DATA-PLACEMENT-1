Sample: CUDA Separable Convolution
Minimum spec: GeForce 8

This sample implements a separable convolution filter of a 2D signal with a gaussian kernel.
Usuage:
	make all	-> build all executable.
	make nvprof -> output profiling results.
	make cuobjdump -> output ptx, sass and elf results.

file		S_Data		D_Dst		D_Src		c_Kernel	Kernel-Execution-time			
															(Row)		(Column)
3.cu		Shared		Global		2Dtexture	Constant	1.5757ms	1.3252ms
4.cu		Shared		Global		1Dtexture	Constant	1.6040ms	1.3447ms
6.cu		Shared		Global		Global		Global		9.5030ms	9.5014ms
7.cu		Shared		Global		Global		Constant	1.8963ms	1.3445ms
8.cu		Shared		Global		Global		1Dtexture	1.9092ms	1.3719ms
9.cu		Shared		Global		Global		Shared		3.3111ms	3.1719ms

Key concepts:

1. convolution_index.cu: Profiling(To support -arch=sm_20, can only be run on ulmo)          (./convolution_index)
2. convolution.cu:  original one(c_Kernel in constant memory, d_Src in global memory); ulmo:Time = 0.00281 s, gpu1:0.00299 s (./convolution)
3. 1.cu:  c_Kernel and d_Src are in global memory; ulmo: Time = 0.01463 s, gpu1:0.07275 s  (./1)
4. 2.cu:  small size(c_Kernel and d_Src are in constant memory); ulmo: Time = 0.00004 s, gpu1:0.00004 s (./2)
    2_re.cu: small size of original one(c_Kernel in constant memory, d_Src in global memory); ulmo: Time = 0.00002 s, gpu1:0.00002 s (./2_re)
5. 3.cu:  BEST ONE(c_Kernel in constant memory, d_Src in texture memory);  ulmo: Time = 0.00250 s,gpu1:0.00331 s (./3)
6. 4.cu:  small size(c_Kernel in global memory, d_Src in constant memory); ulmo: Time = 0.00004 s,gpu1:0.00005 s (./4)
7. 5.cu:  c_Kernel in texture memory, d_Src in global memory; ulmo: Time = 0.00279 s, gpu1:0.00734 s   (./5)
