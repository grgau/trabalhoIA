from algoritmoGenetico import AlgoritmoGenetico
from hdbscancluster import HDBScan

import warnings
import pandas as pd
import numpy as np

def main():
  entrada = pd.read_csv('../7483_patients.csv', header=None)

  parametros = {
    'algorithm' : ['best', 'generic', 'prims_kdtree', 'prims_balltree', 'boruvka_kdtree', 'boruvka_balltree'],
    'min_cluster_size' : [2<<exponent for exponent in range(7)],
    'min_samples': [1<<exponent for exponent in range(6)],
    'cluster_selection_method' : ['eom', 'leaf'],
    'cluster_selection_epsilon' : np.around(np.arange(0.1, 0.7, 0.05), decimals=2).astype(type('float', (float,), {})),
    'metric': ['euclidean', 'manhattan', 'jaccard'],
    'entrada': entrada
  }

  #criação do algoritmo genético e da população inicial
  tamanho_populacao = 20
  num_geracoes = 10
  algoritmo = AlgoritmoGenetico(parametros, 0.2, 0.4, 0.1, HDBScan)
  populacao = algoritmo.criaPopulacao(tamanho_populacao)

  for i in range(0, num_geracoes):
    print('Geração: ' + str(i+1))
    print('Fitness: ' + str(algoritmo.mediaPopulacao(populacao)))

    for pop in populacao:
      pop.printSelf()
      print('---------\n')

    populacao = algoritmo.evoluiGeracao(populacao)

if __name__ == '__main__':
  warnings.simplefilter('ignore', UserWarning)
  main()
