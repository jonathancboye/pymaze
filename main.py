from maze import Maze
from algo import hunt_kill, recursive_backtracker, dijkstra, kruskals, prims, aldous_broder, recursive_division
from sklearn import feature_selection
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import math

def gen_data(rows, columns, algos, num):
    data = []
    target = []
    for fun in algos:
        for sample in range(num):
            maze = Maze(rows, columns, fun, 0)
            data.append([maze.twistiness, maze.dead_ends,
                         maze.longest_path, maze.directness,
                         maze.intersections, maze.average_path_length])
            target.append(maze.steps)
    return np.array(data), np.array(target)

def plot_PvA(algo_samples, algos, prediction, actual):
    linestyles = ['r--', 'b^', 'g-', 'y:', 'p-.', 'b-.']
    colors = ['r', 'g', 'b', 'y', 'm', 'k']
    markers = ['o', 'v', '<', '>', 'h', '+']
    scatter_items = []
    scatter_names = []
    plt.figure()
    for i in range(len(algos)):
        scatter_items.append(plt.scatter(prediction[algo_samples * i:algo_samples *(i + 1)],
                                            actual[algo_samples * i: algo_samples * (i + 1)],
                                            c=colors[i],
                                            marker=markers[i]))
        scatter_names.append(algos[i].__name__)
    plt.xlabel('prediction')
    plt.ylabel('actual')
    plt.xticks(range(0, 350, 25))
    plt.yticks(range(0, 350, 25))
    plt.legend(scatter_items, scatter_names, loc='upper right')
    plt.savefig("plot_PvA.png")

def plot_linreg(x_train, y_train, x_test, y_test, features):
    clf = linear_model.LinearRegression()
    plt.figure(figsize=(12,12))
    for f in range(len(features)):
        xi_test = x_test[ :, f]
        xi_train = x_train[ :, f]
        xi_test = xi_test[ :, np.newaxis]
        xi_train = xi_train[ :, np.newaxis]
        clf.fit(xi_train, y_train)
        y = clf.predict(xi_test)
        plt.subplot(3,3,f+1)
        plt.xlabel(features[f])
        plt.ylabel('steps')
        plt.scatter(xi_test, y_test, color='k')
        plt.plot(xi_test, y, color='b', linewidth = 3)
    plt.savefig("plot_linreg.png")

def plot_fhistogram(data):
    for i in range(6):
        plt.clf()
        plt.hist(np.array(data)[:,i],bins=40)
        plt.savefig("plot_hist" + str(i) + ".png")

def plot_thistogram(target, filename):
    plt.clf()
    plt.hist(target, bins=20)
    plt.savefig(filename)

features = ['twistiness',
            'dead_ends',
            'longest_path',
            'directness',
            'intersections',
            'average_path_length']
algo_samples = 20
rows = 15
columns = 15
algos = [recursive_backtracker, hunt_kill, kruskals, prims, aldous_broder, recursive_division]
train_data, train_target = gen_data(rows, columns, algos, 100)
test_data, test_target = gen_data(rows, columns, algos, algo_samples)

# print(clf.coef_)
# print(clf.score(test_data, test_target))
plot_linreg(train_data, train_target, test_data, test_target, features)
clf = linear_model.LinearRegression()
clf.fit(train_data, train_target)
y = clf.predict(test_data)
plot_PvA(algo_samples, algos, y, test_target)
print(clf.coef_)
print(clf.intercept_)
print(clf.score(test_data, test_target))

















