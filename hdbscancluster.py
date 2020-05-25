import random
from hdbscan import HDBSCAN
from collections import Counter
from numpy import log
import pandas as pd
import json
from sklearn import metrics

class HDBScan():
  def __init__(self, parametros=None):
    self.parametros = {}
    self.data = pd.read_csv("../7483_patients.csv", header=None)
    if parametros != None:
      for parametro in parametros:
        self.parametros[parametro] = random.choice(parametros[parametro])

  def fitness(self):
    clusterer = HDBSCAN(algorithm = self.parametros["algorithm"],
                        min_cluster_size = self.parametros["min_cluster_size"],
                        min_samples = self.parametros["min_samples"],
                        cluster_selection_method = self.parametros["cluster_selection_method"],
                        cluster_selection_epsilon = self.parametros["cluster_selection_epsilon"])

    clusterer.fit(self.data)
    silhouette_score = self.silhouette_score(self.data, clusterer.labels_)

    # balance = self.balance(clusterer.labels_)
    # percents = self.calc_percents(clusterer.labels_)
    # len_labels = self.len_labels(clusterer.labels_)
    # noise_percents = [item for item in percents if item[0] == -1][0][1]

    score = silhouette_score

    # print(percents)
    # print("\n")
    # print('\'' + str(json.dumps(self.parametros)) + '\'')
    # print("\n")
    # print(score)
    # print("---------------------\n\n")

    return score

  def silhouette_score(self, X, labels):
    return metrics.silhouette_score(X, labels)

  def len_labels(self, labels):
    return len(Counter(labels).keys())

  def calc_percents(self, labels):
    c = Counter(labels)
    percents = [(i, c[i] / len(labels) * 100.0) for i in c]
    return sorted(percents, key=lambda tup: tup[1], reverse=True)

  def balance(self, labels):
    n = len(labels)
    classes = [(clas,float(count)) for clas,count in Counter(labels).items()]
    k = len(classes)

    H = -sum([(count/n) * log((count/n)) for clas,count in classes]) #shannon entropy
    return H/log(k)

  def printSelf(self):
    print('\'' + str(json.dumps(self.parametros)) + '\'')