# Title     : Algoritmo Genético Completo -> USANDO A BIBLIOTECA DEAP
# Objective : Neste laboratório vamos aprimorar nosso GA tornando-o mais próximo de uma aplicação real, onde poderemos ter milhões de registros e nos favorecermos do poder dessa biblioteca
# Created by: accol
# Created on: 11/06/2020


# Neste laboratório faremos o ciclo completo -> gerar população inicial -> avaliar população -> selecionar os pais -> crossover -> mutação -> avaliar a população -> definir a população sobrevivente
# Criaremos uma nova tabela de produtos no MySql
# Criaremos uma base de dados no MySql e por fim integraremos nosso código ao banco para realizar as ações do GA na busca da melhor solução para nossa empresa de logistica
# Note que adiconaremos um campo -> quantidade que deverá representar a quantidade de elementos no estoque tornando nosso algoritmo mais realista
# Atenção criação de tabelas e base de dados estão fora do nosso escopo, daremos aqui algumas dicas
# Usaremos o MySql Workbench para essas ações
#   1- primeiramente criaremos uma base de dados com: create database produtos;
#   2- para usarmos a base criada é necessário: use produtos;
#   3- criando a tabela produtos: create table produtos (
#	                                idproduto int not null auto_increment,
#                                   nome varchar(50) not null,
#                                   espaco float not null,
#                                   valor float not null,
#                                   quantidade int not null,
#                                   constraint pk_produtos_iddproduto primary key (idproduto)
#                                 );
#   4- vamos inserir os produtos na tabela: insert into produtos (nome, espaco, valor, quantidade) values ('Geladeira Dako', 0.751, 999.9, 1);

# Para fazermos conexão com o banco de dados precisaremos instalar um novo pacote => "RMySQL"

# Atenção -> pode ser que encontre esse erro ao tentar conectar-se ao banco: "cahing_sha2_password" can not be loaded
#   Resolva assim:
#     Abra o terminal (cmd)
#     Digite o seguinte comando: mysql -u root -p
#     Logado digite o comando: ALTER USER 'your mysql user'@'localhost' IDENTIFIED WITH my_native_password BY 'your mysql password';
#     Saia digitando: exit
#     Agora você só precisa abrir seu Workbranch e criar uma nova conexão
#     Para uma melhor explicação assista: https://www.youtube.com/watch?v=7CE42Tp2d2Y

# Estaremos reaproveitando o código desenvolvido no laboratório anterior

# A classe Indivíduo (nós ainda não estaremos construindo o conjunto de indivíduos). O indivíduo representa as soluções -> cada índiviuo definirá uma solução para o seu problema (qual a carga e o valor a ser transportado)=> num segundo momento deveremos encontrar o indivíduo que apresenta a solução mais interessante para a empresa. O conceito de cromossomo é melhor explicado aqui -> sendo parte do indivíduo ele irá representar a solução daquele indivíduo >>= Uma definição aceita quando se trabalha com AG mais simples é o fato de que o indivíduo pode ser o próprio cromossomo (na maneira mais simples possível) ou pode conter o cromossomo com um de seus atributos. Para este laboratório estaremos criando uma classe Indivíduo que terá o cromossoma como um de seus atributos. Um conjunto de indivíduos formam uma população => Acompanhe


import random
import numpy
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt


# Criando nossa classe Produto -> laboratório anterior

class Produto():  # Cria a classe produto
    def __init__(self, nome, espaco, valor): # Construtor da classe
        self.nome = nome    # Atributos da classe Produto
        self.espaco = espaco
        self.valor = valor

lista_produtos = []
lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
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

# Usando recursos da biblioteca deap
toolbox = base.Toolbox()    # Inicializa os recursos da biblioteca
creator.create('FitnessMax', base.Fitness, weights = (1.0, )) # Peso pode ter múltiplos valores, daí o espaço em branco, no caso queremos os valores mais próximos a 1 possível
creator.create('Individual', list, fitness = creator.FitnessMax) # Aqui teremos os valores 0 e 1 do cromossomo indicando se ele irá levar ou não oproduto
toolbox.register('attr_bool', random.randint, 0, 1)
# A seguir a criação dos indivíduos
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_bool, n = len(espacos))
# Gerar uma função para criação da população
toolbox.register('population', tools.initRepeat, list, toolbox.individual)

# A seguir criamos a função de avaliação => esta terá que ser realizada manualmente
def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
       if individual[i] == 1:   # Observe que não colocamos 1 entre aspas, pois a biblioteca trabalha com inteiros
           nota += valores[i]
           soma_espacos += espacos[i]
    if soma_espacos > limite:
        nota = 1
    return nota / 100000,   # Observe  necessidade da ','. Isso ocorre porque estamos avaliando weights = (1.0, ). O fator 100000 é usado para normalizar os valores numa escala entre 0 e 1

toolbox.register("evaluate", avaliacao) # Avaliação
toolbox.register("mate", tools.cxOnePoint) # Crossover
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.01) # Mutação -> 1% de chance de probabilidade
toolbox.register("select", tools.selRoulette) # Seleção de individuos para fazer o crossover

# Criamos agora a função main para realizar testes
if __name__ == "__main__":
#    random.seed(1) # Define uma semente para que sempre tenha os mesmos resultados -> bom para análise >>= Nota: para efeito de simulação deve-se deixar essa função comentada, caso contrário terá sempre os mesmos valores
    populacao = toolbox.population(n = 20) # Aqui efetivamente cria-se a população
    probabilidade_crossover = 1.0
    probabilidade_mutacao = 0.01
    numero_geracoes = 100
    
    estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
    # Vamos avaliar o valor máximo, mínimo, a média e o desvio padrão
    estatisticas.register("max", numpy.max)
    estatisticas.register("min", numpy.min)
    estatisticas.register("med", numpy.mean)
    estatisticas.register("std", numpy.std)
    
    populacao, info = algorithms.eaSimple(populacao, toolbox,
                                          probabilidade_crossover,
                                          probabilidade_mutacao,
                                          numero_geracoes, estatisticas)
    # Agora faremos a seleção do melhor elemento
    melhores = tools.selBest(populacao, 1)
    for individuo in melhores:
        print(individuo)
        print(individuo.fitness)
        #print(individuo[1])    # Para teste permite o acesso a cada gene do cromossomo
        soma = 0
        for i in range(len(lista_produtos)):
            if individuo[i] == 1:
                soma += valores[i]
                # Aqui mostramos cada produto que será transportado
                print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                           lista_produtos[i].valor))
        # Aqui será exibido a melhor solução
        print("Melhor solução: %s" % soma)
    # Plotando o gráfico com matplotlib
    valores_grafico = info.select("max")
    plt.plot(valores_grafico)
    plt.title("Acompanhamento dos valores")
    plt.show()
