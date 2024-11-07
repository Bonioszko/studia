import sys
import time


def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        p = []
        r = []
        for i in range(n):
            task_data = list(map(int, lines[i + 1].split()))
            p.append(task_data[0])
            r.append(task_data[1])

        S = []
        for i in range(n):
            setup_times = list(map(int, lines[i + n + 1].split()))
            S.append(setup_times)

    return n, p, r, S

def evaluate_permutation(sequence, p, r, S):
    current_time = 0
    total_flow_time = 0
    previous_task = 0

    for task in sequence:
        task_index = task - 1

        
        current_time += S[previous_task - 1][task_index] if previous_task != 0 else 0
        start_time = max(current_time, r[task_index])

        completion_time = start_time + p[task_index]
        flow_time = completion_time - r[task_index]
        total_flow_time += flow_time

        current_time = completion_time
        previous_task = task

    return total_flow_time

def find_solution(n, p, r, S, time_limit):
    time.sleep(time_limit)
    current_time = 0
    previous_task = 0
    sequence = []
    remaining_tasks = set(range(1, n + 1))

    start_time = time.time()
    time_limit -= 1

    while remaining_tasks:
        best_task = None
        best_time = float('inf')

        for task in remaining_tasks:
            task_index = task - 1
            setup_time = S[previous_task - 1][task_index] if previous_task != 0 else 0
            ready_time = max(current_time + setup_time, r[task_index])
            if ready_time < best_time:
                best_time = ready_time
                best_task = task

        if best_task is not None:
            task_index = best_task - 1
            sequence.append(best_task)
            remaining_tasks.remove(best_task)
            if previous_task != 0:
                current_time += S[previous_task - 1][task_index]
            current_time = max(current_time, r[task_index]) + p[task_index]
            previous_task = best_task

        if time.time() - start_time > time_limit:
            print("Time limit exceeded during processing.")
            break

    return evaluate_permutation(sequence, p, r, S), sequence

def write_output(filename, best_F, best_order):
    with open(filename, 'w') as f:
        f.write(f"{best_F}\n")
        f.write(" ".join(str(job) for job in best_order) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python test.py <input_file> <output_file> <time_limit>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_limit = int(sys.argv[3])
    print(input_file)
    n, p, r, S = read_input(input_file)
    best_F, best_order = find_solution(n, p, r, S, time_limit)
    write_output(output_file, best_F, best_order)