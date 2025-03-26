#!/usr/bin/env python3

import sys
import os
import subprocess

def local_mapreduce_simulation(input_file, i_max=3, j_max=2, k_max=3):
    """
    Simulates MapReduce process locally for testing purposes
    """
    # Set environment variables
    os.environ['i_max'] = str(i_max)
    os.environ['j_max'] = str(j_max)
    os.environ['k_max'] = str(k_max)
    
    # Run mapper
    with open(input_file, 'r') as f:
        mapper_proc = subprocess.Popen(
            ['python', 'matrix_multiplication.py', '--mapper'],
            stdin=f,
            stdout=subprocess.PIPE,
            text=True
        )
        mapper_output = mapper_proc.communicate()[0]
    
    # Sort mapper output (simulating shuffle phase)
    sorted_lines = sorted(mapper_output.strip().split('\n'))
    
    # Run reducer
    reducer_proc = subprocess.Popen(
        ['python', 'matrix_multiplication.py', '--reducer'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    reducer_output = reducer_proc.communicate('\n'.join(sorted_lines))[0]
    
    print("Result Matrix:")
    for line in reducer_output.strip().split('\n'):
        i_k, value = line.split('\t')
        i, k = i_k.split(',')
        print(f"C[{i},{k}] = {value}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python local_simulation.py <input_file> [i_max j_max k_max]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) >= 5:
        i_max = int(sys.argv[2])
        j_max = int(sys.argv[3])
        k_max = int(sys.argv[4])
        local_mapreduce_simulation(input_file, i_max, j_max, k_max)
    else:
        local_mapreduce_simulation(input_file)