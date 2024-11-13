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
        next(reader)
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