import os
import subprocess
import sys
import re
import csv
import time

def run_verification_for_all_files(executable):
    exec_name = os.path.splitext(os.path.basename(executable))[0]
    number = re.search(r'\d+', exec_name).group()  
    
    with open('end.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow([number])

        for i in range(50, 501, 50):
            input_file = f'in_151892_{i}.txt'
            output_file = f'out_{number}_{i}.txt'
            exec_output_file = f'out_{exec_name}_{i}.txt'
            
            if os.path.exists(input_file):
                print(f"Running verification for {input_file}")
                try:
                    start_time = time.time()
                    command = ['python', 'weryfikator_czasu.py', executable, input_file, output_file, str(i//10)]
                    print(f"Executing command: {' '.join(command)}")
                    result = subprocess.run(
                        command,
                        capture_output=True,
                        text=True
                    )
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    
                    if result.returncode != 0:
                        print(f"Error running verification for {input_file}. Return code: {result.returncode}")
                        print(f"Error output: {result.stderr}")
                        value = "Error"
                    else:
                        print(f"Verification completed for {input_file}.")
                        exec_command = ['python', 'weryfikator.py', input_file, output_file]
                        exec_result = subprocess.run(
                            exec_command,
                            capture_output=True,
                            text=True
                        )
                        if exec_result.returncode != 0:
                            print(f"Error running weryfikator.py for {exec_output_file}. Return code: {exec_result.returncode}")
                            print(f"Error output: {exec_result.stderr}")
                            value = "Error"
                        else:
                            print(f"Verification completed for {exec_output_file}.")
                            print(f"Output: {exec_result.stdout}")
                            with open(output_file, 'r') as f:
                                value = f.readline().strip()

                    csv_writer.writerow([elapsed_time, value])

                except Exception as e:
                    print(f"Exception occurred while running verification for {input_file}: {e}")
                    csv_writer.writerow([None, "Exception"])
            else:
                print(f"Input file {input_file} does not exist. Skipping.")
                csv_writer.writerow([None, "File not found"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_all.py <executable>")
        sys.exit(1)

    executable = sys.argv[1]
    run_verification_for_all_files(executable)