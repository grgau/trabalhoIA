import random

class AlgoritmoGenetico():
  def __init__(self, parametros_algoritmo, chance_mutacao, qntd_mantida, chance_manter, algoritmo_aplicado):
    self.parametros_algoritmo = parametros_algoritmo
    self.chance_mutacao = chance_mutacao
    self.qntd_mantida = qntd_mantida
    self.algoritmo_aplicado = algoritmo_aplicado
    self.chance_manter = chance_manter

  def criaPopulacao(self, tamanho_populacao):
    populacao = []
    for individuo in range(0, tamanho_populacao):
      novoIndividuo = self.algoritmo_aplicado(self.parametros_algoritmo)
      populacao.append(novoIndividuo)
    qualidadePopulacao = [ (individuo.fitness() , individuo) for individuo in populacao ]
    populacaoOrdenada = [ x[1] for x in sorted(qualidadePopulacao, key=lambda x: x[0], reverse=True) ]
    return populacaoOrdenada

  def fazFilho(self, mae, pai):
    filho = self.algoritmo_aplicado(self.parametros_algoritmo)

    for parametro in self.parametros_algoritmo:
      if parametro is not 'entrada':
        filho.parametros[parametro] = random.choice([ mae.parametros[parametro], pai.parametros[parametro] ])
    if self.chance_mutacao > random.random():
      filho = self.mutacao(filho)
    return filho

  def mutacao(self, individuo):
    geneMutado = random.choice( list(self.parametros_algoritmo.keys()) )
    individuo.parametros[geneMutado] = random.choice(self.parametros_algoritmo[geneMutado])
    return individuo

  def mediaPopulacao(self, populacao):
    mediaPopulacao = 0
    for individuo in populacao:
      mediaPopulacao = mediaPopulacao + individuo.fitness()
    mediaPopulacao =  float( mediaPopulacao/len(populacao) )
    return mediaPopulacao

  def evoluiGeracao(self, populacao):
    qntdPopulacaoMantida = int(self.qntd_mantida * len(populacao) )
    novaPopulacao = populacao[:qntdPopulacaoMantida]

    for individuo in populacao[qntdPopulacaoMantida:]:
      if self.chance_manter > random.random():
          novaPopulacao.append(individuo)

    for individuo in novaPopulacao:
      if self.chance_mutacao > random.random():
          individuo = self.mutacao(individuo)
    qntdFilhos = len(populacao) - len(novaPopulacao)

    filhos = []
    while len(filhos) < qntdFilhos:
      pai = random.randint(0, len(novaPopulacao) - 1 )
      mae = random.randint(0, len(novaPopulacao) - 1 )
      if pai != mae:
        filhos.append( self.fazFilho(novaPopulacao[mae], novaPopulacao[pai]) )
    novaPopulacao.extend(filhos)

    qualidadePopulacao = [ (individuo.fitness() , individuo) for individuo in novaPopulacao ]
    populacaoOrdenada = [ x[1] for x in sorted(qualidadePopulacao, key=lambda x: x[0], reverse=True) ]
    return populacaoOrdenada
