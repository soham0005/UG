import csv

def calculate_total_weight(a_value, b_value):
    if a_value + b_value == 0:
        return 0
    return (a_value / (a_value + b_value)) * 100

def calculate_direct_weight(current_value, total_value):
    if total_value == 0:
        return 0
    return (current_value / total_value) * 100

def read_from_csv(filename):
    regions = []
    valuesA = []
    valuesB = []
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row

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

def save_weights_to_txt(filename, regions, valuesA, valuesB, t_wt_A, t_wt_B, d_wt_A, d_wt_B, total_counts):
    try:
        with open(filename, mode='w') as file:
            for i in range(len(regions)):
                file.write(f"Region: {regions[i]}\n")
                file.write(f"  A Count: {valuesA[i]}, t-weight: {t_wt_A[i]:.2f}%, d-weight: {d_wt_A[i]:.2f}%\n")
                file.write(f"  B Count: {valuesB[i]}, t-weight: {t_wt_B[i]:.2f}%, d-weight: {d_wt_B[i]:.2f}%\n")
                file.write(f"  Total Count: {total_counts[i]}\n\n")
        print(f"Success: Data has been written to {filename}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    input_filename = "DM_05_t_wt_d_wt_Dataset.csv"
    output_filename = "output.txt"
    regions, valuesA, valuesB = read_from_csv(input_filename)

    if regions is None or valuesA is None or valuesB is None:
        return

    total_counts = [int(a + b) for a, b in zip(valuesA, valuesB)]

    t_wt_A = [calculate_total_weight(valuesA[i], valuesB[i]) for i in range(len(regions))]
    t_wt_B = [calculate_total_weight(valuesB[i], valuesA[i]) for i in range(len(regions))]

    totalA = sum(valuesA)
    totalB = sum(valuesB)
    d_wt_A = [calculate_direct_weight(valuesA[i], totalA) for i in range(len(regions))]
    d_wt_B = [calculate_direct_weight(valuesB[i], totalB) for i in range(len(regions))]

    save_weights_to_txt(output_filename, regions, valuesA, valuesB, t_wt_A, t_wt_B, d_wt_A, d_wt_B, total_counts)

if __name__ == "__main__":
    main()
