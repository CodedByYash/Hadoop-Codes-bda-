#!/usr/bin/env python

import sys
from operator import itemgetter

class WordFrequencyMapper:
    def __init__(self, target_word):
        self.target_word = target_word.lower()
    
    def map(self):
        # Input comes from standard input (stdin)
        for line in sys.stdin:
            # Remove leading and trailing whitespace
            line = line.strip()
            # Split the line into words
            words = line.split()
            
            # For each word, emit a key-value pair with the word as the key
            # and 1 as the value only if it matches our target word
            for word in words:
                # Convert to lowercase to make comparison case-insensitive
                word = word.lower()
                if word == self.target_word:
                    print('%s\t%s' % (word, 1))

class WordFrequencyReducer:
    def reduce(self):
        current_word = None
        current_count = 0
        word = None

        # Input comes from standard input (stdin)
        for line in sys.stdin:
            # Remove leading and trailing whitespace
            line = line.strip()
            
            # Parse the input from mapper
            word, count = line.split('\t', 1)
            
            # Convert count to integer
            try:
                count = int(count)
            except ValueError:
                # Count was not a number, so silently ignore this line
                continue
            
            # This IF-switch works because Hadoop sorts map output by key
            # before it is passed to the reducer
            if current_word == word:
                current_count += count
            else:
                if current_word:
                    # Write result to standard output
                    print('%s\t%s' % (current_word, current_count))
                current_count = count
                current_word = word
        
        # Don't forget to output the last word if needed
        if current_word == word:
            print('%s\t%s' % (current_word, current_count))

# Main function to execute the mapper or reducer based on command line args
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python word_frequency.py [mapper|reducer] [target_word]")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "mapper":
        if len(sys.argv) < 3:
            print("Mapper mode requires a target word")
            sys.exit(1)
        target_word = sys.argv[2]
        mapper = WordFrequencyMapper(target_word)
        mapper.map()
    elif mode == "reducer":
        reducer = WordFrequencyReducer()
        reducer.reduce()
    else:
        print("Invalid mode. Use 'mapper' or 'reducer'")
        sys.exit(1)

# hadoop jar C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.2.4.jar ^
# -files word_frequency.py ^
# -mapper "python word_frequency.py mapper mapreduce" ^
# -reducer "python word_frequency.py reducer" ^
# -input file:///C:/Users/ADMIN/OneDrive/Documents/CL4/bda3/input/your_text_file.txt ^
# -output file:///C:/Users/ADMIN/OneDrive/Documents/CL4/bda3/output-word