import argparse
import sys

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
    
    return n, task_durations, deadlines, penalties 

def calculate_criterion(sequences, task_durations, deadlines, penalties):
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

    tasks = list(range(1, n + 1))
    tasks.sort(key=lambda x: deadlines[x - 1])

    sequences = [[] for _ in range(4)]
    machine_end_times = [0] * 4

    for task in tasks:
        task_index = task - 1
        best_machine = min(range(4), key=lambda m: machine_end_times[m] + task_durations[task_index][m])
        sequences[best_machine].append(task)
        machine_end_times[best_machine] += task_durations[task_index][best_machine]

    criterion_value = calculate_criterion(sequences, task_durations, deadlines, penalties)
    

    with open(output_filename, 'w') as file:
        file.write(f"{criterion_value}\n")
        for sequence in sequences:
            file.write(" ".join(map(str, sequence)) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python 151892.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    
    generate_output(input_file, output_file)