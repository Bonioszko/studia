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

    error_message = "; ".join(errors) if errors else "No errors"
    return calculated_penalty, expected_penalty, error_message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the validator with a specified in_number or specific files.')
    parser.add_argument('args', nargs='+', help='Either in_number or instance and solution files')
    args = parser.parse_args()

    results = []
    if len(args.args) == 1:
        in_number = int(args.args[0])
        for i in range(50, 501, 50):
            instance_file = f"in_{in_number}_{i}.txt"
            solution_file = f"out_{i}"
            calculated_penalty, expected_penalty, error_message = main(instance_file, solution_file)
            results.append([calculated_penalty, expected_penalty, error_message])

        with open(f"results_{in_number}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Calculated Penalty", "Expected Penalty", "Errors"])
            writer.writerows(results)
            
    elif len(args.args) == 2:
        instance_file = args.args[0]
        solution_file = args.args[1]
        calculated_penalty, expected_penalty, error_message = main(instance_file, solution_file)
        print(f'Obliczona {calculated_penalty}, odczytana {expected_penalty} Error: {error_message}')
        with open("results.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Calculated Penalty", "Expected Penalty", "Errors"])
            writer.writerow([calculated_penalty, expected_penalty, error_message])