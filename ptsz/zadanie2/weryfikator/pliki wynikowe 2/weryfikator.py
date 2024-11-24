import csv
import argparse

def read_output_file(filename):
    with open(filename, mode='r') as file:
        lines = file.readlines()
    
    criterion_value = int(lines[0].strip())
    sequences = [line.strip().split() for line in lines[1:5]]
    return criterion_value, sequences

def verify_sequences(sequences, n):
    task_set = set()
    for seq in sequences:
        
        for task in seq:
            if task in task_set:
                return False
            task_set.add(task)
    return len(task_set) == n 

def calculate_criterium(sequences, task_durations, deadlines, penalties):
    total_penalty = 0
    for task_index, machine_seq in enumerate(sequences):
        current_time = 0
        for task in machine_seq:
            task = int(task) -1
            duration = task_durations[task][task_index]
            deadline = deadlines[task_index]
            penalty = penalties[task_index]
            
            current_time += duration
            delay = max(0, current_time - deadline)
            total_penalty += delay * penalty
    
    return total_penalty

def read_input_file(input_filename):
    with open(input_filename, mode='r') as file:
        lines = file.readlines()
    
    n = int(lines[0].strip())
    task_durations = []
    deadlines = []
    penalties = []
    
    for line in lines[1:]:
        parts = list(map(int, line.strip().split()))
        task_durations.append(parts[:4])
        penalties.append(parts[4])
        deadlines.append(parts[5])
    
    return task_durations, deadlines, penalties

def main(input_filename, output_filename):
    task_durations, deadlines, penalties = read_input_file(input_filename)
    n = len(task_durations)
    criterion_value, sequences = read_output_file(output_filename)
    
    if not verify_sequences(sequences, n):
        print("Error: Each task must appear exactly once across all sequences.")
        return
    
    calculated_criterion = calculate_criterium(sequences, task_durations, deadlines, penalties)
    
    if calculated_criterion == criterion_value:
        print("Verification successful: Criterion value matches.")
    else:
        print(f"Verification failed: Expected {criterion_value}, but calculated {calculated_criterion}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Verify the output file against the input file.')
    parser.add_argument('input_filename', type=str, help='The input CSV file name')
    parser.add_argument('output_filename', type=str, help='The output CSV file name')
    args = parser.parse_args()
    
    main(args.input_filename, args.output_filename)