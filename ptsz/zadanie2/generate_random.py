import csv
import random
import argparse

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
    
    return n,  task_durations, deadlines, penalties

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

def generate_output(input_filename, output_filename):
    n, task_durations, deadlines, penalties = read_input_file(input_filename)

    # Generate random sequences for 4 machines
    sequences = [[] for _ in range(4)]
    task_indices = list(range(1, n + 1))
    random.shuffle(task_indices)

    for i, task_index in enumerate(task_indices):
        machine = i % 4
        sequences[machine].append(task_index)

    # Calculate the criterion value
    criterion_value = calculate_criterium(sequences, task_durations, deadlines, penalties)
    
    # Write the output file
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([criterion_value])
        for sequence in sequences:
            writer.writerow(sequence)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sample output file.')
    parser.add_argument('input_filename', type=str, help='The input CSV file name')
    parser.add_argument('output_filename', type=str, help='The output CSV file name')
    args = parser.parse_args()
    
    generate_output(args.input_filename, args.output_filename)