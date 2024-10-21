import os
import subprocess
import sys

def run_verification_for_all_files(executable, folder, time_limit):
    for i in range(50, 501, 50):
        input_file = os.path.join(folder, f'in_151892_{i}.txt')
        output_file = os.path.join(folder, f'out_151892_{i}.txt')
        
        if os.path.exists(input_file):
            print(f"Running verification for {input_file}...")
            try:
                command = ['python', 'weryfikator_czasu.py', executable, input_file, output_file, str(time_limit)]
                print(f"Executing command: {' '.join(command)}")
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"Error running verification for {input_file}. Return code: {result.returncode}")
                    print(f"Error output: {result.stderr}")
                else:
                    print(f"Verification completed for {input_file}.")
                    print(f"Output: {result.stdout}")
            except Exception as e:
                print(f"Exception occurred while running verification for {input_file}: {e}")
        else:
            print(f"Input file {input_file} does not exist. Skipping.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_all_verifications.py <executable> <folder> <time_limit>")
        sys.exit(1)

    executable = sys.argv[1]
    folder = sys.argv[2]
    time_limit = int(sys.argv[3])

    run_verification_for_all_files(executable, folder, time_limit)