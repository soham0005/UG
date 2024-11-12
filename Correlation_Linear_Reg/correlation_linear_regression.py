import csv
import math

def read_csv(filename):
    X, Y = [], []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            X.append(float(row[0]))
            Y.append(float(row[1]))
    return X, Y

def find_mean(values):
    mean_value = sum(values) / len(values)
    return mean_value

def find_covariance(a, b, mean_a, mean_b):
    covariance = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(len(a))) / len(a)
    return covariance

def find_standard_deviation(values, mean):
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)

def find_correlation(a, b):
    mean_a = find_mean(a)
    mean_b = find_mean(b)
    
    # Save output to the file
    output = f"Mean of X: {mean_a}\nMean of Y: {mean_b}\n"
    
    covariance = find_covariance(a, b, mean_a, mean_b)
    output += f"Covariance: {covariance}\n"
    
    sd_a = find_standard_deviation(a, mean_a)
    sd_b = find_standard_deviation(b, mean_b)
    output += f"Standard Deviation of X: {sd_a}\nStandard Deviation of Y: {sd_b}\n"
    
    if sd_a == 0 or sd_b == 0:
        output += "Correlation cannot be calculated due to zero variance in one of the datasets.\n"
        return None, output
    
    correlation = covariance / (sd_a * sd_b)
    output += f"Pearson Correlation Coefficient (r): {correlation}\n"
    return correlation, output

def calculate_regression(X, Y):
    n = len(X)
    mean_X, mean_Y = find_mean(X), find_mean(Y)
    
    # Save output to the file
    output = f"Mean of X: {mean_X}\nMean of Y: {mean_Y}\n"
    
    num = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n))
    denom = sum((X[i] - mean_X) ** 2 for i in range(n))
    m = num / denom
    c = mean_Y - m * mean_X
    output += f"m (slope): {m}\nc (intercept): {c}\n"
    
    return m, c, output

def predict(m, c, new_X):
    return c + m * new_X

def main():
    filename = "data.csv"  
    X, Y = read_csv(filename)
    
    with open("correlation_output.txt", "w") as file:
        correlation, correlation_output = find_correlation(X, Y)
        file.write(correlation_output)
        
        if correlation is not None:
            file.write(f"Pearson Correlation Coefficient (r): {correlation:.4f}\n")
            if correlation > 0:
                file.write("Interpretation: Positive correlation\n")
            elif correlation < 0:
                file.write("Interpretation: Negative correlation\n")
            else:
                file.write("Interpretation: No correlation\n")
        else:
            file.write("Correlation cannot be calculated due to zero variance in one of the datasets.\n")
        
        # Calculate and write regression
        m, c, regression_output = calculate_regression(X, Y)
        file.write(regression_output)
        file.write(f"Linear Regression Equation: Y = {m:.2f} * X + {c:.2f}\n")
        
        # Display results in the console
        print(correlation_output)
        if correlation is not None:
            print(f"Pearson Correlation Coefficient (r): {correlation:.4f}")
            if correlation > 0:
                print("Interpretation: Positive correlation")
            elif correlation < 0:
                print("Interpretation: Negative correlation")
            else:
                print("Interpretation: No correlation")
        
        print(f"Linear Regression Equation: Y = {m:.2f} * X + {c:.2f}")
        
        # Predict a new Y value
        try:
            new_X = float(input("Enter a value of X to predict Y: "))
            predicted_Y = predict(m, c, new_X)
            print(f"Predicted Y for X = {new_X}: {predicted_Y:.2f}")
            file.write(f"Predicted Y for X = {new_X}: {predicted_Y:.2f}\n")
        except ValueError:
            print("Invalid input for prediction.")
            file.write("Invalid input for prediction.\n")

if __name__ == "__main__":
    main()