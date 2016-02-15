#!/usr/bin/python

"""
usage: ./analysis.py *.txt dimension 
"""

import sys
import os
import re
from itertools import *
import time
import math
start = time.time()
alfa = 1
dimension =[]# [2,2,2]
sizeof = []#[4, 4, 4]
block_X = []#[3072,3072,3072]
block_Y = []#[256,256,256]
array_size = []
stride = []
for line in open(sys.argv[10],'r'):
 thread = line.strip()
 if thread[0].isdigit():
  thread = thread.split()
  for x in range(0,len(thread)):
   thread[x] = int(thread[x])
  stride.append(thread)
 elif  thread[0] == '[':
  while thread[0]!= ':':
   thread = thread[1:]
  thread = thread[1:]
  thread = thread.split()
  for x in range(0,len(thread)):
   thread[x] = int(thread[x])
  stride.append(thread)
 else:
  thread = thread.split()
  for i in range(1,len(thread)):
   thread[i] = int(thread[i])
  if thread[0] == "dimension":
   dimension = thread[1:]
  elif thread[0]=="sizeof":
   sizeof = thread[1:]
  elif thread[0] =="block_X":
   block_X = thread[1:]
  elif thread[0] == "block_Y":
   block_Y = thread[1:]
  elif thread[0] == "array_size":
   array_size = thread[1:]
  else:
   continue 
out = open("output.txt",'a')
flag = 0
for x in sizeof:
 if x > 4:
  flag = 1
if flag == 1:
 printout = "texture2D"
 for x in sizeof:
  printout+=" 99999999 0 0"
 printout += " \n"
 out = open("output.txt",'a')
 out.close()
 sys.exit(0)
stride.sort(
key = lambda l:(l[0],l[1],l[2],l[3],l[5])
)
end = time.time()
print end - start
print("###########################")
print("          Texture  Memory   2D              ")
print("###########################")
size_1D = int(sys.argv[1])
size_2D = int(sys.argv[2])

con_lat = int(sys.argv[3])
L2_size = int(sys.argv[4])
L2_cache_line = int(sys.argv[5])
L2_lat = int(sys.argv[6])
L1_size = int(sys.argv[7])
L1_cache_line = int(sys.argv[8])
L1_lat = int(sys.argv[9])
if L2_cache_line < L1_cache_line:
 L2_cache_line = L1_cache_line
if L2_size == 0:
 L2_cache_line = sizeof[0]
if L1_size == 0:
 L1_cache_line = sizeof[0]
 L1_cache_line = L2_cache_line
#L1_cache_line = 128
#L1_size = 12*1024
#L2_cache_line = 256
#L2_size = 768*1024
if L2_cache_line < L1_cache_line:
 L2_cache_line = L1_cache_line


x=0
printout = "texture2D "
array = int(stride[x][0])
array_next = array
rw = int(stride[x][1])
exp = int(stride[x][2])
loop = int(stride[x][3])
index = int(stride[x][5])
warp = int(stride[x][4])
print1 = 0
cache_line = L1_cache_line
add = 0
#array_total=[]
flag = 0
total = 0
total_cache_line=0
access = []
access_cache_line = []
collect = []
collect_cache_line = []
collect_array = []
L1 = []
L2 = []
L1_hit = 0
L2_hit = 0
L1_position = []
L2_position = []
L1_cache_len = int(math.sqrt(L1_cache_line/sizeof[array])/4)*4
L2_cache_len = int(math.sqrt(L2_cache_line/sizeof[array])/4)*4
L1_lines = L1_size/(L1_cache_len*L1_cache_len)
L2_lines = L2_size/(L2_cache_len*L2_cache_len)
#n =0
#kong_set = []
#L1_x = int(math.sqrt(L1_cache_line/sizeof[n])/4)*4
"""for i in range(0,(block_X[n] +L1_x-1)/L1_x):
 xi = []
 for j in range(0,(block_Y[n]+L1_x-1)/L1_x):
  xi.append(0)
 kong_set.append(xi)
"""
def kong(n):
 start = time.time()
 L1_x = int(math.sqrt(L1_cache_line/sizeof[n])/4)*4
 kong_set1 = [[0 for col in range(0,(block_Y[n] +L1_x-1)/L1_x)] for row in range(0,(block_X[n] +L1_x-1)/L1_x)]
 end = time.time()
 print end-start,n
 return kong_set1

#kong_set2 = []
#L2_x = int(math.sqrt(L2_cache_line/sizeof[n])/4)*4
"""for i in range(0,(block_X[n]+L2_x-1)/L2_x):
 xi = []
 for j in range(0,(block_Y[n]+L2_x -1)/L2_x):
  xi.append(0)
 kong_set2.append(xi) """
