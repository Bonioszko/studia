import csv
from collections import defaultdict
import math
# Open the CSV file in read mode
data = []
with open('titanic-homework.csv', 'r') as csvfile:
  csv_reader = csv.reader(csvfile)

  for row in csv_reader:
      data.append(row)

data_length = len(data) -1
    
#first index is for no, second for yes
def CollectData(data, attr):
    values = defaultdict(lambda: [0, 0])
    for i, row in enumerate(data):
        if i != 0:  # Skip the header row
            if attr == 4:  # Check if the attribute is the fourth one (age)
                age = int(row[attr])
                if 0 <= age <= 20:
                    age_group = 'young'
                elif 20 < age <= 40:
                    age_group = 'middle'
                elif 40 < age <= 100:
                    age_group = 'old'
                else:
                    continue  # Skip invalid age values

                if int(row[-1]) == 1:
                    values[age_group][1] += 1
                else:
                    values[age_group][0] += 1
            else:
                if int(row[-1]) == 1:
                    values[row[attr]][1] += 1
                else:
                    values[row[attr]][0] += 1
    return values

def calculate_entropy_whole(data):
    # Count the number of instances for each class
    class_counts = defaultdict(int)
    for i, row in enumerate(data):
        if i != 0:  # Skip the header row
            class_counts[row[-1]] += 1

    # Calculate the entropy
    entropy = 0
    for count in class_counts.values():
        probability = count / data_length
        entropy -= probability * math.log2(probability)

    return entropy

def CalculateEntropyForAttr(data):
    entropies={}
    for key in data.keys():
        first_value = data[key][0]
        second_value = data[key][1]
        sum_values = first_value + second_value

        entropy = 0
        if first_value > 0:
            entropy -= (first_value / sum_values) * math.log2(first_value / sum_values)
        if second_value > 0:
            entropy -= (second_value / sum_values) * math.log2(second_value / sum_values)

        entropies[key] = entropy
    return entropies

def CalculateIntrinsicInfo(attr):
    intrinsic_info= 0
    for value in attr.values():
        temp = (value[0] + value[1]) / data_length
        intrinsic_info -=  temp * math.log2(temp)
    return intrinsic_info

decisions = []
for i in range (1, len(data[0])-1):
    #skip the name attr
    if i !=2:
        dict = CollectData(data, i)
        decisions.append(dict)


entropies = []

for attr in decisions:
    entropies.append(CalculateEntropyForAttr(attr))

print("entropies ", entropies)

conditional_entropies= []
for i, attr in enumerate(decisions):
    conditional_entr = 0
    for key in attr.keys():
        conditional_entr += ((decisions[i][key][0] + decisions[i][key][1]) / data_length) * entropies[i][key]
    conditional_entropies.append(conditional_entr)

print("conditional", conditional_entropies)
entropy_whole = calculate_entropy_whole(data)
print("Entropy for the whole dataset: ", entropy_whole)
information_gains = []
for value in conditional_entropies:
    information_gains.append (entropy_whole- value)

print("information", information_gains)

gain_ratios =[]
for i, attr in enumerate(decisions):
    gain_ratios.append(information_gains[i] / CalculateIntrinsicInfo(attr))
print("gain", gain_ratios)