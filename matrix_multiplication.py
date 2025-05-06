#!/usr/bin/env python3

import sys
import os

# Mapper script
def mapper():
    # Read environment variables or use defaults
    i_max = int(os.environ.get('i_max', 3))
    k_max = int(os.environ.get('k_max', 3))
    
    for line in sys.stdin:
        # Parse input line
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(',')
        matrix = parts[0]
        
        if matrix == 'A':
            # A,i,j,value
            _, i, j, value = parts
            i, j = int(i), int(j)
            value = float(value)
            
            # Emit for each possible k
            for k in range(k_max):
                print(f"{i},{k}\tA,{j},{value}")
                
        elif matrix == 'B':
            # B,j,k,value
            _, j, k, value = parts
            j, k = int(j), int(k)
            value = float(value)
            
            # Emit for each possible i
            for i in range(i_max):
                print(f"{i},{k}\tB,{j},{value}")

# Reducer script
def reducer():
    current_key = None
    a_values = {}
    b_values = {}
    
    # Read j_max from environment variables or use default
    j_max = int(os.environ.get('j_max', 2))
    
    for line in sys.stdin:
        # Parse input
        line = line.strip()
        if not line:
            continue
        
        key, value = line.split('\t', 1)
        matrix, j, val = value.split(',')
        j = int(j)
        val = float(val)
        
        # If key changes, process the previous key
        if current_key and current_key != key:
            # Calculate result for previous key
            result = 0
            for j in range(j_max):
                result += a_values.get(j, 0) * b_values.get(j, 0)
            
            if result != 0:
                print(f"{current_key}\t{result}")
            
            # Reset for new key
            a_values = {}
            b_values = {}
        
        current_key = key
        
        # Store value
        if matrix == 'A':
            a_values[j] = a_values.get(j, 0) + val
        else:  # matrix == 'B'
            b_values[j] = b_values.get(j, 0) + val
    
    # Process the last key
    if current_key:
        result = 0
        for j in range(j_max):
            result += a_values.get(j, 0) * b_values.get(j, 0)
        
        if result != 0:
            print(f"{current_key}\t{result}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--mapper":
        mapper()
    elif len(sys.argv) > 1 and sys.argv[1] == "--reducer":
        reducer()
    else:
        # Simulate MapReduce locally for testing
        print("This script is designed to be used with Hadoop Streaming.")
        print("For local testing, pipe input through mapper and reducer:")
        print("cat matrix_data.txt | python3 matrix_multiplication.py --mapper | sort | python3 matrix_multiplication.py --reducer")

# hadoop jar C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.2.4.jar ^
# -files matrix_multiplication.py ^
# -mapper "python matrix_multiplication.py --mapper" ^
# -reducer "python matrix_multiplication.py --reducer" ^
# -input file:///C:/Users/ADMIN/OneDrive/Documents/CL4/bda3/input/matrix_data.txt ^
# -output file:///C:/Users/ADMIN/OneDrive/Documents/CL4/bda3/output-matrix ^
# -cmdenv "i_max=3" -cmdenv "j_max=2" -cmdenv "k_max=3"