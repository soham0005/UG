import csv

data = []
with open('Naive_bayes_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        data.append(row)

total_count = len(data)
count_M = sum(1 for row in data if row[-1] == "M")
count_H = total_count - count_M
P_M = f"{count_M}/{total_count} = {count_M / total_count:.3f}"
P_H = f"{count_H}/{total_count} = {count_H / total_count:.3f}"

print(f"Total count of M: {count_M}, Probability of M: {P_M}")
print(f"Total count of H: {count_H}, Probability of H: {P_H}\n")

def calculate_prob(attribute_index, value, species):
    count_species = count_M if species == "M" else count_H
    count = sum(1 for row in data if row[attribute_index] == value and row[-1] == species)
    fraction = f"{count}/{count_species}"
    decimal = count / count_species if count_species else 0
    print(f"Probability of attribute[{attribute_index}]={value} | Species={species}: {fraction} = {decimal:.3f}")
    return decimal

test_instance = ["Green", "2", "Tall", "No"]

print(f"\nTest instance to be classified: {test_instance}\n")

def calculate_posterior(species):
    posterior = count_M / total_count if species == "M" else count_H / total_count
    for i, value in enumerate(test_instance):
        posterior *= calculate_prob(i, value, species)
    return posterior

posterior_M = calculate_posterior("M")
posterior_H = calculate_posterior("H")

print(f"\nProbability of instance for M: {posterior_M:.6f}")
print(f"Probability of instance for H: {posterior_H:.6f}\n")

print(f"Comparing posterior probabilities:\nP(M | X) = {posterior_M:.6f} vs P(H | X) = {posterior_H:.6f}")
classification = "M" if posterior_M > posterior_H else "H"

print(f"\nPredicted Species: {classification}")