def kong_L2(n):
 start = time.time()
 L2_x = int(math.sqrt(L2_cache_line/sizeof[n])/4)*4
 kong_set1 = [[0 for col in range(0,(block_Y[n] +L2_x-1)/L2_x)] for row in range(0,(block_X[n] +L2_x-1)/L2_x)]
 end =time.time()
 print end-start,"L2", n
 return kong_set1
collect_array_N = []
L1_list = []
L2_list = []
L1_transform = 0
L2_transform = 0
index_transform = 0
while x<len(stride):
 array_next = int(stride[x][0])
 rw_next = int(stride[x][1])
 exp_next = int(stride[x][2])
 loop_next = int(stride[x][3])
 warp_next = int(stride[x][4])
 index_next = int(stride[x][5])
 x = x + 1 
 #if (x==1):
  #collect_array = kong(0)
  #collect_array_N =[]
  #L1 = kong(0)
  #L2 = kong_L2(0)
  

 if (array == array_next):
  if(rw_next == 0):
   """ if print1 == 1:
    collect_array=kong(array_next)
    temporal_hit = 0
    temporal_cache = kong(array_next)
    L1_hit = 0
    L2_hit = 0
    L1 = kong(array_next)
    L2 = kong_L2(array_next)
    print1 = 0 """
   
   if (exp == exp_next):

    if (loop == loop_next):
     if ((warp/32) == (warp_next/32)):
      if index_next not in collect:
       collect.append(index_next)
       index = index_next
      index_transform= (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
      if index_transform not in collect_array_N:#(collect_array[(index_next%block_X[array])/L1_cache_len][(index_next/block_X[array])/L1_cache_len]!=1):
       collect_array_N.append(index_transform)
       L1_transform = (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
       if L1_transform in L1_list:#(L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]==1):
        L1_list.append(L1_transform)
        #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
        #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
        
        if math.fabs(L1_list.index(L1_transform)-len(L1_list))<=L1_lines:#if math.fabs(L1_position.index(position)-len(L1_position))<=L1_lines:
         L1_hit += 1 
        L1_list.remove(L1_transform)
        L1_list.append(L1_transform)
        
       else:
        L1_transform = (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
        #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
        #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
        if L1_transform  in L1_list:#L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]==1:
         L1_list.remove(L1_transform)
        L1_list.append(L1_transform)
        L2_transform = (index_next%block_X[array_next])/L2_cache_len *size_1D+(index_next/block_X[array_next])/L2_cache_len*size_2D
        if L2_transform in L2_list:#(L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]==1):
         #L2_x = int(math.sqrt(L2_cache_line/sizeof[array_next])/4)*4
         #position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_x-1)/L1_x) + ((index_next%block_X[array_next])/L2_cache_len)
        
         if math.fabs(L2_list.index(L2_transform)-len(L2_list))<=L2_lines:
          L2_hit += 1 
         L2_list.remove(L2_transform)
         L2_list.append(L2_transform)
        else:
         #position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_cache_len-1)/L2_cache_len) + ((index_next%block_X[array_next])/L2_cache_len)
         L2_list.append(L2_transform)
        
      
       
        
       
      #collect_array[(index_next%block_X[array])/L1_cache_len][(index_next/block_X[array])/L1_cache_len] = 1
      #L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]=1
      #L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]=1
     else: # different warp
      warp = warp_next
      access.append(len(collect))
     
      collect = []
      add = 0
      collect.append(index_next)
      add = len(collect_array_N)
      access_cache_line.append(1+(add-1)*alfa)
      #collect_array = kong(array_next)
      collect_array_N = []
      index_transform= (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
      if index_transform not in collect_array_N:
       collect_array_N.append(index_transform)
       L1_transform = (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
       if L1_transform in L1_list:
        #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
        #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
        if math.fabs(L1_list.index(L1_transform)-len(L1_list))<=L1_lines:
         L1_hit += 1 
        L1_list.remove(L1_transform)
        L1_list.append(L1_transform)
       
       else:
        #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
        #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
        #if L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]==1:
        if L1_transform in L1_list:
         L1_list.remove(L1_transform)
        L1_list.append(L1_transform)
        L2_transform = (index_next%block_X[array_next])/L2_cache_len *size_1D+(index_next/block_X[array_next])/L2_cache_len*size_2D
        if L2_transform in L2_list:#(L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]==1):
         #L2_x = int(math.sqrt(L2_cache_line/sizeof[array_next])/4)*4
        # position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_x-1)/L1_x) + ((index_next%block_X[array_next])/L2_cache_len)
         if math.fabs(L2_list.index(L2_transform)-len(L2_list))<=L2_lines:
          L2_hit += 1 
         L2_list.remove(L2_transform)
         L2_list.append(L2_transform)
        else:
         #position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_cache_len-1)/L2_cache_len) + ((index_next%block_X[array_next])/L2_cache_len)
         L2_list.append(L2_transform)

      #collect_array[(index_next%block_X[array])/L1_cache_len][(index_next/block_X[array])/L1_cache_len] = 1
      #L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]=1
      #L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]=1
    else:  #different loop
     loop = loop_next
     warp = warp_next
     access.append(len(collect))
     collect = []
     add = 0
     collect.append(index_next)
     add = len(collect_array_N)
     collect_array_N = []
     access_cache_line.append(1+(add-1)*alfa)
     #collect_array = kong(array_next)
     index_transform= (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
     if index_transform not in collect_array_N:
      collect_array_N.append(index_transform)
      L1_transform = (index_next%block_X[array_next])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
      if L1_transform in L1_list:#(L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]==1):
       #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
       #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
       if math.fabs(L1_list.index(L1_transform)-len(L1_list))<=L1_lines:
        L1_hit += 1 
       L1_list.remove(L1_transform)
       L1_list.append(L1_transform)
       
      else:
       #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
       #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
       #if L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]==1:
       if L1_transform in L1_list:
        L1_list.remove(L1_transform)
       L1_list.append(L1_transform)
       L2_transform = (index_next%block_X[array_next])/L2_cache_len *size_1D+(index_next/block_X[array_next])/L2_cache_len*size_2D
       if L2_transform in L2_list:#(L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]==1):
        #L2_x = int(math.sqrt(L2_cache_line/sizeof[array_next])/4)*4
        #position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_x-1)/L1_x) + ((index_next%block_X[array_next])/L2_cache_len)
        if math.fabs(L2_list.index(L2_transform)-len(L2_list))<=L2_lines:
         L2_hit += 1 
        L2_list.remove(L2_transform)
        L2_list.append(L2_transform)
       else:
        #position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_cache_len-1)/L2_cache_len) + ((index_next%block_X[array_next])/L2_cache_len)
        L2_list.append(L2_transform)

     #collect_array[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len] = 1
     #L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]=1
     #L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]=1
   else: #different exprs

    access.append(len(collect))
    collect = []
    collect.append(index_next)
    add = len(collect_array_N)
    collect_array_N =[]
    access_cache_line.append(1+(add-1)*alfa)
    index_transform= (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
    if index_transform not in collect_array_N:
     collect_array_N.append(index_transform)
     L1_transform = (index_next%block_X[array_next])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
     if L1_transform in L1_list:#(L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]==1):
      #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
      #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
      if math.fabs(L1_position.index(L1_transform)-len(L1_list))<=L1_lines:
       L1_hit += 1 
      L1_list.remove(L1_transform)
      L1_list.append(L1_transform)
     
     else:
      #L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
      #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_x-1)/L1_x) + ((index_next%block_X[array_next])/L1_cache_len)
      if L1_transform in L1_list:#L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]==1:
       L1_list.remove(L1_transform)
      L1_list.append(L1_transform)
      L2_transform = (index_next%block_X[array_next])/L2_cache_len *size_1D+(index_next/block_X[array_next])/L2_cache_len*size_2D
      if L2_transform in L2_list:#(L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]==1):
      # L2_x = int(math.sqrt(L2_cache_line/sizeof[array_next])/4)*4
      # position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_x-1)/L1_x) + ((index_next%block_X[array_next])/L2_cache_len)
       if math.fabs(L2_list.index(L2_transform)-len(L2_list))<=L2_lines:
        L2_hit += 1 
       L2_list.remove(L2_transform)
       L2_list.append(L2_transform)
      else:
       #position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_cache_len-1)/L2_cache_len) + ((index_next%block_X[array_next])/L2_cache_len)
       L2_list.append(L2_transform)
    #print(str(x)+" index "+str(index_next)+" "+str((index_next%block_X[array_next])/L1_cache_len)+" "+str((index_next/block_X[array_next])/L1_cache_len))
    #collect_array[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len] = 1
    #L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len]=1
    #L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len]=1
    exp = exp_next
    loop = loop_next
    warp = warp_next
  else:  #different rw
   access = []
   access_cache_line = []
   collect = []
   if print1 == 0:
    #collect_array=kong(array_next)
    collect_array_N =[]
    L1_hit = 0
    L2_hit = 0
    L1_list =[] #kong(array_next)
    L2_list =[]#kong_L2(array_next)
   L1_transform = []
   L2_transform = []
   loop = loop_next
   exp = exp_next
   warp = warp_next
   #rw  = rw_next
   total = 99999999
   total_cache_line = 99999999
   if print1 == 0:
    print("array "+str(array)+" can only be put in shared memory or global memory")
    print1 = 1
 else: #different array
  access.append(len(collect))
  add = 0
  L1_x = int(math.sqrt(L1_cache_line/sizeof[array_next])/4)*4
  
  add = len(collect_array_N)
  collect_array_N =[]
  access_cache_line.append(1+(add-1)*alfa)
 # print(access_cache_line)
  for i in access:
   total += i
  if dimension[array] == 2:
   
   print("Array "+str(array)+" put in texture memory 2D has "+str(total)+ " latency")
  for i in access_cache_line:
   total_cache_line += i
  if dimension[array] == 2:
   if(block_X[array]>size_1D or block_Y[array]>size_2D):
    total_cache_line = 99999999
   print("Array "+str(array)+" put in texture memory 2D has "+str(total_cache_line)+ " cold latency!")
   print("Array "+str(array)+" put in texture memory 2D has "+str(L1_hit)+ " L1 hits!")
   print("Array "+str(array)+" put in texture memory 2D has "+str(L2_hit)+ " L2 hits!")
   printout = printout +str(total_cache_line)+" "+str(L1_hit)+" "+str(L2_hit)+" "
  #rw = rw_next
  access = []
  access_cache_line = []
  collect = []
  collect.append(index_next)
  #collect_array = kong(array_next) 
  #collect_array[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len] = 1
  index_transform= (index_next%block_X[array])/L1_cache_len*size_1D+(index_next/block_X[array])/L1_cache_len*size_2D
  collect_array_N.append(index_transform)
  exp = exp_next
  loop = loop_next
  total = 0
  total_cache_line=0
  array=array_next
  warp = warp_next
  L1_hit = 0
  L2_hit = 0
  L1_list = []#kong(array_next)
  L2_list = []# kong_L2(array_next)
  L1_position = []
  L2_position = []
  L1_cache_len = int(math.sqrt(L1_cache_line/sizeof[array])/4)*4
  L2_cache_len = int(math.sqrt(L2_cache_line/sizeof[array])/4)*4
  L1_lines = L1_size/(L1_cache_len*L1_cache_len)
  L2_lines = L2_size/(L2_cache_len*L2_cache_len)
  #L1[(index_next%block_X[array_next])/L1_cache_len][(index_next/block_X[array_next])/L1_cache_len] = 1
  #L2[(index_next%block_X[array_next])/L2_cache_len][(index_next/block_X[array_next])/L2_cache_len] = 1
  L1_transform = (index_next%block_X[array_next])/L1_cache_len *size_1D+(index_next/block_X[array_next])/L1_cache_len*size_2D
  L2_transform = (index_next%block_X[array_next])/L2_cache_len *size_1D+(index_next/block_X[array_next])/L2_cache_len*size_2D
  L1_list.append(L1_transform)
  L2_list.append(L2_transform)
  #position = ((index_next/block_X[array_next])/L1_cache_len) * ((block_X[array_next]+L1_cache_len)/L1_cache_len) + ((index_next%block_X[array_next])/L1_cache_len)
  #L1_position.append(position)
  #position = ((index_next/block_X[array_next])/L2_cache_len) * ((block_X[array_next]+L2_cache_len-1)/L2_cache_len) + ((index_next%block_X[array_next])/L2_cache_len)
  #L2_position.append(position)
access.append(len(collect))
add = len(collect_array_N)
access_cache_line.append(1+(add-1)*alfa)
for i in access:
 total += i
for i in access_cache_line:
 total_cache_line += i
if(block_X[array]>size_1D or block_Y[array]>size_2D):
 total_cache_line = 99999999
if dimension[array_next] == 2:
 print("Array "+str(array_next)+" put in texture memory has "+str(total)+ " latency")
if dimension[array_next] == 2:
 print("Array "+str(array_next)+" put in texture memory has "+str(total_cache_line)+ " cold latency")
 print("Array "+str(array)+" put in texture memory 2D has "+str(L1_hit)+ " L1 hits!")
 print("Array "+str(array)+" put in texture memory 2D has "+str(L2_hit)+ " L2 hits!")
 printout = printout +str(total_cache_line)+" "+str(L1_hit)+" "+str(L2_hit)+"\n"
 out = open("output.txt",'a')
 out.write(printout)
 out.close()
end = time.time()
print end-start
