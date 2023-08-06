import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, cluster
from queue import Queue
import os

def show(dataset):
    plt.scatter(dataset[0][:,0], dataset[0][:,1], s = 1, c = dataset[1])
    plt.show()

def circles():
    return datasets.make_circles(n_samples = 1500, factor = .5, noise = .05, random_state = 50)

def moons():
    return datasets.make_moons(n_samples= 1500, noise=.05, random_state = 8)

def blobs(n_samples= 1500):
    return datasets.make_blobs(n_samples=n_samples, random_state=8)

def smashed():
    random_state = 170
    X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
    transformation = [[0.6, -0.6], [-0.4, 0.8]]
    X_aniso = np.dot(X, transformation)
    aniso = (X_aniso, y)
    return aniso

def varied():
    random_state = 170
    return datasets.make_blobs(n_samples=150, cluster_std=[1.0, 2.5, 0.5], random_state=random_state)

class KMeansexample:

    def __init__(self, k = 5, dataset = 'blobs'):
        # create the dataset
        if dataset == 'blobs':
            self.X, self.y = blobs()
        elif dataset == 'moons':
            self.X, self.y = moons()
        else:
            raise(Exception('Something went wrong with the dataset'))
        # step count
        self.i = 0
        # number of clusters
        self.k = k
        # container of the clusters
        self.clusters = []

        self.centroids = [self.X[i + 2] for i in range(self.k)]

        # show the initial points
        plt.scatter(self.X[:, 0], self.X[:, 1], s = 1)
        plt.title(f"ESEMPIO K-Means: inizializzazione \n steps: {self.i}")
        plt.show()

    def calc_distance(self, x1, x2):
        """Euclidean distance function"""
        return (sum((x1 - x2) ** 2)) ** 0.5

    def assign_clusters(self):
        self.clusters = []
        for i in range(self.X.shape[0]):
            distances = []
            for centroid in self.centroids:
                distances.append(self.calc_distance(centroid, self.X[i]))
            cluster = [z for z, val in enumerate(distances) if val == min(distances)]
            self.clusters.append(cluster[0])
        self.i += 1

    # Calculate new centroids based on each cluster's mean
    def calc_centroids(self):
        new_centroids = []
        for c in range(self.k):
            current_cluster = self.X[np.array(self.clusters) == c]
            cluster_mean = current_cluster.mean(axis=0)
            new_centroids.append(cluster_mean)
        self.centroids = new_centroids

    def show(self):
        # show points
        plt.scatter(self.X[:,0], self.X[:,1], s = 1, c = self.clusters, cmap = 'Set2')
        # show centroids
        plt.scatter(np.array(self.centroids)[:, 0], np.array(self.centroids)[:, 1], marker='+', c='red')
        plt.title(f"ESEMPIO K-Means: \n steps: {self.i}")
        plt.show()

    def step(self):
        self.calc_centroids()
        self.assign_clusters()

    def fit(self):
        self.assign_clusters()
        for i in range(500):
            clusters = self.clusters
            self.step()
            if clusters == self.clusters:
                break
        self.show()

class DBSCANexample:

    def __init__(self, epsilon=0.2, min_points=5):
        self.X, self.y = moons()

        self.epsilon = epsilon
        self.min_points = min_points
        self.noise = 0
        self.cluster_label = 0
        self.i = 0
        # Create labels column initialized to -1 (unclassified)
        self.labels = np.array([[-1] * 1500]).reshape(-1, 1)

        # show the initial points
        plt.scatter(self.X[:, 0], self.X[:, 1], s = 1)
        plt.title(f"ESEMPIO DBSCAN: inizializzazione \n steps: {self.i}")
        plt.show()

    def find_points(self):
        point = self.X[0]
        figure, axes = plt.subplots()
        plt.scatter(self.X[:, 0], self.X[:, 1], s = 1)
        plt.scatter(point[0], point[1], color = 'k', marker = 'x')
        draw_circle = plt.Circle((point[0], point[1]), self.epsilon, fill=False)

        axes.set_aspect(1)
        axes.add_artist(draw_circle)
        plt.show()

    def assign_neighbors(self):
        point = self.X[0]
        figure, axes = plt.subplots()
        plt.scatter(self.X[:, 0], self.X[:, 1], s=1)
        plt.scatter(point[0], point[1], color='k', marker='x')
        draw_circle = plt.Circle((point[0], point[1]), self.epsilon, fill=False)

        neighbors = self.find_neighbors(point)
        plt.scatter(self.X[neighbors, 0], self.X[neighbors, 1], s=1, c= 'red')

        axes.set_aspect(1)
        axes.add_artist(draw_circle)
        plt.show()

    def find_neighbors(self, point):
        neighbors = []

        for y in range(len(self.X)):
            q = self.X[y]
            if self.dist(point, q) <= self.epsilon:
                neighbors.append(y)

        return neighbors

    def fit(self):
        "Fit the data"

        for x in range(len(self.X)):

            # if the point is not labeled already then search for neighbors
            if self.labels[x] != -1:
                continue

            # find neighbors
            p = self.X[x]
            neighbors = self.find_neighbors(p)

            # If less neighbors than min_points then label as noise and continue
            if len(neighbors) < self.min_points:
                self.labels[x] = self.noise
                continue

            # increment cluster label
            self.cluster_label += 1

            # set current row to new cluster label
            self.labels[x] = self.cluster_label

            # create seed set to hold all neighbors of cluster including the neighbors already found
            found_neighbors = neighbors

            # create Queue to fold all neighbors of cluster
            q = Queue()

            # add original neighbors
            for neighbor in neighbors:
                q.put(neighbor)

            # While isn't empty label new neighbors to cluster
            while not q.empty():

                current = q.get()

                # if cur_row labeled noise then change to cluster label (border point)
                if self.labels[current] == self.noise:
                    self.labels[current] = self.cluster_label

                # If label is not -1(unclassified) then continue
                if self.labels[current] != -1:
                    continue

                # label the neighbor
                self.labels[current] = self.cluster_label

                # look for neighbors of cur_row
                point = self.X[current]
                neighbors2 = self.find_neighbors(point)

                # if neighbors2 >= min_points then add those neighbors to seed_set
                if len(neighbors2) >= self.min_points:

                    for neighbor in neighbors2:
                        if neighbor not in found_neighbors:
                            q.put(neighbor)
                            found_neighbors.append(neighbor)

        plt.scatter(self.X[:, 0], self.X[:, 1], s=1, c=self.labels, cmap='Set1')
        plt.show()

    def dist(self, x1, x2):
        """Euclid distance function"""
        return (sum((x1 - x2) ** 2)) ** 0.5

