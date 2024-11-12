import csv
import math

def read_distance_matrix_from_csv(file_name):
    labels = []
    matrix = []
    
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        labels = header[1:]
        
        for row in reader:
            distances = [float(d) for d in row[1:]]
            matrix.append(distances)
    
    return matrix, labels

def save_distance_matrix(matrix, labels, file_name):
    with open(file_name, 'a') as f:
        f.write("\nDistance Matrix:\n")
        
        max_label_len = max(len(str(label)) for label in labels) + 2
        
        header = " " * max_label_len + "|"
        for label in labels:
            header += f"{str(label):>7} "
        f.write(header + "\n")
        
        separator = "-" * max_label_len + "+" + "-" * (8 * len(labels))
        f.write(separator + "\n")
        
        for i in range(len(matrix)):
            row = f"{str(labels[i]):<{max_label_len}}|"
            for j in range(len(matrix[i])):
                row += f"{matrix[i][j]:>7.2f} "
            f.write(row + "\n")
        f.write("\n")

def find_min_distance(matrix):
    min_distance = float('inf')
    min_i, min_j = -1, -1
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] > 0 and matrix[i][j] < min_distance:
                min_distance = matrix[i][j]
                min_i, min_j = i, j
    return min_i, min_j, min_distance

def update_distance_matrix(old_matrix, min_i, min_j):
    n = len(old_matrix) - 1
    new_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    row_idx = 0
    for i in range(len(old_matrix)):
        if i == min_i or i == min_j:
            continue
        col_idx = 0
        for j in range(len(old_matrix)):
            if j == min_i or j == min_j:
                continue
            new_matrix[row_idx][col_idx] = old_matrix[i][j]
            col_idx += 1
        row_idx += 1
    
    new_distances = []
    for i in range(len(old_matrix)):
        if i not in [min_i, min_j]:
            new_distance = max(old_matrix[i][min_i], old_matrix[i][min_j])
            new_distances.append(new_distance)
    
    for i in range(len(new_distances)):
        new_matrix[i][n-1] = new_distances[i]
        new_matrix[n-1][i] = new_distances[i]
    
    return new_matrix

def agglomerative_clustering(distance_matrix, labels, output_file):
    with open(output_file, 'w') as f:
        f.write("Agglomerative Clustering Process\n")
        f.write("===============================\n\n")
        f.write("Initial clusters: " + ", ".join(labels) + "\n\n")
    
    current_matrix = [row[:] for row in distance_matrix]
    current_labels = labels[:]
    
    save_distance_matrix(current_matrix, current_labels, output_file)

    iteration = 1
    while len(current_matrix) > 1:
        min_i, min_j, min_distance = find_min_distance(current_matrix)
        
        if min_i == -1 or min_j == -1:
            break
            
        with open(output_file, 'a') as f:
            f.write(f"Iteration {iteration}: Merging clusters {current_labels[min_i]} and {current_labels[min_j]}\n")
            f.write(f"Distance between merged clusters: {min_distance:.2f}\n\n")

        new_label = f"({current_labels[min_i]},{current_labels[min_j]})"
        
        remaining_labels = [label for idx, label in enumerate(current_labels) if idx not in [min_i, min_j]]
        remaining_labels.append(new_label)
        current_labels = remaining_labels

        current_matrix = update_distance_matrix(current_matrix, min_i, min_j)
        save_distance_matrix(current_matrix, current_labels, output_file)
        
        iteration += 1

    with open(output_file, 'a') as f:
        f.write("Clustering Complete!\n")
        f.write(f"Final cluster: {current_labels[0]}\n")

    return current_matrix, current_labels

if __name__ == "__main__":
    input_file = 'DM_11_Agglomeritive_data.csv'
    output_file = 'clustering_output.txt'
    
    input_matrix, input_labels = read_distance_matrix_from_csv(input_file)
    final_matrix, final_labels = agglomerative_clustering(input_matrix, input_labels, output_file)