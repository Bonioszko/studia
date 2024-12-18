import random
import sys

def generate_instance(num_tasks):
    with open(f'in_151892_{num_tasks}.txt', 'w') as f:
        f.write(f"{num_tasks}\n")
        for _ in range(num_tasks):
            p1 = random.randint(1, num_tasks//2)
            p2 = random.randint(1, num_tasks//2)
            p3 = random.randint(1, num_tasks//2)
            p4 = random.randint(1, num_tasks//2)
            r = random.randint(1, num_tasks)
            d = random.randint(r , r *3)
            w = random.randint(1, 10)
            f.write(f"{p1} {p2} {p3} {p4} {r} {d} {w}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generator.py <number_of_tasks>")
        sys.exit(1)
    
    num_tasks = int(sys.argv[1])
    generate_instance(num_tasks)