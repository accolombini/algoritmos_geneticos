# Title     : Algoritmo Genético Completo -> USANDO BIBLIOTECA EPECÍFICA DO R CHAMADA GA
# Objective : Neste laboratório vamos aprimorar nosso GA empregando a biblioteca GA da linguagem R
# Created by: accol
# Created on: 11/06/2020


# Neste laboratório faremos o ciclo completo -> gerar população inicial -> avaliar população -> selecionar os pais -> crossover -> mutação -> avaliar a população -> definir a população sobrevivente

# Para este laboratório precisaremos de uma biblioteca nova 'GA'

# Está pronto para respirar aliviado => veja como ficou muito simples o nosso trabalho utilizando essa biblioteca

library(GA)

setClass (
  "Produto",
  slots = c(
    nome = "character",
    espaco = "numeric",
    valor = "numeric"
  )
)

library(RMySQL)

conexao = dbConnect(MySQL(), user = "root", password = "1234", dbname = "produtos", host = "localhost")
dataFrameProdutos = dbGetQuery(conexao, "select nome, espaco, valor, quantidade from produtos")
dbDisconnect(conexao)

listaProdutos = c()

for (i in 1:nrow(dataFrameProdutos)) {
  #print(dataFrameProdutos["nome"])
  for (j in 1:dataFrameProdutos[i, 4]) {
    listaProdutos = c(listaProdutos, new("Produto", nome = dataFrameProdutos[i, 1],
                                         espaco = dataFrameProdutos[i, 2],
                                         valor = dataFrameProdutos[i, 3]))
  }
}

espacos = c()
valores = c()
nomes = c()
for (produto in listaProdutos) {
  espacos = c(espacos, produto@espaco)
  valores = c(valores, produto@valor)
  nomes = c(nomes, produto@nome)
}
limite = 10

# Para fortalecer nosso algoritmo vamos implementar a função de avaliação, pois esta não está presente na biblioteca por N razões => o restante faremos por meio dos recursos disponíveis na biblioteca

avaliacao = function(cromossomo) {
  nota = 0
  somaEspaco = 0
  for (i in 1:length(cromossomo)) {
    if (cromossomo[i] == '1') {
      nota = nota + valores[i]
      somaEspaco = somaEspaco + espacos[i]
    }
  }
  if (somaEspaco > limite) {
    nota = 1
  }
  return(nota)
}

# algoritmo@bestSol -> local de armazenamento da melhor solução => keepBest = TRUE -> Consulte a referência da biblioteca para maiores informações

# Praticamente tudo o que foi desenvolvido nos laboratórios anteriores se enontra na próxima linha de código, observe que o processo será feito de forma automática, basta que você parametrize adequadamente
# nBits -> indica a quantidade de genes que seu projeto demanda (neste caso são 47)
# gabin_Population -> gera uma população randômica para ser usada em algoritmo genético
# gabin_rwSelection -> faz a seleção do indivíduo => equivale ao algoritmo da Roleta Viciada
# gabin_spCrossover -> define como será a operação de crossover => neste caso define que será através de um único ponto de corte
# gabin_raMutation -> equivale ao algoritmo criado onde se for '0' vira '1' e vice versa
# popSize -> o tamanho da populaçào
# pcrossover -> define o probabilidade de ocorrência de crossover (no caso 80%) diferente de nosso algoritmos que trabalhava com 100%
# pmutation -> define a probabilidade de ocorrência de mutação
# elitism -> define o número de melhores indivíduos aptos que irão sobreviver em cada geração
# maxiter -> define o número de gerações (estamos trabalhando com 100)
# keepBest -> quando setado em TRUE guarda salva as melhores soluções de cada uma das gerações
# seed -> semente apenas para garantir que consigamos obter sempre o mesmo resutado

algoritmo = ga(type = "binary", fitness = avaliacao, nBits = length(listaProdutos),
               population = gabin_Population, selection = gabin_rwSelection,
               crossover = gabin_spCrossover, mutation = gabin_raMutation, popSize = 20,
               pcrossover = 0.8, pmutation = 0.05, elitism = 0.05, maxiter = 100,
               keepBest = TRUE, seed = 20)

# Podemos visualizar um sumário do algoritmo -> os parâmetros e resultados alcançados
summary(algoritmo)

# Observe como ficou fácil plotar um gráfico
plot(algoritmo)

# Para visualizarmos quais produtos serão carregados neste frete => use o for a seguir
cat("\n\n$$$$ Lista de Produtos a ser transportada neste frete $$$$\n")
for (i in 1:length(listaProdutos)) {
  if (algoritmo@solution[i] == '1') {
    cat("\n Nome: ", nomes[i], " R$: ", valores[i])
  }
}
