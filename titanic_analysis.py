#!/usr/bin/env python3
import sys
import csv
import argparse

def mapper():
    reader = csv.reader(sys.stdin)
    header = next(reader)  # Skip header
    for row in reader:
        if len(row) < 6:
            continue
        survived = row[1].strip()
        pclass = row[2].strip()
        sex = row[4].strip().lower()
        age = row[5].strip()

        # Emit for average age of males and females who died
        if survived == '0':
            try:
                age_value = float(age)
                if sex == 'male':
                    print(f"male_dead\t{age_value}")
                elif sex == 'female':
                    print(f"female_dead\t{age_value}")
            except:
                continue  # skip if age is not a number

        # Emit for number of survivors in each class
        if survived == '1':
            print(f"survived_class_{pclass}\t1")

def reducer():
    current_key = None
    total_male_age = 0
    total_female_age = 0
    male_count = 0
    female_count = 0
    total_class_1 = 0
    total_class_2 = 0
    total_class_3 = 0

    for line in sys.stdin:
        key, value = line.strip().split('\t')
        
        # Debugging: Print the current key and value to verify the input to the reducer
        print(f"Processing key: {key}, value: {value}")  # Debugging line
        
        if key != current_key and current_key is not None:
            # Output the average age of males who died
            if current_key == 'male_dead':
                avg_male_age = total_male_age / male_count if male_count != 0 else 0
                print(f"Average age of males who died: {avg_male_age:.2f}")
            # Output the average age of females who died
            elif current_key == 'female_dead':
                avg_female_age = total_female_age / female_count if female_count != 0 else 0
                print(f"Average age of females who died: {avg_female_age:.2f}")
            # Output survivors in each class
            elif current_key.startswith('survived_class_'):
                class_num = current_key[-1]
                if class_num == '1':
                    print(f"Number of survivors in class 1: {total_class_1}")
                elif class_num == '2':
                    print(f"Number of survivors in class 2: {total_class_2}")
                elif class_num == '3':
                    print(f"Number of survivors in class 3: {total_class_3}")
            # Reset counters
            total_male_age = total_female_age = 0
            male_count = female_count = 0
            total_class_1 = total_class_2 = total_class_3 = 0

        current_key = key
        try:
            value = float(value)
            if key == 'male_dead':
                total_male_age += value
                male_count += 1
            elif key == 'female_dead':
                total_female_age += value
                female_count += 1
            elif key == 'survived_class_1':
                total_class_1 += value
            elif key == 'survived_class_2':
                total_class_2 += value
            elif key == 'survived_class_3':
                total_class_3 += value
        except ValueError:
            continue  # skip if value cannot be converted to float

    # Final keys: Ensure to output for the last key encountered
    if current_key == 'male_dead':
        avg_male_age = total_male_age / male_count if male_count != 0 else 0
        print(f"Average age of males who died: {avg_male_age:.2f}")
    elif current_key == 'female_dead':
        avg_female_age = total_female_age / female_count if female_count != 0 else 0
        print(f"Average age of females who died: {avg_female_age:.2f}")
    elif current_key.startswith('survived_class_'):
        class_num = current_key[-1]
        if class_num == '1':
            print(f"Number of survivors in class 1: {total_class_1}")
        elif class_num == '2':
            print(f"Number of survivors in class 2: {total_class_2}")
        elif class_num == '3':
            print(f"Number of survivors in class 3: {total_class_3}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapper', action='store_true')
    parser.add_argument('--reducer', action='store_true')
    args = parser.parse_args()

    if args.mapper:
        mapper()
    elif args.reducer:
        reducer()

# hadoop jar C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.2.4.jar ^
# -files mapreduce_titanic.py ^
# -mapper "python mapredue_titanic.py run_mapper" ^
# -reducer "python mapreduce_titanic.py run_reducer" ^
# -input file:///C:/Users/ADMIN/OneDrive/Documents/CL4/bda3/titanic_test_data.csv ^
# -output file:///C:\Users\ADMIN\OneDrive\Documents\CL4\bda3\titanic_output