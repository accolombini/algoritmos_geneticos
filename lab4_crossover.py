# Title     : Crossover -> Reprodução => trata-se de um operador genético
# Objective : Neste laboratório vamos trabalhar com um dos operadores de AG -> O CROSSOVER => utilizando R => Queremos preparar nossos indivíduos para que evoluam dentro da melhor expectativa para solução do problema (evolução dos indivíduos mais aptos)
# Created by: accol
# Created on: 11/06/2020


# A ideia por trás do crossover é combinar os genes dos pais para gerar um filho resultante desse cruzamento
#   Combina pedaços do cromossomo de dois genitores gerando filhos mais aptos e consequentemente com o passar das gerações a população tende a evoluir
#   Representa a reproduçào sexuada, pois na reprodução assexuada cada filho é idêntico a seu genitor e tem as mesmas habilidades, o que não cria/gera diversidade -> requisito fundamental para GA
#   O operador de crossover pode ser de um ponto (mais simples) a n pontos (mais complexa). No caso de crossover de um ponto, imagine um cromossomo com 7 gênes (0 1 0 1 0 1 0) -> teremos 6 pontos de cortes (interseção entre os gênes) => pense nos pontos de corte como sendo os espaços entres os gênes
#   A ideia é selecionar um desses pontos de corte por algum método aleatório. Feito isso, o próximo passo é a geração de dois filhos a partir dos genitores (cruzando os cromossomos). Considere: pa1 = 1 0 1 1 0 1 0 e pai2 = 0 1 0 0 1 1 1. Considere o ponto de crote entre o terceiro e o quarto gêne. Aplicando o operador de crossover teremos os seguintes filhos: filho1 = 1 0 1 0 1 1 1 e filho2 = 0 1 0 1 0 1 0

# Neste laboratório estaremos construindo a operação do crossover -> usaremos a mesma codificação desenvolvida nas aulas anteriores

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
    print('\nIndividuo 1\n')
    individuo1 = Individuo(espacos, valores, limite)
    print('\nIndividuo numero 1 --> Teste\n')
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == '1':
            print('Nome: %s R$ %s ' % (lista_produtos[i].nome, lista_produtos[i].valor))
# Teste da função de avaliação
individuo1.avaliacao()  # Chamada da função
print('\nAvaliacao do Individuo 1\n')
print('Nota = %s' % individuo1.nota_avaliacao)
print('Espaco usado = %s' % individuo1.espaco_usado)

print('\nIndividuo 2\n')
individuo2 = Individuo(espacos, valores, limite)
print('\nIndividuo numero 2 --> Teste\n')
for i in range(len(lista_produtos)):
    if individuo2.cromossomo[i] == '1':
        print('Nome: %s R$ %s ' % (lista_produtos[i].nome, lista_produtos[i].valor))
# Teste da função de avaliação
individuo2.avaliacao()  # Chamada da função
print('\nAvaliacao do Individuo 2\n')
print('Nota = %s' % individuo2.nota_avaliacao)
print('Espaco usado = %s' % individuo2.espaco_usado)

# Teste da função crossover
individuo1.crossover(individuo2)
