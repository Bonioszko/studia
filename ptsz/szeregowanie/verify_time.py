import subprocess
import time
import sys

def run_verification(executable, input_file, output_file, time_limit):
    start_time = time.time()
    
    print(f"Running: {executable} {input_file} {output_file} {time_limit}")

    result = subprocess.run(
        [executable, input_file, output_file, str(time_limit)],
        capture_output=True,
        text=True
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    if result.returncode != 0:
        print(f"Program terminated with an error. Return code: {result.returncode}")
        print(f"Error output: {result.stderr}")
        print(f"Standard output: {result.stdout}")
    else:
        print(f"Program executed successfully.")
        print(f"Output: {result.stdout}")

    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    if end_time - start_time > time_limit:
        print("Time exceeded !!!!!")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python verify_time.py <executable> <input_file> <output_file> <time_limit>")
        sys.exit(1)

    executable = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    time_limit = int(sys.argv[4])

    run_verification(executable, input_file, output_file, time_limit)