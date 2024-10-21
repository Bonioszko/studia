import random


def generator(n):
    
    with open(f'in_151892_{n}.txt', 'w') as f:
        f.write(f'{n}\n') 

        sum_p = 0
        count  =0
        for i in range(1, n+1):
            p = random.randint(1, n) 
            r = random.randint(1, n*3)  
            f.write(f'{p} {r}\n')
            sum_p += p
            count += 1
        avg_p = sum_p // count
        for i in range(1, n+1):  
            f.write(' '.join(str(random.randint(1, avg_p)) for _ in range(1, n+1)) + '\n')
for i in range(50, 550, 50):
    generator(i)