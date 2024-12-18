# import sys

# def read_instance(filename):
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#         n = int(lines[0].strip())
#         p = []
#         r = []
#         d = []
#         w = []

#         for line in lines[1:]:
#             values = list(map(int, line.split()))
#             p.append(values[:4])  # Processing times for 4 machines
#             r.append(values[4])  # Ready time
#             d.append(values[5])  # Deadline
#             w.append(values[6])  # Penalty weight

#     return n, p, r, d, w

# def read_solution(filename):
#     with open(filename, 'r') as file:
#         total_penalty = int(file.readline().strip())
#         schedule = [list(map(int, line.split())) for line in file]
#     return total_penalty, schedule

# def validate_solution(num_jobs, processing_times, ready_times, deadlines, weights, expected_penalty, machine_schedule):
#     errors = []
#     job_completion_times = [0] * num_jobs
#     job_assigned = [False] * num_jobs
#     total_penalty = 0

#     # Calculate penalties and validate
#     for job_index in range(num_jobs):
#         delay = max(0, job_completion_times[job_index] - deadlines[job_index])
#         penalty = weights[job_index] * delay
#         total_penalty += penalty

#     if total_penalty != expected_penalty:
#         errors.append(f"Calculated penalty ({total_penalty}) does not match the expected value ({expected_penalty}).")

#     # Validate each job appears exactly once in each sequence
#     for job in range(1, num_jobs + 1):
#         for machine_jobs in machine_schedule[:4]:
#             if machine_jobs.count(job) != 1:
#                 errors.append(f"Job {job} does not appear exactly once in machine sequence.")

#     # Validate no overlapping operations for the same job on different machines
#     for job in range(1, num_jobs + 1):
#         job_times = []
#         for machine_id, machine_jobs in enumerate(machine_schedule[:4]):
#             if job in machine_jobs:
#                 job_index = machine_jobs.index(job)
#                 start_time = sum(processing_times[job - 1][:machine_id])
#                 end_time = start_time + processing_times[job - 1][machine_id]
#                 job_times.append((start_time, end_time))
#         job_times.sort()
#         for i in range(1, len(job_times)):
#             if job_times[i][0] < job_times[i - 1][1]:
#                 errors.append(f"Overlapping operations for job {job} on different machines.")

#     # Validate no overlapping operations for different jobs on the same machine
#     for machine_id, machine_jobs in enumerate(machine_schedule[:4]):
#         current_time = 0
#         for job in machine_jobs:
#             job_index = job - 1
#             start_time = current_time
#             end_time = start_time + processing_times[job_index][machine_id]
#             current_time = end_time
#             for other_job in machine_jobs:
#                 if other_job != job:
#                     other_job_index = other_job - 1
#                     other_start_time = sum(processing_times[other_job_index][:machine_id])
#                     other_end_time = other_start_time + processing_times[other_job_index][machine_id]
#                     if start_time < other_end_time and end_time > other_start_time:
#                         errors.append(f"Overlapping operations for different jobs {job} and {other_job} on machine {machine_id + 1}.")

#     # Validate job starts after its ready time
#     for machine_id, machine_jobs in enumerate(machine_schedule[:4]):
#         current_time = 0
#         for job in machine_jobs:
#             job_index = job - 1
#             if current_time < ready_times[job_index]:
#                 current_time = ready_times[job_index]
#             start_time = current_time
#             end_time = start_time + processing_times[job_index][machine_id]
#             current_time = end_time
#             if start_time < ready_times[job_index]:
#                 errors.append(f"Job {job} on machine {machine_id + 1} starts before its ready time.")

#     return errors, total_penalty

# def main(instance_file, solution_file):
#     n, p, r, d, w = read_instance(instance_file)
#     expected_penalty, schedule = read_solution(solution_file)

#     errors, calculated_penalty = validate_solution(n, p, r, d, w, expected_penalty, schedule)

#     print(f"Given penalty: {expected_penalty}")
#     print(f"Calculated penalty: {calculated_penalty}")
#     if errors:
#         print("Errors:")
#         for error in errors:
#             print(f" - {error}")
#     else:
#         print("Solution is valid.")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("USAGE: python3 weryfikator.py <instance> <solution>")
#         sys.exit(1)

#     instance_file = sys.argv[1]
#     solution_file = sys.argv[2]
#     main(instance_file, solution_file)

import sys

def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        p, r, d, w = [], [], [], []

        for line in lines[1:]:
            values = list(map(int, line.split()))
            p.append(values[:4])  # Processing times for 4 machines
            r.append(values[4])  # Ready time
            d.append(values[5])  # Deadline
            w.append(values[6])  # Penalty weight

    return n, p, r, d, w

def read_output(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        criterion_value = int(lines[0].strip())
        task_sequences = [list(map(int, line.split())) for line in lines[1:5]]
        machine_sequences = [list(map(int, line.split())) for line in lines[5:]]

    return criterion_value, task_sequences, machine_sequences

def verify_solution(instance_file, output_file):
    n, p, r, d, w = read_instance(instance_file)
    criterion_value, task_sequences, machine_sequences = read_output(output_file)

    # Verify task and machine sequences
    all_tasks = set(range(1, n + 1))
    for idx, seq in enumerate(task_sequences):
        if set(seq) != all_tasks:
            return False, f"Error in task sequence at line {idx + 2}: Missing or duplicate tasks."

    for idx, seq in enumerate(machine_sequences):
        if len(seq) != 4 or set(seq) != {1, 2, 3, 4}:
            return False, f"Error in machine sequence at line {idx + 6}: Incorrect machine order."

    # Check scheduling constraints
    current_time = [[0] * 4 for _ in range(n)]  # Current time for each task and machine
    end_times = [0] * 4  # End times for each machine
    criterion_sum = 0

    for task_id in range(1, n + 1):
        task_idx = task_id - 1
        ready_time = r[task_idx]

        for machine_idx in range(4):
            machine = machine_sequences[task_idx][machine_idx] - 1
            start_time = max(current_time[task_idx][machine_idx], end_times[machine], ready_time)
            end_time = start_time + p[task_idx][machine_idx]

            # Check overlap for the task on the same machine
            if start_time < end_times[machine]:
                return False, f"Error: Overlapping operation for task {task_id} on machine {machine + 1}."

            # Update machine and task times
            current_time[task_idx][machine_idx] = end_time
            end_times[machine] = end_time

            # Check deadline violation
            if end_time > d[task_idx]:
                criterion_sum += w[task_idx]

    if criterion_sum != criterion_value:
        return False, f"Error: Criterion value mismatch. Expected {criterion_sum}, got {criterion_value}."

    return True, "Solution is valid."

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python verify.py <instance_file> <output_file>")
        sys.exit(1)

    instance_file = sys.argv[1]
    output_file = sys.argv[2]

    is_valid, message = verify_solution(instance_file, output_file)
    if is_valid:
        print("VALID:", message)
    else:
        print("INVALID:", message)
