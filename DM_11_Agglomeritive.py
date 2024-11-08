import csv
import math

def euclidean_distance(point1, point2):
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

def print_distance_matrix(matrix, labels):
    print("\nDistance Matrix:")
   
    max_label_len = max(len(str(label)) for label in labels) + 2
    
    header = " " * max_label_len + "│ "
    for label in labels:
        header += f"{str(label):>7} "
    print(header)
    
   
    separator = "─" * max_label_len + "┼" + "─" * (8 * len(labels) + 1)
    print(separator)
    
   
    for i in range(len(matrix)):
        row = f"{str(labels[i]):<{max_label_len}}│ "
        for j in range(len(matrix[i])):
            row += f"{matrix[i][j]:>7.2f} "
        print(row)

def read_data_from_csv(file_name):
    data = []
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            point_id = int(row[0])
            x = float(row[1])
            y = float(row[2])
            data.append((point_id, x, y))
    return data

def create_distance_matrix(clusters):
    n = len(clusters)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = euclidean_distance(clusters[i][0], clusters[j][0])
    return matrix

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
            # new_distance = min(old_matrix[i][min_i], old_matrix[i][min_j]) # Change this for Average and Complete Linkage
            new_distance = max(old_matrix[i][min_i], old_matrix[i][min_j])

            new_distances.append(new_distance)
    
   
    for i in range(len(new_distances)):
        new_matrix[i][n-1] = new_distances[i]
        new_matrix[n-1][i] = new_distances[i]
    
    return new_matrix

def agglomerative_clustering(data):
    # Initialize clusters
    clusters = [[point] for point in data]
    labels = [str(point[0]) for point in data]
    
    distance_matrix = create_distance_matrix(clusters)
    print_distance_matrix(distance_matrix, labels)

    while len(clusters) > 1:
        min_i, min_j, min_distance = find_min_distance(distance_matrix)
        
        if min_i == -1 or min_j == -1:
            break

        print(f"\nMerging Points {labels[min_i]} and {labels[min_j]} with distance {min_distance:.2f} as the minimum distance")

        merged_cluster = clusters[min_i] + clusters[min_j]
        
        new_label = f"({labels[min_i]},{labels[min_j]})"

        clusters = [cluster for idx, cluster in enumerate(clusters) if idx not in [min_i, min_j]]
        clusters.append(merged_cluster)

        remaining_labels = [label for idx, label in enumerate(labels) if idx not in [min_i, min_j]]
        remaining_labels.append(new_label)
        labels = remaining_labels

        distance_matrix = update_distance_matrix(distance_matrix, min_i, min_j)
        print_distance_matrix(distance_matrix, labels)

    return clusters

if __name__ == "__main__":
    file_name = 'DM_11_Agglomeritive_data.csv'
    sample_data = read_data_from_csv(file_name)
    final_clusters = agglomerative_clustering(sample_data)