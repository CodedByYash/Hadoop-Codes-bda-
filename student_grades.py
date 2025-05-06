#!/usr/bin/env python3

import sys
import os

# Mapper function
def mapper():
    """
    Mapper reads student records and emits (student_id, score) pairs
    Input format expected: student_id,subject,score
    """
    for line in sys.stdin:
        # Remove leading/trailing whitespace and split the line
        line = line.strip()
        if not line:
            continue
            
        # Parse the input
        fields = line.split(',')
        if len(fields) != 3:
            # Skip malformed input
            continue
            
        student_id, subject, score = fields
        
        try:
            # Validate score is a number
            score = float(score)
            # Emit student_id as key and score as value
            print(f"{student_id}\t{score}")
        except ValueError:
            # Skip records with invalid scores
            continue

# Reducer function
def reducer():
    """
    Reducer processes scores for each student and assigns a grade
    Output: student_id, average_score, grade
    """
    current_student = None
    scores = []
    
    # Grade boundaries
    def get_grade(avg_score):
        if avg_score >= 90:
            return 'A'
        elif avg_score >= 80:
            return 'B'
        elif avg_score >= 70:
            return 'C'
        elif avg_score >= 60:
            return 'D'
        else:
            return 'F'
    
    for line in sys.stdin:
        # Remove leading/trailing whitespace and split the line
        line = line.strip()
        if not line:
            continue
            
        # Parse the input (student_id, score)
        student_id, score = line.split('\t')
        score = float(score)
        
        # If we encounter a new student, process the previous one
        if current_student and current_student != student_id:
            # Calculate average score
            avg_score = sum(scores) / len(scores)
            # Determine grade
            grade = get_grade(avg_score)
            # Output: student_id, average_score, grade
            print(f"{current_student}\t{avg_score:.2f}\t{grade}")
            
            # Reset for the new student
            scores = []
        
        # Update current student and add score to the list
        current_student = student_id
        scores.append(score)
    
    # Process the last student
    if current_student:
        avg_score = sum(scores) / len(scores)
        grade = get_grade(avg_score)
        print(f"{current_student}\t{avg_score:.2f}\t{grade}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--mapper":
        mapper()
    elif len(sys.argv) > 1 and sys.argv[1] == "--reducer":
        reducer()
    else:
        # Simulate MapReduce locally for testing
        print("This script is designed to be used with Hadoop Streaming.")
        print("For local testing, pipe input through mapper and reducer:")
        print("cat student_data.txt | python3 student_grades.py --mapper | sort | python3 student_grades.py --reducer")

# hadoop jar C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.2.4.jar ^
# -files student_grades.py ^
# -mapper "python student_grades.py --mapper" ^
# -reducer "python student_grades.py --reducer" ^
# -input file:///C:/Users/ADMIN/OneDrive/Documents/CL4/bda3/input/student_data.txt ^
# -output file:///C:/Users/ADMIN/OneDrive/Documents/CL4/bda3/output-grades