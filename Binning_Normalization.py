import csv
import math

def read_csv(file_name):
    try:
        with open(file_name, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header
            return [int(row[0]) for row in csvreader]
    except FileNotFoundError:
        print("File Not Found")
        return []

def binning_mean(data, bin_size):
    return [[round(sum(bin) / len(bin), 2)] * len(bin) for bin in create_bins(data, bin_size)]

def binning_median(data, bin_size):
    return [[bin[len(bin) // 2]] * len(bin) for bin in create_bins(data, bin_size)]

def binning_boundaries(data, bin_size):
    bins = create_bins(data, bin_size)
    return [[min(bin) if abs(x - min(bin)) < abs(x - max(bin)) else max(bin) for x in bin] for bin in bins]

def create_bins(data, bin_size):
    data.sort()
    return [data[i:i + bin_size] for i in range(0, len(data), bin_size)]

def z_score_normalization(data):
    mean = sum(data) / len(data)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in data) / (len(data) - 1)) if len(data) > 1 else 0
    return [round((x - mean) / std_dev, 4) if std_dev != 0 else 0 for x in data]

def normalize_bins(binned_data):
    zscore_bins = [z_score_normalization(bin) for bin in binned_data]
    return zscore_bins

def write_to_file(file_name, original_data, mean_binned, median_binned, boundaries_binned, zscore_data):
    with open(file_name, "w") as file:
        file.write("Original Data:\n")
        file.write(f"{original_data}\n\n")

        for title, binned_data, zscore_bins in [
            ("Mean Binning", mean_binned, zscore_data["mean"]),
            ("Median Binning", median_binned, zscore_data["median"]),
            ("Boundaries Binning", boundaries_binned, zscore_data["boundaries"])
        ]:
            file.write(f"{title}\n")
            for i, bin_data in enumerate(binned_data, start=1):
                file.write(f"Bin {i}: {bin_data}\n")
            file.write("\n")

            file.write(f"{title} - Z-score Normalized\n")
            for i, bin_data in enumerate(zscore_bins, start=1):
                file.write(f"Bin {i}: {bin_data}\n")
            file.write("\n")

if __name__ == "__main__":
    file_name = "DM_03_Binning_Data.csv"
    output_file = "Binning_Normalization_Output.txt"
    data = read_csv(file_name)
    if not data:
        print("No data found.")
    else:
        num_bins = int(input("Enter the number of bins: "))
        bin_size = math.ceil(len(data) / num_bins)
        
        mean_binned = binning_mean(data, bin_size)
        median_binned = binning_median(data, bin_size)
        boundaries_binned = binning_boundaries(data, bin_size)
        
        zscore_data = {
            "mean": normalize_bins(mean_binned),
            "median": normalize_bins(median_binned),
            "boundaries": normalize_bins(boundaries_binned)
        }
        
        write_to_file(output_file, data, mean_binned, median_binned, boundaries_binned, zscore_data)
