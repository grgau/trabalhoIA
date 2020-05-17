import random
from hdbscan import HDBSCAN
from collections import Counter
from numpy import log

class HDBScan():
  def __init__(self, parametros=None):
    self.parametros = {}
    self.entrada = parametros['entrada']
    if parametros != None:
      for parametro in parametros:
        if parametro is not 'entrada':
          self.parametros[parametro] = random.choice(parametros[parametro])

  def fitness(self):
    clusterer = HDBSCAN(algorithm = self.parametros['algorithm'], 
                        min_cluster_size = self.parametros['min_cluster_size'], 
                        min_samples = self.parametros['min_samples'],
                        cluster_selection_method = self.parametros['cluster_selection_method'],
                        cluster_selection_epsilon = self.parametros['cluster_selection_epsilon'],
                        gen_min_span_tree = True)

    clusterer.fit(self.entrada)
    score = self.balance(clusterer.labels_)
    return score

  def balance(self, data):
    n = len(data)
    classes = [(clas,float(count)) for clas,count in Counter(data).items()]
    k = len(classes)

    H = -sum([(count/n) * log((count/n)) for clas,count in classes]) #shannon entropy
    return H/log(k)

  def printSelf(self):
    for parametro in self.parametros:
      print('        Parametro: ' + str(parametro) + ' -- ' + str(self.parametros[parametro]))
