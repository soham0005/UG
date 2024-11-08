import csv
import itertools

def read_transactions(input_file):
    transactions = []
    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            # Remove empty strings and store as sets
            transaction = set(item.strip() for item in row if item.strip())
            if transaction:
                transactions.append(transaction)
    return transactions

def calculate_support(transactions, itemset):
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions) if transactions else 0

def find_frequent_itemsets(transactions, min_support):
    items = {item for transaction in transactions for item in transaction}
    
    # Generate 1-itemsets
    current_itemsets = [frozenset({item}) for item in items]
    frequent_itemsets = []
    seen_itemsets = set()

    while current_itemsets:
        new_frequent_itemsets = []
        for itemset in current_itemsets:
            support = calculate_support(transactions, itemset)
            if support >= min_support:
                if itemset not in seen_itemsets:
                    frequent_itemsets.append(itemset)
                    seen_itemsets.add(itemset)
                    new_frequent_itemsets.append(itemset)
        
        # Generate new itemsets from the previous frequent itemsets
        current_itemsets = [
            set1.union(set2) for set1 in new_frequent_itemsets 
            for set2 in new_frequent_itemsets
            if len(set1.union(set2)) == len(set1) + 1
        ]
        # Ensure unique itemsets
        current_itemsets = list(set(frozenset(itemset) for itemset in current_itemsets))

    return frequent_itemsets

def generate_rules(frequent_itemsets, min_confidence, transactions):
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent_set = frozenset(antecedent)
                consequent = itemset.difference(antecedent_set)
                support_antecedent = calculate_support(transactions, antecedent_set)
                support_itemset = calculate_support(transactions, itemset)
                if support_antecedent > 0:
                    confidence = support_itemset / support_antecedent
                    if confidence >= min_confidence:
                        rules.append((antecedent_set, consequent, confidence))
    return rules

def main():
    input_file = 'frequent_itemset_data.csv'
    output_file = 'output.txt'
    
    min_support = float(input("Enter minimum support (in %): ")) / 100
    min_confidence = float(input("Enter minimum confidence (in %): ")) / 100
    
    transactions = read_transactions(input_file)
    frequent_itemsets = find_frequent_itemsets(transactions, min_support)
    
    print("Frequent Item Sets:")
    print("----------------------------------------")
    with open(output_file, 'w') as out_file:
        out_file.write("Frequent Item Sets:\n")
        out_file.write("----------------------------------------\n")
        for itemset in frequent_itemsets:
            itemset_str = "{ " + " ".join(itemset) + " }"
            print(itemset_str)
            out_file.write(itemset_str + "\n")
        
        # Write and print association rules
        print("\nAssociation Rules:")
        print("----------------------------------------")
        out_file.write("\nAssociation Rules:\n")
        out_file.write("----------------------------------------\n")
        
        rules = generate_rules(frequent_itemsets, min_confidence, transactions)
        for antecedent, consequent, confidence in rules:
            rule_str = "{{ {} }} => {{ {} }} (Confidence: {:.2f}%)".format(
                " ".join(antecedent),
                " ".join(consequent),
                confidence * 100
            )
            print(rule_str)
            out_file.write(rule_str + "\n")
    
    print("\nSuccess! Output saved to 'output.txt'.")

if __name__ == "__main__":
    main()
