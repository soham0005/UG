import csv
import os

def combine(arr, miss):
    return ','.join([arr[i] for i in range(len(arr)) if i != miss])

def apriori_gen(sets, k):
    set2 = set()
    for item1 in sets:
        for item2 in sets:
            if item1 != item2:
                v1 = item1.split(',')
                v2 = item2.split(',')
                if v1[:k-1] == v2[:k-1]:
                    v1.append(v2[k-1])
                    v1.sort()
                    all_eq = all(combine(v1, i) in sets for i in range(len(v1)))
                    if all_eq:
                        set2.add(','.join(v1))
    return set2

def calculate_support(itemset, datatable):
    count = 0
    for transaction in datatable:
        if all(item in transaction for item in itemset):
            count += 1
    return count

def apriori_algorithm(input_file, output_file, minfre):
    datatable = []
    products = set()
    freq = {}
    try:
        with open(input_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                transaction = set(item.strip() for item in row if item.strip())
                if transaction: 
                    datatable.append(transaction)
                    for item in transaction:
                        products.add(item)
                        freq[item] = freq.get(item, 0) + 1
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except csv.Error as e:
        print(f"Error reading the CSV file: {e}")
        return

 
    min_support = minfre * len(datatable) / 100
    print(f"Minimum support count: {min_support:.2f} (calculated as {minfre}% of {len(datatable)})\n")

  
    products = {item for item in products if freq[item] >= min_support}

    pass_count = 1
    final_frequent_sets = []

   
    print(f"Frequent {pass_count}-item sets:\n" + "-" * 30)
    for item in sorted(products):  
        final_frequent_sets.append((f"{{{item}}}", freq[item]))
        print(f"{item: <15}: {freq[item]}")

    prev = products.copy()
    i = 2

    while prev:
        cur = apriori_gen(prev, i - 1)
        if not cur:
            break

        cur_freq = {}
        for itemset_str in cur:
            itemset = itemset_str.split(',')
            if all(item for item in itemset):
                support_count = calculate_support(itemset, datatable)
                if support_count >= min_support:
                    cur_freq[itemset_str] = support_count

        if not cur_freq:
            break

        final_frequent_sets = []  
        pass_count += 1
        print(f"\nFrequent {pass_count}-item sets:\n" + "-" * 30)

        for itemset_str in sorted(cur_freq.keys()):
            support_count = cur_freq[itemset_str]
            final_frequent_sets.append((f"{{{itemset_str}}}", support_count))
            print(f"{itemset_str: <15}: {support_count} (Support calculated from {support_count} occurrences)")

        prev = cur_freq.keys()
        i += 1

    # Write results to output file
    with open(output_file, 'w', newline='') as fw:
        writer = csv.writer(fw)
        writer.writerow(['Itemset', 'Support Count'])
        for itemset, support_count in final_frequent_sets:
            writer.writerow([itemset, support_count])

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'frequent_itemset_data.csv')
    output_file = os.path.join(script_dir, 'data_output.csv')

    try:
        minfre = float(input("Enter minimum Freq percentage: "))
        if minfre <= 0 or minfre > 100:
            raise ValueError("Frequency percentage must be between 0 and 100")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        apriori_algorithm(input_file, output_file, minfre)

