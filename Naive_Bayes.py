import csv

data = []
with open('Naive_bayes_data.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    for row in reader:
        data.append(row)

total_count = len(data)
count_yes = sum(1 for row in data if row[-1] == "Yes")
count_no = total_count - count_yes

output = []
output.append(f"Total count of Yes: {count_yes}, Probability of Yes (M): {count_yes}/{total_count} = {count_yes / total_count:.3f}")
output.append(f"Total count of No: {count_no}, Probability of No (H): {count_no}/{total_count} = {count_no / total_count:.3f}\n")

def display_conditional_probs():
    for i, attribute in enumerate(headers[:-1]):
        output.append(f"Attribute: {attribute}")
        values = set(row[i] for row in data)
        for value in values:
            count_yes_given_value = sum(1 for row in data if row[i] == value and row[-1] == "Yes")
            count_no_given_value = sum(1 for row in data if row[i] == value and row[-1] == "No")
            prob_yes = f"{count_yes_given_value}/{count_yes} = {count_yes_given_value / count_yes:.3f}" if count_yes > 0 else "0/0 = 0.000"
            prob_no = f"{count_no_given_value}/{count_no} = {count_no_given_value / count_no:.3f}" if count_no > 0 else "0/0 = 0.000"
            output.append(f"    P({attribute}={value} | Yes): {prob_yes}")
            output.append(f"    P({attribute}={value} | No): {prob_no}")
        output.append("")

display_conditional_probs()

test_instance = ["Sunny", "Cool", "High", "false"]
output.append(f"Test instance to be classified: {test_instance}\n")

def calculate_posterior(species):
    posterior = count_yes / total_count if species == "Yes" else count_no / total_count
    for i, value in enumerate(test_instance):
        count_species = count_yes if species == "Yes" else count_no
        count = sum(1 for row in data if row[i] == value and row[-1] == species)
        conditional_prob = count / count_species if count_species else 0
        posterior *= conditional_prob
    return posterior

posterior_yes = calculate_posterior("Yes")
posterior_no = calculate_posterior("No")

output.append(f"\nProbability of instance for Yes: {posterior_yes:.6f}")
output.append(f"Probability of instance for No: {posterior_no:.6f}\n")

classification = "Yes" if posterior_yes > posterior_no else "No"
output.append(f"Predicted Species: {classification}")

with open("naive_bayes_output.txt", "w") as file:
    file.write("\n".join(output))
