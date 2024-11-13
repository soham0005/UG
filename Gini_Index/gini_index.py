import csv
from collections import defaultdict
from math import pow

def find_gini(data, attr):
    freq = defaultdict(int)
    for record in data:
        if attr in record:
            freq[record[attr]] += 1
    n = len(data)
    gini = 1.0
    for count in freq.values():
        pi = count / n
        gini -= pow(pi, 2)
    return round(gini, 3)

def find_gini_index(data, attr, target, file):
    freq = defaultdict(int)
    for record in data:
        if attr in record:
            freq[record[attr]] += 1
    n = len(data)
    gini_index = 0.0
    file.write(f"Counts for {attr}: {dict(freq)}\n")
    
    for value, count in freq.items():
        subset = [record for record in data if record[attr] == value]
        subset_gini = find_gini(subset, target)
        pi = count / n
        weighted_gini = round(pi * subset_gini, 3)
        gini_index += weighted_gini
        file.write(f"Gini({value}) = {subset_gini}, Weighted Gini = {weighted_gini}\n")
    
    gini_index = round(gini_index, 3)
    file.write(f"Gini Index(S, {attr}) = {gini_index}\n\n")
    return gini_index

data = []
with open('input.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    headers = reader.fieldnames
    for row in reader:
        data.append(row)

target = headers[-1]
attributes = headers[:-1]

with open('gini_output.txt', 'w') as file:
    target_gini = find_gini(data, target)
    file.write(f"Target Gini: {target_gini}\n\n")
    
    gini_indices = {}
    for attr in attributes:
        file.write(f"Calculating Gini Index for {attr}:\n")
        gini_index = find_gini_index(data, attr, target, file)
        gini_indices[attr] = gini_index

    best_split = min(gini_indices, key=gini_indices.get)
    file.write("Final Gini Indices:\n")
    for attr, gini_index in gini_indices.items():
        file.write(f"{attr}: {gini_index}\n")
    file.write(f"\nThe best attribute for splitting is: {best_split}\n")
