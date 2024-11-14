import csv
import itertools

def read_transactions(input_file):
    transactions = []
    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            transaction = set(item.strip() for item in row if item.strip())
            if transaction:
                transactions.append(transaction)
    return transactions

def calculate_support(transactions, itemset):
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions) if transactions else 0

def find_all_itemsets(transactions):
    items = {item for transaction in transactions for item in transaction}
    current_itemsets = [frozenset({item}) for item in items]
    all_itemsets = []
    seen_itemsets = set()

    while current_itemsets:
        new_itemsets = []
        for itemset in current_itemsets:
            support = calculate_support(transactions, itemset)
            if itemset not in seen_itemsets:
                all_itemsets.append(itemset)
                seen_itemsets.add(itemset)
                new_itemsets.append(itemset)
        
        current_itemsets = [
            set1.union(set2) for set1 in new_itemsets 
            for set2 in new_itemsets
            if len(set1.union(set2)) == len(set1) + 1
        ]
        current_itemsets = list(set(frozenset(itemset) for itemset in current_itemsets))

    return all_itemsets

def main():
    input_file = 'frequent_itemset_data.csv'
    output_file = 'output.txt'
    
    transactions = read_transactions(input_file)
    all_itemsets = find_all_itemsets(transactions)
    
    print("All Item Sets:")
    print("----------------------------------------")
    with open(output_file, 'w') as out_file:
        out_file.write("All Item Sets:\n")
        out_file.write("----------------------------------------\n")
        for itemset in all_itemsets:
            itemset_str = "{ " + " ".join(itemset) + " }"
            print(itemset_str)
            out_file.write(itemset_str + "\n")
    
    print("\nAll itemsets written to 'output.txt'.")

    # Take rule input from user
    rule_input = input("Enter the rule in the format 'A => B' (e.g., L1 L2 => L3): ").strip()
    antecedent_str, consequent_str = rule_input.split("=>")
    antecedent = frozenset(antecedent_str.strip().split())
    consequent = frozenset(consequent_str.strip().split())
    rule = antecedent.union(consequent)

    # Calculate support and confidence of the rule
    support_rule = calculate_support(transactions, rule)
    support_antecedent = calculate_support(transactions, antecedent)
    confidence = (support_rule / support_antecedent) if support_antecedent > 0 else 0

    # Print and write the results to the output file with intermediate steps
    rule_str = "{{ {} }} => {{ {} }}".format(" ".join(antecedent), " ".join(consequent))
    result = (
        f"\nRule: {rule_str}\n"
        f"Step 1: Identify transactions containing antecedent {antecedent}\n"
        f"Count of transactions with antecedent {antecedent}: {sum(1 for t in transactions if antecedent.issubset(t))}\n"
        f"Total transactions: {len(transactions)}\n"
        f"Support of antecedent {antecedent} = (Count of transactions with antecedent / Total transactions) * 100 = {support_antecedent * 100:.2f}%\n\n"
        f"Step 2: Identify transactions containing rule {rule}\n"
        f"Count of transactions with rule {rule}: {sum(1 for t in transactions if rule.issubset(t))}\n"
        f"Support of rule {rule} = (Count of transactions with rule / Total transactions) * 100 = {support_rule * 100:.2f}%\n\n"
        f"Step 3: Confidence = Support(Rule) / Support(Antecedent)\n"
        f"Confidence: {confidence * 100:.2f}%\n"
    )

    print(result)
    with open(output_file, 'a') as out_file:
        out_file.write(result)
    
    print("Intermediate steps, support, and confidence of the rule saved to 'output.txt'.")

if __name__ == "__main__":
    main()
