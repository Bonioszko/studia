import sys

def read_instance(filename):
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


def read_solution(filename):
    with open(filename, 'r') as f:
        F = int(f.readline().strip())
        sequence = list(map(int, f.readline().split()))
    return F, sequence


def verify_solution(n, p, r, S, F, sequence):
    errors = []

    if len(sequence) != n or set(sequence) != set(range(1, n + 1)):
        errors.append("Some task is missing or is present more than once")

    current_time = 0
    total_flow_time = 0
    previous_task = 0

    for task in sequence:
        task_index = task - 1

        if previous_task != 0:
            current_time += S[previous_task - 1][task_index]

        start_time = max(current_time, r[task_index])

        if start_time < r[task_index]:
            errors.append(f"Task {task} start befaore it is ready")

        completion_time = start_time + p[task_index]
        flow_time = completion_time - r[task_index]
        total_flow_time += flow_time

        current_time = completion_time
        previous_task = task

    if total_flow_time != F:
        errors.append(f"Value ({total_flow_time}) is not the same as provided: ({F})")

    return errors, total_flow_time


def main(instance_file, solution_file):
    n, p, r, S = read_instance(instance_file)
    F, sequence = read_solution(solution_file)
    print(sequence)
    errors, calculated_F = verify_solution(n, p, r, S, F, sequence)
    
    
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Correct solution")

    print(f"Correct value: {F}")
    print(f"Solution value: {calculated_F}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python verify.py <instance> <output>")
        sys.exit(1)

    instance_file = sys.argv[1]
    solution_file = sys.argv[2]
    main(instance_file, solution_file)