# Title     : Avaliação da população
# Objective : Neste laboratório vamos implementar a avaliação da população => em outras palavras, queremos aplicar os operadores Genéticos (Crossover e Mutação) e selecionar o indivíduo com a melhor opção de solução. A Nota mais alta do indivíduo deverá ser associada ao melhor uso do espaço do caminhão (meio de transporte). Indivíduo que extrapolem o limite da capacidade do meio de transporte serão penalizados e receberão nota = 1
# Created by: accol
# Created on: 11/06/2020


# Neste laboratório precisaremos criar uma função para ordenar -> de forma decrescente => os indivíduos com base no valor da nota alcançada

# Estaremos reaproveitando o código desenvolvido no laboratório anterior

# A classe Indivíduo (nós ainda não estaremos construindo o conjunto de indivíduos). O indivíduo representa as soluções -> cada índiviuo definirá uma solução para o seu problema (qual a carga e o valor a ser transportado)=> num segundo momento deveremos encontrar o indivíduo que apresenta a solução mais interessante para a empresa. O conceito de cromossomo é melhor explicado aqui -> sendo parte do indivíduo ele irá representar a solução daquele indivíduo >>= Uma definição aceita quando se trabalha com AG mais simples é o fato de que o indivíduo pode ser o próprio cromossomo (na maneira mais simples possível) ou pode conter o cromossomo com um de seus atributos. Para este laboratório estaremos criando uma classe Indivíduo que terá o cromossoma como um de seus atributos. Um conjunto de indivíduos formam uma população => Acompanhe


from random import random

# Criando nossa classe Produto -> laboratório anterior

class Produto():  # Cria a classe produto
    def __init__(self, nome, espaco, valor): # Construtor da classe
        self.nome = nome    # Atributos da classe Produto
        self.espaco = espaco
        self.valor = valor

# Criando a classe Indivíduo => espacos -> representa o espaço a ser utilizado no caminhão; valores -> representa o somatório dos valores dos produtos selecionados; limiteEspecos -> representará a capacidade do meio de transporte utilizado (inicialmente a capacidade do caminhão é de 3 metros cúbicos); notaAvaliacao -> será a nota atribuída à solução do indivíiduo (quanto melhor a proposta de solução melhor a nota); geracao -> aramazenará a geração do indivíduo (acompanhando o processo de evolução); cromossomo -> é aqui que teremos nossa sequência de zeros e uns (14 um bit para cada produto) a ser utilizado para definir a mercadoria que será levada e a mercadoria que será deixada (0 -> mercadoria fica 1 -> mercadoria transportada)

class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0 # Atributo necessário para a função de avaliação
        self.espaco_usado = 0   # Atributo necessário para a função de avaliação
        self.geracao = geracao
        self.cromossomo = [] # Esta lista contera o resultado sugerido pelo individuo

        for i in range(len(espacos)): # O objetivo desse for é inicializar a lista com valores aleatórios
            if random() < 0.5:  # Estamos considerando 50% => chances iguais
                self.cromossomo.append('0')
            else:
                self.cromossomo.append('1')
    
    # Vamos criar a função de avaliação. Nesta função vamos fazer o somatório do espaço e o somatório do valor da carga selecionada para o frete. Observer que estamos usando o termo nota ao invés de soma que é vocabulário comum em GA. A avaliação se dará pelo máximo valor transportando e melhor ocupação do espaço físico (caminhão)
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:  # Testa se a capacidade de transporte excedeu o volume do caminhão. Se isso ocorrer o indivíduo (cromossoma --> deve ser penalizado => nota baixa)
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
    # Vamos agora fazer a implementação da função de CROSSOVER
    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo)) # Define randomicamente o ponto de corte
        # A seguir a operação de crossover propriamente dito => gerando o cromossomo
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        # A seguir vamos criar um vetor chamado filhos --> cada um dos filhos deverão ser novos membros da classe Indivíduo
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        # Agora estaremos criando os cromossos ou melhor iniciando os filhos
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos

# Vamos agora construir nosso segundo operador Genético a MUTAÇÃO >>- criar diversidade a partir da alteração aleatória de indivíduos >-> é aplicada de forma menos frequente que a reprodução (trabalhar com probabilidade extremamente baixa) geralmente entre 1% e 5%
    def mutacao(self, taxa_mutacao):
        print('\nAntes da mutação %s ' % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:  # Teste para avaliar se a mutação será ou não aplicada
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        print('\nDepois da mutação %s ' % self.cromossomo)
        return self     # Retorno o próprio objeto com a mutação já feita

# Criaremos uma nova classe que deverá conter a solução do nosso problema. Em outras palavras, o objetivo dessa classe é encontrar a melhor solução para nosso problema
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):  # Observe que precisamos do self, pois estamos acessando atributo da própria classe
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        # Vamos setar o valor inicial como sendo a melhor solução ==> início dos trabahos
        self.melhor_solucao = self.populacao[0]
    
    # Criaremos agora uma função para ordenar de forma decrescente os indivíduos da população, com base na sua nota => usarmos a função order() com o parâmetro decreasing setado como TRUE do R que realiza essa operação de forma simples e direta
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_avaliacao, reverse = True)



if __name__ =='__main__':
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
    espacos = []
    valores = []
    nomes = []
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3  # Representa a capacidade máxima de transporte do caminhão 3 metros cubicos
    # Vamos criar uma variável que irá definir o tamanho da população
    tamanho_populacao = 20
    ag = AlgoritmoGenetico(tamanho_populacao)
    ag.inicializa_populacao(espacos, valores, limite)
    # Precisamos atribuir as notas para podermos classificar o melhor indivíduo
    for individuo in ag.populacao:
        individuo.avaliacao()
    ag.ordena_populacao()
    for i in range(ag.tamanho_populacao):
        print('*** Individuo %s ***\n' % i,
        'Espacos = %s\n' % str(ag.populacao[i].espacos),
        'Valores = %s\n' % str(ag.populacao[i].valores),
        'Cromossomo = %s\n' % str(ag.populacao[i].cromossomo),
        'nota = %s\n ' % ag.populacao[i].nota_avaliacao)
