import random
import csv
import argparse

def generate_data(pmin, pmax, n):
    data = []
    for _ in range(n):
        p1 = random.randint(pmin, pmax)
        p2 = random.randint(pmin, pmax)
        p3 = random.randint(pmin, pmax)
        p4 = random.randint(pmin, pmax)
        w = random.randint(pmin //2, pmax//2 )
        d = random.randint((pmin+pmax) , (n*((pmax +pmin) //6)))
        data.append([p1, p2, p3, p4, w, d])
    return data

def main(n):
    data = generate_data(1,100,n)
    
    filename = f'in_151892_{n}.txt'
    with open(filename, mode='w') as file:
        file.write(f"{n}\n")
        for row in data:
            file.write(" ".join(map(str, row)) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate printing orders data.')
    parser.add_argument('n', type=int, help='Number of orders to generate')
    args = parser.parse_args()
    
    main(args.n)