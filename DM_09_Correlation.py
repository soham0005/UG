# import csv

# def find_correlation(tid1, tid2, table):
#     tid1_count = 0
#     tid2_count = 0
#     total_common_count = 0
    
#     print("\nDetailed Analysis:")
#     print("-" * 50)
#     print(f"Analyzing Transaction IDs: {tid1+1} and {tid2+1}")
#     print("\nDay-by-day comparison:")
#     print("Day | TID1 | TID2 | Common")
#     print("-" * 30)
    
#     # Analyze each day's data
#     for day in range(1, 8):
#         has_tid1 = table[tid1][day] == "Y"
#         has_tid2 = table[tid2][day] == "Y"
#         is_common = has_tid1 and has_tid2
        
#         if has_tid1:
#             tid1_count += 1
#         if has_tid2:
#             tid2_count += 1
#         if is_common:
#             total_common_count += 1
            
#         print(f"{day}   |   {table[tid1][day]}   |   {table[tid2][day]}   |   {'Y' if is_common else 'N'}")

#     print("\nSummary Statistics:")
#     print(f"Total occurrences of TID {tid1+1}: {tid1_count}")
#     print(f"Total occurrences of TID {tid2+1}: {tid2_count}")
#     print(f"Total common occurrences: {total_common_count}")
    
#     # Calculate correlation
#     if tid1_count == 0 or tid2_count == 0:
#         print("\nCorrelation cannot be calculated - one or both transactions have zero occurrences")
#         return 0
    
#     correlation = total_common_count / (tid1_count * tid2_count)
#     print(f"\nCorrelation Calculation:")
#     print(f"Formula: Common occurrences / (TID1 occurrences × TID2 occurrences)")
#     print(f"        = {total_common_count} / ({tid1_count} × {tid2_count})")
#     print(f"        = {total_common_count} / {tid1_count * tid2_count}")
#     print(f"        = {correlation}")
    
#     return correlation

# def get_correlation_verdict(correlation):
#     if correlation == 0:
#         return "No relationship between entities"
#     elif correlation < 0:
#         return "Negative correlation"
#     elif correlation > 0:
#         return "Positive correlation"
#     else:
#         return "Not defined"

# # Read the CSV file
# table = []
# with open('DM_09_correlation.csv', newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     header = next(reader)  # Store header row
#     print("\nAnalyzing data from:", csvfile.name)
#     print("Months covered:", header[1:])
#     for row in reader:
#         table.append(row)

# n = len(table)
# print(f"\nTotal number of transactions in dataset: {n}")

# try:
#     i, j = map(int, input("\nEnter the two transaction IDs (separated by space): ").split())
#     if i < 1 or j < 1 or i > n or j > n:
#         raise ValueError("Transaction IDs must be within valid range")
# except ValueError as e:
#     print(f"Error: {e}")
#     exit(1)

# # Calculate correlation
# correlation = find_correlation(i-1, j-1, table)
# verdict = get_correlation_verdict(correlation)

# print("\nFinal Result:")
# print("-" * 50)
# print(f"Correlation ratio between TID {i} & {j} = {correlation}")
# print(f"Result: {verdict}")


# Numerical Data
import csv
import math

def find_mean(values):
    mean_value = sum(values) / len(values)
    print(f"Mean: {mean_value}")
    return mean_value


def find_covariance(a, b, mean_a, mean_b):
    covariance = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(len(a))) / len(a)
    print(f"Covariance: {covariance}")
    return covariance

def find_standard_deviation(values, mean):
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    standard_deviation = math.sqrt(variance)
    print(f"Standard Deviation: {standard_deviation}")
    return standard_deviation

def find_correlation(a, b):
    mean_a = find_mean(a)
    mean_b = find_mean(b)
    covariance = find_covariance(a, b, mean_a, mean_b)
    sd_a = find_standard_deviation(a, mean_a)
    sd_b = find_standard_deviation(b, mean_b)
    
    if sd_a == 0 or sd_b == 0:
        print("Correlation cannot be calculated due to zero variance in one of the datasets.")
        return None
    
    correlation = covariance / (sd_a * sd_b)
    print(f"Pearson Correlation Coefficient (r): {correlation}")
    return correlation

def read_csv(filename):
    x_data, y_data = [], []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            x_data.append(float(row[0]))
            y_data.append(float(row[1]))
    return x_data, y_data

filename = 'DM_09_correlation.csv'

x_data, y_data = read_csv(filename)
correlation = find_correlation(x_data, y_data)

if correlation is not None:
    if correlation > 0:
        print("Interpretation: Positive correlation")
    elif correlation < 0:
        print("Interpretation: Negative correlation")
    else:
        print("Interpretation: No correlation")


# X,Y
# 10,20
# 20,25
# 30,30
# 40,35
# 50,45
# 60,50

# covariance formula
'''
(1/n) summation(Xi - meanX) (Yi - meanY)
'''

# variance formula
'''
(1/n-1) summation(Xi - meanX)^2 
similarly for  Y dataset

SD = root of variance

r = cov(x,y) / Sd.x * Sd.y

'''