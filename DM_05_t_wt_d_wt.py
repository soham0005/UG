import csv
from tabulate import tabulate

def calculate_total_weight(a_value, b_value):
    if a_value + b_value == 0:
        return 0
    return (a_value / (a_value + b_value)) * 100

def calculate_direct_weight(current_value, total_value):
    if total_value == 0:
        return 0
    return (current_value / total_value) * 100

def write_to_csv(filename, regions, valuesA, valuesB, t_wt_A, t_wt_B, d_wt_A, d_wt_B, total_counts):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Region", "A", "B", "t_wt_A (%)", "t_wt_B (%)", "d_wt_A (%)", "d_wt_B (%)", "Total"])
            for i in range(len(regions)):
                writer.writerow([regions[i], valuesA[i], valuesB[i], f"{t_wt_A[i]:.2f}", f"{t_wt_B[i]:.2f}", f"{d_wt_A[i]:.2f}", f"{d_wt_B[i]:.2f}", total_counts[i]])
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def read_from_csv(filename):
    regions = []
    valuesA = []
    valuesB = []
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header

            for row in csv_reader:
                regions.append(row[0])
                valuesA.append(float(row[1]))
                valuesB.append(float(row[2]))
        return regions, valuesA, valuesB
    except FileNotFoundError:
        print(f"Error: Unable to open file {filename}")
        return None, None, None
    except ValueError as e:
        print(f"Error: {e}")
        return None, None, None

def main():
    input_filename = "DM_05_t_wt_d_wt_Dataset.csv"
    regions, valuesA, valuesB = read_from_csv(input_filename)

    if regions is None or valuesA is None or valuesB is None:
        return

    total_counts = [int(a + b) for a, b in zip(valuesA, valuesB)]  # Calculate total counts

    t_wt_A = []
    t_wt_B = []
    d_wt_A = []
    d_wt_B = []

    for i in range(len(regions)):
        t_wt_A.append(calculate_total_weight(valuesA[i], valuesB[i]))
        t_wt_B.append(calculate_total_weight(valuesB[i], valuesA[i]))

    totalA = sum(valuesA)
    totalB = sum(valuesB)
    for i in range(len(regions)):
        d_wt_A.append(calculate_direct_weight(valuesA[i], totalA))
        d_wt_B.append(calculate_direct_weight(valuesB[i], totalB))

    output_filename = "output.csv"
    if write_to_csv(output_filename, regions, valuesA, valuesB, t_wt_A, t_wt_B, d_wt_A, d_wt_B, total_counts):
        print(f"Success: Data has been written to {output_filename}")

    table = []
    for i in range(len(regions)):
        table.append([regions[i], valuesA[i], valuesB[i], f"{t_wt_A[i]:.2f}", f"{t_wt_B[i]:.2f}", f"{d_wt_A[i]:.2f}", f"{d_wt_B[i]:.2f}", total_counts[i]])

    print(tabulate(table, headers=["Region", "A", "B", "t_wt_A (%)", "t_wt_B (%)", "d_wt_A (%)", "d_wt_B (%)", "Total"], tablefmt="grid"))

if __name__ == "__main__":
    main()

# T weight - multiple class
# D- weight - same class