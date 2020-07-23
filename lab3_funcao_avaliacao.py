# Title     : Função de Avaliação
# Objective : Neste laboratório vamos construir a função de avaliação do nosso indivíduo utilizando R => Queremos avaliar o quão boa é nossa solução -> inicialmente um indíviduo
# Created by: accol
# Created on: 11/06/2020


# A função de avaliação é mais um conceito importante de GA e compreende o que segue:
# 1- Função de avaliação (fitness) -> em palavras queremos saber o  quanto o indivíduo está se encaixando na solução do problema
# 2- Medida de qualidade para saber como o cromossomo resolve o problema
# 3- Se é uma solução aceitável e se pode ser utilizada para a evolução. Aqui cuidado, zerar indivíduos menos aptos pode ser a melhor forma para se chegar a solução ótima, lembre-se que termos que evoluir por gerações e as diferenças poderão resultar em indivíduos mais aptos

# Neste laboratório estaremos criando uma função que avalia (funçao avaliação) o valor da nota (quanto mais alto melhor) e o espaço utilizado pela carga (quanto mais próximo ao limite do transporte melhor) no nosso caso estamos trabalhando com uma caminhão de 3 metros cúbicos
# Precisaremos na classe Individuo criar um novo atributo que será o somatório do espaço utilizado e em seguida devemos iniciar essa variável com 0

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
#    for produto in lista_produtos: # So para testes
#        print(produto.nome)
# Vamos criar listas para =>> espacos; valores e nomes (uma para cada atributo da classe produto)
    espacos = []
    valores = []
    nomes = []
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3  # Representa a capacidade máxima de transporte do caminhão 3 metros cubicos
    individuo1 = Individuo(espacos, valores, limite)
    print('Espacos = %s' %str(individuo1.espacos))
    print('Valores = %s' %str(individuo1.valores))
    print('Cromossomo = %s' %str(individuo1.cromossomo))

    # Vamos exibir os produtos selecionados para esta carga
    print('\nComponentes da Carga\n')
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == '1':
            print('Nome: %s R$ %s ' % (lista_produtos[i].nome, lista_produtos[i].valor))

# Teste da função de avaliação
individuo1.avaliacao()  # Chamada da função
print('\nAvaliacao do Individuo\n')
print('Nota = %s' % individuo1.nota_avaliacao)
print('Espaco usado = %s' % individuo1.espaco_usado)
