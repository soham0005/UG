import csv
import random

def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append([float(val) for val in row])
    return data

def initialize_centroids(data, k):
    return random.sample(data, k)

def assign_clusters(data, centroids):
    clusters = [[] for _ in centroids]
    for point in data:
        distances = [((point[0] - c[0]) ** 2 + (point[1] - c[1]) ** 2) ** 0.5 for c in centroids]
        min_dist_idx = distances.index(min(distances))
        clusters[min_dist_idx].append(point)
    return clusters

def update_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if len(cluster) == 0:
            continue
        avg_x = sum([point[0] for point in cluster]) / len(cluster)
        avg_y = sum([point[1] for point in cluster]) / len(cluster)
        new_centroids.append([avg_x, avg_y])
    return new_centroids

def kmeans(data, k, output_file, max_iters=100):
    centroids = initialize_centroids(data, k)
    with open(output_file, 'w') as file:
        for iteration in range(max_iters):
            file.write(f"\nIteration {iteration + 1}:\n")
            clusters = assign_clusters(data, centroids)
            for i, cluster in enumerate(clusters):
                file.write(f"Cluster {i + 1} - Centroid: {centroids[i]}\n")
                file.write(f"Points: {cluster}\n")
            new_centroids = update_centroids(clusters)
            if new_centroids == centroids:
                break
            centroids = new_centroids
        file.write("\nFinal Clusters and Points:\n")
        for i, cluster in enumerate(clusters):
            file.write(f"Cluster {i + 1} - Centroid: {centroids[i]}\n")
            file.write(f"Points: {cluster}\n")
    return clusters

filename = 'data.csv'
output_file = 'kmeans_output.txt'
k = 3
data = load_data(filename)
kmeans(data, k, output_file)
