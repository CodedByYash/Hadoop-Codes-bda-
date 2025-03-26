#!/usr/bin/env python3

import subprocess

def local_mapreduce_simulation(input_file):
    """
    Simulates MapReduce process locally for testing student grades program
    """
    # Run mapper
    with open(input_file, 'r') as f:
        mapper_proc = subprocess.Popen(
            ['python', 'student_grades.py', '--mapper'],
            stdin=f,
            stdout=subprocess.PIPE,
            text=True
        )
        mapper_output = mapper_proc.communicate()[0]
    
    # Sort mapper output (simulating shuffle phase)
    sorted_lines = sorted(mapper_output.strip().split('\n'))
    
    # Run reducer
    reducer_proc = subprocess.Popen(
        ['python', 'student_grades.py', '--reducer'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    reducer_output = reducer_proc.communicate('\n'.join(sorted_lines))[0]
    
    print("Student Grades:")
    print("Student ID\tAverage\tGrade")
    print("-" * 30)
    for line in reducer_output.strip().split('\n'):
        print(line)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python local_simulation_grades.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    local_mapreduce_simulation(input_file)