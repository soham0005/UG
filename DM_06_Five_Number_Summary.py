import csv

data_file = 'Dry_Bean_Dataset_CSV.csv'
attributes = ['Perimeter', 'MajorAxisLength', 'MinorAxisLength', 
              'AspectRation', 'Eccentricity', 'EquivDiameter']

data = {attribute: [] for attribute in attributes}

# Read the CSV file
with open(data_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        for attribute in attributes:
            data[attribute].append(float(row[attribute]))

def calculate_statistics(attribute_data):
    sorted_data = sorted(attribute_data)
    n = len(sorted_data)

    # Calculate Q1, Median, Q3, IQR
    q1 = sorted_data[(n + 1) // 4 - 1]
    median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2 if n % 2 == 0 else sorted_data[n // 2]
    q3 = sorted_data[(3 * (n + 1)) // 4 - 1]
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Calculate Mean and Standard Deviation
    mean = sum(attribute_data) / n
    variance = sum((x - mean) ** 2 for x in attribute_data) / n
    std_dev = variance ** 0.5

    # Find Outliers
    outliers = [x for x in attribute_data if x < lower_bound or x > upper_bound]
    count_outliers = len(outliers)

    # Capture first 5 outliers
    first_five_outliers = outliers[:5] if count_outliers > 5 else outliers

    return q1, median, q3, iqr, lower_bound, upper_bound, mean, std_dev, count_outliers, first_five_outliers

for attribute in attributes:
    q1, median, q3, iqr, lower_bound, upper_bound, mean, std_dev, count_outliers, first_five_outliers = calculate_statistics(data[attribute])

    print(f"\n{attribute}:")
    print(f"Q1: {q1:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Q3: {q3:.2f}")
    print(f"IQR: {iqr:.2f}")
    print(f"Lower Bound: {lower_bound:.2f}")
    print(f"Upper Bound: {upper_bound:.2f}")
    print(f"Mean: {mean:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")
    print("Outliers are points that fall outside the lower and upper bound.")
    print(f"Count of Outliers: {count_outliers}")
    print(f"First 5 Outliers: {first_five_outliers}")
