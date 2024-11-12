import csv
import math
from collections import defaultdict

def entropy(data, target):
    freq = defaultdict(int)
    for row in data:
        freq[row[target]] += 1

    n = len(data)
    entropy_value = 0.0
    for count in freq.values():
        pi = count / n
        if pi > 0:
            entropy_value -= pi * math.log2(pi)
    return round(entropy_value, 4)

def info_gain(data, attr, target):
    target_entropy = entropy(data, target)
    print(f"\nCalculating Information Gain for '{attr}':")
    print(f"Target Class Entropy (Entropy of '{target}'): {target_entropy}")

    freq = defaultdict(int)
    for row in data:
        freq[row[attr]] += 1

    n = len(data)
    attr_entropy = 0.0
    for attr_value, count in freq.items():
        pi = count / n
        subset = [row for row in data if row[attr] == attr_value]
        subset_entropy = entropy(subset, target)
        attr_entropy += pi * subset_entropy
        print(f"Subset for {attr} = '{attr_value}': Entropy = {subset_entropy}, Weight = {round(pi, 4)}")

    attr_entropy = round(attr_entropy, 4)
    print(f"Attribute Entropy of '{attr}': {attr_entropy}")
    gain = round(target_entropy - attr_entropy, 4)
    print(f"Information Gain (Gain(S, {attr})) = {gain}\n")
    return gain

def main():
   
    filename = "DM_04_Info_Gain_Data.csv"  
    data = []

   
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  
        for row in csvreader:
          
            row_data = {header[i]: row[i] for i in range(len(header))}
            data.append(row_data)

    if not header:
        print("The CSV file is empty or header is missing.")
        return

    target = header[-1] 

    attribute = input(f"Enter the attribute for information gain calculation (options: {header[:-1]}): ")
    if attribute not in header[:-1]:
        print(f"Invalid attribute. Choose from: {header[:-1]}")
        return

    gain = info_gain(data, attribute, target)
    print(f"Final Information Gain for '{attribute}' with respect to target '{target}': {gain}")

if __name__ == "__main__":
    main()
