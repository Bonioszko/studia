import sys
import argparse
import csv

def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())
        p = []
        w = []
        d = []

        for line in lines[1:]:
            values = list(map(int, line.split()))
            p.append(values[:4])  
            w.append(values[4])  
            d.append(values[5]) 

    return n, p, w, d

def read_solution(filename):
    with open(filename, 'r') as file:
        total_penalty = int(file.readline().strip())
        schedule = [list(map(int, line.split())) for line in file]
    return total_penalty, schedule

def validate_solution(num_jobs, processing_times, weights, deadlines, expected_penalty, machine_schedule):
    errors = []
    job_completion_times = [0] * num_jobs
    job_assigned = [False] * num_jobs
    total_penalty = 0

    for machine_id, machine_jobs in enumerate(machine_schedule):
        current_time = 0
        for job in machine_jobs:
            if job < 1 or job > num_jobs:
                errors.append(f"Niepoprawne zadanie {job} na maszynie {machine_id + 1}.")
                continue

            job_index = job - 1
            if job_assigned[job_index]:
                errors.append(f"Zadanie {job} nie jest tylko raz")
                continue

            job_assigned[job_index] = True
            current_time += processing_times[job_index][machine_id]
            job_completion_times[job_index] = current_time

    for i, assigned in enumerate(job_assigned):
        if not assigned:
            errors.append(f"Zadanie {i + 1} nie jest przypisane.")

    for job_index in range(num_jobs):
        delay = max(0, job_completion_times[job_index] - deadlines[job_index])
        penalty = weights[job_index] * delay
        total_penalty += penalty

    if total_penalty != expected_penalty:
        errors.append(f"Obliczona wartosc ({total_penalty}) nie jest taka sama jak {expected_penalty}).")

    return errors, total_penalty

def main(instance_file, solution_file):
    n, p, w, d = read_instance(instance_file)
    expected_penalty, schedule = read_solution(solution_file)

    errors, calculated_penalty = validate_solution(n, p, w, d, expected_penalty, schedule)
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Correct solution")

    print(f"Correct value: {expected_penalty}")
    print(f"Solution value: {calculated_penalty}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python verify.py <instance> <output>")
        sys.exit(1)

    instance_file = sys.argv[1]
    solution_file = sys.argv[2]
    main(instance_file, solution_file)