class MEANSHIFTexample:

    def __init__(self, radius=4):
        self.X, self.y = varied()
        self.radius = radius
        self.centroids = {}
        for i in range(len(self.X)):
            self.centroids[i] = self.X[i]
        self.i = 0
        # Create labels column initialized to -1 (unclassified)
        #self.labels = np.array([[-1] * 1500]).reshape(-1, 1)

        # show the initial points
        plt.scatter(self.X[:, 0], self.X[:, 1], s=1)
        plt.title(f"ESEMPIO MEAN SHIFT: inizializzazione \n steps: {self.i} \n numero di centroidi: {len(self.centroids)}")
        plt.show()

    def step(self):
        data = self.X
        new_centroids = []
        for i in range(len(self.centroids)):
            in_bandwidth = []
            centroid = self.centroids[i]
            for featureset in data:
                if np.linalg.norm(featureset - centroid) < self.radius:
                    in_bandwidth.append(featureset)

            new_centroid = np.average(in_bandwidth, axis=0)
            new_centroids.append(tuple(new_centroid))

        uniques = sorted(list(set(new_centroids)))

        self.centroids = []
        for i in range(len(uniques)):
            self.centroids.append(uniques[i])

    def show(self, centroidi=True):
        figure, axes = plt.subplots()
        plt.scatter(self.X[:, 0], self.X[:, 1], s=1)

        for c in range(len(self.centroids)):
            if centroidi:
                plt.scatter(self.centroids[c][0], self.centroids[c][1], color='k', marker='x')
            draw_circle = plt.Circle((self.centroids[c][0], self.centroids[c][1]), self.radius, fill=False)

            axes.set_aspect(1)
            axes.add_artist(draw_circle)

        plt.title(f"ESEMPIO MEAN SHIFT: \n steps: {self.i} \n numero di centroidi: {len(self.centroids)}")
        plt.show()

    def fit(self):

        while True:
            prev_centroids = self.centroids
            self.step()
            self.i += 1

            optimized = True

            for i in range(len(self.centroids)):
                if not np.array_equal(self.centroids[i], prev_centroids[i]):
                    optimized = False
                if not optimized:
                    break

            if optimized:
                break
        self.show()

class Challenge1:

    def __init__(self):
        self.description = "Un laboratorio di microbiologia sta analizzando dei minuscoli vermi che crescono in dei vetrini." \
                           "Devono analizzare la velocità con cui si riproducono, quindi contare quanti vermi ci sono in " \
                           "ogni singolo vetrino, solo ce ne sono un'infinità! Ti chiedono quindi di creare un algoritmo per contarli " \
                           "automaticamente. Ci riuscirai?"

        X = []
        pt = os.path.dirname(os.path.realpath(__file__))
        fin = open(pt+'challenges/worms_2d.txt')
        for i in fin:
            i = i.strip()
            i = i.split(',')
            X.append([float(j) for j in i])
        fin.close()
        self.X = np.array(X)

    def show(self):
        plt.scatter(self.X[:, 0], self.X[:, 1], s=0.001)
        plt.title('Challenge 1: WORMS')
        plt.show()

    def analizza(self, algoritmo, parametri):
        if algoritmo == 'k-means':
            clf = cluster.KMeans(n_clusters=parametri['k'], random_state=0).fit(self.X)

        if algoritmo == 'mean shift':
            clf = cluster.MeanShift(bandwidth=parametri['raggio']).fit(self.X)

        if algoritmo == 'DBSCAN':
            clf = cluster.DBSCAN(eps=parametri['eps']).fit(self.X)

        plt.scatter(self.X[:, 0], self.X[:, 1], s=0.001, c=clf.labels_)
        plt.title(f'Challenge 1: WORMS \n algoritmo:{algoritmo} \n parametri:{parametri}')
        plt.show()
