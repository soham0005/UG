import csv
import math

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            for key, value in row.items():
                try:
                    row[key] = float(value)
                except ValueError:
                    pass 
            data.append(row)
    return data

def calculate_mean(data, attribute):
    values = [row[attribute] for row in data]
    return sum(values) / len(values)

def calculate_median(data, attribute):
    values = sorted([row[attribute] for row in data])
    n = len(values)
    mid = n // 2
    if n % 2 == 0:
        return (values[mid - 1] + values[mid]) / 2
    else:
        return values[mid]

def calculate_mode(data, attribute):
    values = [row[attribute] for row in data]
    return max(set(values), key=values.count)

def calculate_standard_deviation(data, attribute, mean):
    values = [row[attribute] for row in data]
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

def calculate_z_score(data, attribute):
    
    values = [row[attribute] for row in data]
    mean = calculate_mean(data, attribute)
    std_dev = calculate_standard_deviation(data, attribute, mean)
    return [round((x - mean) / std_dev, 4) for x in values]

def min_max_normalization(data, attribute, scale_range):
    values = [row[attribute] for row in data]
    old_min = min(values)
    old_max = max(values)
    new_min, new_max = scale_range
    return [round(((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min, 4) for x in values]

def suggest_range(min_value, max_value, mean):
    if max_value - min_value > 10000:
        return (1000, 10000)
    elif max_value - min_value > 1000:
        return (100, 1000)
    else:
        return (0, 1)


def main():
    file_path = 'Dry_Bean_Dataset_CSV.csv'
    try:
        seed_data = read_csv(file_path)
        
        numeric_attributes = [attr for attr, value in seed_data[0].items() 
                            if isinstance(value, (int, float))]

        for attr in numeric_attributes:
            try:
                values = [row[attr] for row in seed_data]
                mean = calculate_mean(seed_data, attr)
                min_value = min(values)
                max_value = max(values)
                
                # Calculate suggested range based on current column details
                suggested_range = suggest_range(min_value, max_value, mean)
                
                print(f"\n{attr}:")
                print(f"Current Min: {min_value}")
                print(f"Current Max: {max_value}")
                print(f"Current Mean: {mean:.4f}")
                print(f"Suggested Range: {suggested_range}")
                
                # Get user input for normalization range for this attribute
                print(f"\nEnter scale range for '{attr}' (or press Enter to use suggested range):")
                min_range_input = input(f"Enter minimum value for normalization (suggested: {suggested_range[0]}): ")
                max_range_input = input(f"Enter maximum value for normalization (suggested: {suggested_range[1]}): ")
                
                min_range = float(min_range_input) if min_range_input else suggested_range[0]
                max_range = float(max_range_input) if max_range_input else suggested_range[1]
                
                scale_range = (min_range, max_range)
                
                median = calculate_median(seed_data, attr)
                mode = calculate_mode(seed_data, attr)
                z_scores = calculate_z_score(seed_data, attr)
                normalized_data = min_max_normalization(seed_data, attr, scale_range)

                print(f"\n{attr} normalization results:")
                print(f"Mean: {mean:.4f}")
                print(f"Median: {median:.4f}")
                print(f"Mode: {mode:.4f}")
                print(f"Z-scores (first 5): {z_scores[:5]}")
                print(f"Min-Max Normalized data (first 5): {normalized_data[:5]}")

            except KeyError:
                print(f"Warning: Column '{attr}' not found in the dataset")
            except Exception as e:
                print(f"Error processing {attr}: {str(e)}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError as e:
        print(f"Error: Please enter valid numeric values for scales. {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
