import csv
import math

def read_csv(file_name):
    data = []
    try:
        with open(file_name, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                data.append(int(row[0])) 
    except FileNotFoundError:
        print(f"Error: Could not open the file {file_name}")
    
    return data

def write_to_file(file_name, median_binned, mean_binned, boundaries_binned):
    try:
        with open(file_name, mode='w') as file:
            file.write("Median Binning - ")
            file.write(" ".join(map(str, median_binned)))
            file.write("\n")

            file.write("Mean Binning - ")
            file.write(" ".join(map(str, mean_binned)))
            file.write("\n")

            file.write("Boundaries Binning - ")
            file.write(" ".join(map(str, boundaries_binned)))
            file.write("\n")

        print(f"Success: Results saved to {file_name}")
    except Exception as e:
        print(f"Error: Could not write to file {file_name}. Reason: {e}")

def binning_by_median(data, bin_size):
    if bin_size == 0:
        return data
    
    data.sort()
    binned_data = []

    for i in range(0, len(data), bin_size):
        bin_data = data[i:i+bin_size]
        median = bin_data[len(bin_data) // 2]
        binned_data.append([median] * len(bin_data))

    return binned_data

def binning_by_mean(data, bin_size):
    if bin_size == 0:
        return [float(x) for x in data]
    
    data.sort()
    binned_data = []

    for i in range(0, len(data), bin_size):
        bin_data = data[i:i+bin_size]
        mean = round(sum(bin_data) / len(bin_data), 2) 
        binned_data.append([mean] * len(bin_data))

    return binned_data

def binning_by_boundaries(data, bin_size):
    if bin_size == 0:
        return data
    
    data.sort()
    binned_data = []

    for i in range(0, len(data), bin_size):
        bin_data = data[i:i+bin_size]
        min_val = bin_data[0]
        max_val = bin_data[-1]
        bin_result = []
        for value in bin_data:
            if abs(value - min_val) < abs(value - max_val):
                bin_result.append(min_val)
            else:
                bin_result.append(max_val)
        binned_data.append(bin_result)

    return binned_data

def print_binning_info(original_data, binned_data, method_name, num_bins):
    print(f"\n--- {method_name} ---")
    print(f"Original Data: {original_data}")
    for bin_idx, bin_data in enumerate(binned_data, start=1):
        print(f"Bin {bin_idx}: {bin_data}")
    print(f"Total Bins Created: {num_bins}")


def equal_width_binning(data, num_bins):
    if num_bins <= 0:
        raise ValueError("Number of bins must be greater than zero.")
    
    min_val = min(data)
    max_val = max(data)
    
    bin_width = (max_val - min_val) / num_bins

    bins = [[] for _ in range(num_bins)]
    
    for value in data:
        bin_index = int((value - min_val) / bin_width)
        
        if bin_index == num_bins:
            bin_index = num_bins - 1
        
        bins[bin_index].append(value)
    
    return bins

# Using Equal Width
# if __name__ == "__main__":
#     # Sample data
#     data = [1, 5, 7, 10, 14, 18, 20, 24, 30, 35, 40, 45, 50]
#     num_bins = 5  # Specify the number of bins

#     binned_data = equal_width_binning(data, num_bins)

#     # Print binning results
#     for i, bin_data in enumerate(binned_data):
#         print(f"Bin {i + 1}: {bin_data}")


# Main code
if __name__ == "__main__":

    file_name = "DM_03_Binning_Data.csv"
    output_file = "DM_03_Binning_Output.csv"

    data = read_csv(file_name)

    if not data:
        print("Error: No data found or file could not be opened.")
    else:
        num_bins = int(input("Enter the number of bins: "))

        if num_bins <= 0:
            print("Error: Number of bins should be greater than 0.")
        else:
            
            bin_size = math.ceil(len(data) / num_bins)

            median_binned = binning_by_median(data, bin_size)
            print_binning_info(data, median_binned, "Median Binning", num_bins)

            mean_binned = binning_by_mean(data, bin_size)
            print_binning_info(data, mean_binned, "Mean Binning", num_bins)

            boundaries_binned = binning_by_boundaries(data, bin_size)
            print_binning_info(data, boundaries_binned, "Boundaries Binning", num_bins)


            
            flat_median_binned = [item for sublist in median_binned for item in sublist]
            flat_mean_binned = [item for sublist in mean_binned for item in sublist]
            flat_boundaries_binned = [item for sublist in boundaries_binned for item in sublist]

            write_to_file(output_file, flat_median_binned, flat_mean_binned, flat_boundaries_binned)
