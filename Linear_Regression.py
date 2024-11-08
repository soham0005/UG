import csv

def read_csv(filename):
    X, Y = [], []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            X.append(float(row[0]))
            Y.append(float(row[1]))
    return X, Y

def calculate_regression(X, Y):
    n = len(X)
    sum_X, sum_Y = sum(X), sum(Y)
    mean_X, mean_Y = sum_X / n, sum_Y / n

    num, denom = 0, 0
    for i in range(n):
        num += (X[i] - mean_X) * (Y[i] - mean_Y)
        denom += (X[i] - mean_X) ** 2
    
    m = num / denom
    c = mean_Y - m * mean_X
    return m, c

def predict(m, c, new_X):
    return c + m * new_X

def main():
    filename = "Linear_Regression_data.csv"
    X, Y = read_csv(filename)

    m, c = calculate_regression(X, Y)

    print("Slope:", m)
    print("Intercept:", c)

    new_X = float(input("Enter years of experience to predict salary: "))
    predicted_Y = predict(m, c, new_X)

    print(f"Predicted Salary for {new_X} years of experience: {predicted_Y:.2f}k")

if __name__ == "__main__":
    main()

# For Getting Intercept as negative
# YearsExperience,Salary
# 1,3.5
# 2,7
# 3,14
# 4,50,5,87

# m = (summation(1,n) (Xi - meanx) * (Yi - meanY) ) / summation(1,n)(Xi - meanX)^2
# c (intercept) = meanY - m * meanX