import csv
import random
import argparse

def read_input_file(input_filename):
    with open(input_filename, mode='r') as file:
        reader = csv.reader(file)
        n = int(next(reader)[0])  
        task_durations = []
        deadlines = []
        penalties = []
        for row in reader:
            task_durations.append([int(row[0]), int(row[1]), int(row[2]), int(row[3])])
            penalties.append(int(row[4]))
            deadlines.append(int(row[5]))
    return n, task_durations, deadlines, penalties

def calculate_criterion(sequences, task_durations, deadlines, penalties):
    total_penalty = 0
    for machine_seq in sequences:
        current_time = 0
        for task in machine_seq:
            task_index = task - 1  # Convert to zero-based index
            duration = task_durations[task_index][machine_seq.index(task)]
            deadline = deadlines[task_index]
            penalty = penalties[task_index]
            
            current_time += duration
            delay = max(0, current_time - deadline)
            total_penalty += delay * penalty
    
    return total_penalty

def generate_output(input_filename, output_filename):
    n, task_durations, deadlines, penalties = read_input_file(input_filename)

    # Sort tasks by their deadlines
    tasks = list(range(1, n + 1))
    tasks.sort(key=lambda x: deadlines[x - 1])

    # Generate sequences for 4 machines
    sequences = [[] for _ in range(4)]
    machine_end_times = [0] * 4

    for task in tasks:
        task_index = task - 1
        # Find the machine that will complete the task the earliest
        best_machine = min(range(4), key=lambda m: machine_end_times[m] + task_durations[task_index][m])
        sequences[best_machine].append(task)
        machine_end_times[best_machine] += task_durations[task_index][best_machine]

    # Calculate the criterion value
    criterion_value = calculate_criterion(sequences, task_durations, deadlines, penalties)
    
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