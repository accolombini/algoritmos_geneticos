# Title     : Algoritmo Genético Completo -> versão final -> para quantidade de cada produto = 1
# Objective : Neste laboratório vamos adicionar mais funcionalidades para realizar as funções de AG de forma generalizada -> podendo ser replicado para casos reais com as devidas alterações que se fizerem necessário
# Created by: accol
# Created on: 11/06/2020


# Neste laboratório faremos o ciclo completo -> gerar população inicial -> avaliar população -> selecionar os pais -> crossover -> mutação -> avaliar a população -> definir a população sobrevivente
# Criaremos uma nova função chamada resolver -> esta função terá como parâmetros => algoritmoGenetico, taxaMutacao, numeroGeracoes, espacos, valores e limiteEspaco
# Este laboratório será muito repetitivo, pois estaremos simplesmente reaproveitando o código já estudado e organizando para que seja genérico

# Estaremos reaproveitando o código desenvolvido no laboratório anterior

setClass(
  'Produto',
  slots = c(
    nome = 'character',
    espaco = 'numeric',
    valor = 'numeric'
  )
)

# Criando a classe Indivíduo => espacos -> representa o espaço a ser utilizado no caminhão; valores -> representa o somatório dos valores dos produtos selecionados; limiteEspecos -> representará a capacidade do meio de transporte utilizado (inicialmente a capacidade do caminhão é de 3 metros cúbicos); notaAvaliacao -> será a nota atribuída à solução do indivíiduo (quanto melhor a proposta de solução melhor a nota); geracao -> aramazenará a geração do indivíduo (acompanhando o processo de evolução); cromossomo -> é aqui que teremos nossa sequência de zeros e uns (14 um bit para cada produto) a ser utilizado para definir a mercadoria que será levada e a mercadoria que será deixada (0 -> mercadoria fica 1 -> mercadoria transportada)

setClass(
'Individuo',
  slots = c(
    espacos = 'numeric',
    valores = 'numeric',
    limiteEspacos = 'numeric',
    notaAvaliacao = 'numeric',
    espacoUsado = 'numeric',
    geracao = 'numeric',
    cromossomo = 'character'
  ),
     # Aqui faremos a inicialização das variáveis -> o cromossomo será inicializado por meio de uma função
     prototype = list(
          espacos = 0,
          valores = 0,
          limiteEspacos = 0,
          notaAvaliacao = 0,
          espacoUsado = 0,
          geracao = 0
     )
)

# Vamos criar uma funçao para gerar um primeiro cromossomo de forma aleatória -> garantindo assim maior rigor no tratamento do AG -> o parâmetro tamanhoCromossomo definirá a quantidade de rpodutos, no caso, estamos trabalhando com 14, mas queremos que nosso algoritmo seja o mais gerérico possível. Usaremos a função sample() do R que irá gerar para nós uma sequência randômica de valores (0 e 1) para compor nosso cromossomo, replace = TRUE garante a reposição do valor sorteado e apossibilidade de sorteá-lo novamente num evento próximo -> acompanhe

gerarCromossomo = function (tamanhoCromossomo){
  cromossomo = sample(x = c('0', '1'), size = tamanhoCromossomo, replace = TRUE)
  return(cromossomo)
}

# Vamos criar a função de avaliação. Nesta função vamos fazer o somatório do espaço e o somatório do valor da carga selecionada para o frete. Observer que estamos usando o termo nota ao invés de soma que é vocabulário comum em GA

avaliacao = function (individuo){
  nota = 0
  somaEspacos = 0
  for (i in 1:length(individuo@cromossomo)){
    if (individuo@cromossomo[i] == '1'){
      nota = nota + individuo@valores[i]
      somaEspacos = somaEspacos + individuo@espacos[i]
    }
  }
  # Neste if iremos rebaixar a nota de um individuo para 1 no caso dele estourar o limite de capaciade do caminhão. A nota 1 é uma boa dica para AG
  if(somaEspacos > individuo@limiteEspacos){
    nota = 1
  }
  # A seguir precisamos escrever esses valores nos atributos da Classe Individuo
  individuo@notaAvaliacao = nota
  individuo@espacoUsado = somaEspacos
  # Precisamos do comando return para retornar o objeto -> caso contrário teríamos apenas uma solução local
  return(individuo)
}

# Vamos agora fazer a implementação da função de CROSSOVER

crossover = function(individuoA, individuoB) {
  # Criaremos uma variável que será nossa referência para encontrarmos o ponto de corte do cromosso dos pais. Como o ponto de corte será o mesmo para os dois indivíduos poderemos usar individuoA ou individuoB

  indices = 1:length(individuoA@cromossomo)
  # Usaremos a função randomica sample() para gerar o ponto de corte

  corte = sample(indices, 1)
#  cat('\nA variável corte é: ', corte) -> use para verificar seus resultados
  # Precisamos garantir que o ponto de corte não seja o tamanho do próprio cromossomo -> isso inviabilizaria o crossover. Embora não seja um resultado interessante é possível que aconteça e o algoritmos precisa estar preparado para lidar com essa situação

      if (corte == length(individuoA@cromossomo)) {
    filho1 = individuoB@cromossomo[1:corte]
    filho2 = individuoA@cromossomo[1:corte]
  } else {
    filho1 = c(individuoB@cromossomo[1:corte], individuoA@cromossomo[(corte + 1):length(individuoA@cromossomo)])
    filho2 = c(individuoA@cromossomo[1:corte], individuoB@cromossomo[(corte + 1):length((individuoB@cromossomo))])
  }
  # Note que filho1 e filho2 ainda não são objetos do tipo indivíduo, são apenas variáveis utilizadas para realizar a operação do crossover. Vamos a seguir resolver esse problema acompanhe

  filhos = list(
    new("Individuo", espacos = individuoA@espacos, valores = individuoA@valores,
        limiteEspacos = individuoA@limiteEspacos, geracao = individuoA@geracao + 1),
    new("Individuo", espacos = individuoB@espacos, valores = individuoB@valores,
        limiteEspacos = individuoB@limiteEspacos, geracao = individuoB@geracao + 1)
  )

  filhos[[1]]@cromossomo = filho1
  filhos[[2]]@cromossomo = filho2
  return(filhos)
}

# Vamos agora construir nosso segundo operador Genético a MUTAÇÃO

mutacao = function(individuo, taxaMutacao) {
  for (i in 1:length(individuo@cromossomo)) {
    # Usaremos a função runif() para a geração do número aleatório => observe o teste para verificar se teremos ou não mutação
   if (runif(n = 1, min = 0, max = 1) < taxaMutacao) {
      if (individuo@cromossomo[i] == '1') {
        individuo@cromossomo[i] = '0'
      } else {
        individuo@cromossomo[i] = '1'
      }
    }
  }
  return(individuo)
}

# Criaremos uma nova classe que deverá conter a solução do nosso problema. Em outras palavras, o objetivo dessa classe é encontrar a melhor solução para nosso problema

setClass(
'algoritmoGenetico',
      slots = c(
      tamanhoPopulacao = 'numeric',
      populacao = 'list',
      geracao = 'numeric',
      melhorSolucao = 'Individuo'
      )
)

# Vamos agora criar uma função que deverá inicializar nossa população

inicializaPopulacao = function (algoritmoGenetico, espacos, valores, limite){
  for (i in 1:algoritmoGenetico@tamanhoPopulacao){
    algoritmoGenetico@populacao[[i]] = new('Individuo', espacos = espacos, valores = valores, limiteEspacos = limite)
    algoritmoGenetico@populacao[[i]]@cromossomo = gerarCromossomo(length(espacos))
  }
  return(algoritmoGenetico)
}

# Criaremos agora uma função para ordenar de forma decrescente os indivíduos da população, com base na sua nota => usarmos a função order() com o parâmetro decreasing setado como TRUE do R que realiza essa operação de forma simples e direta

ordenaPopulacao = function (populacao){
  populacaoOrdenada = c()
  notasAvaliacao = c()
  # Precisamos agora percorrer toda população -> usaremos um comando for => acompanhe
  for (individuo in populacao){
    notasAvaliacao = c(notasAvaliacao, individuo@notaAvaliacao)
  }
  listaPosicao = order(notasAvaliacao, decreasing = TRUE)
  # Vamos agora realizar um novo for preenchendo nossa lista ordenada
  for (i in 1:length(listaPosicao)){
    populacaoOrdenada = c(populacaoOrdenada, populacao[[listaPosicao[i]]])
  }
  return(populacaoOrdenada)
}

# Criaremos agora a função que nos permitirá trabalhar com o indivíduo mais apto

melhorIndividuo = function(algoritmoGenetico, individuo){
  if (individuo@notaAvaliacao > algoritmoGenetico@melhorSolucao@notaAvaliacao){
    algoritmoGenetico@melhorSolucao = individuo
  }
  return(algoritmoGenetico)
}

# Criaremos agora a função somaAvaliacoes

somaAvaliacoes = function (algoritmoGenetico){
  soma = 0
  for (individuo in algoritmoGenetico@populacao){
    soma = soma + individuo@notaAvaliacao
  }
  return(soma)
}

# Aqui iniciamos nosso processo para implementarmos o método da Roleta Viciada => para esse método precisaremos utilizar o somaAvaliacoes para parametrizar a distribuição de proporção para os indivíduos -> acompanhe
# Vamos criar uma função para a seleção do pai => usaremos a função runif() (aceita 3 parâmetros quantidade de valores a serem gerados, valor mínimo e valor máximo) para a geração do número aleatório (roda a roleta) e criaremos uma variável chamada pai que será um índice para percorrer a população indicando qual é o indivíduo que será selecionado

selecionaPai = function (algoritmoGenetico, somaAvaliacoes){
  pai = 0
  valorSorteado = runif(1, 0,1) * somaAvaliacoes
  soma = 0
  i = 1
  while (i < length(algoritmoGenetico@populacao) && soma < valorSorteado){
    soma = soma + algoritmoGenetico@populacao[[i]]@notaAvaliacao
    pai = pai + 1
    i = i + 1
  }
  return(pai)
}

# Vamos agora criar a função que deverá exibir a geração

visualizaGeracao = function (algoritmoGenetico){
  melhor = algoritmoGenetico@populacao[[1]]
  cat('\nGeração: ', melhor@geracao, '\nValor: R$', melhor@notaAvaliacao, '\nEspaço: ', melhor@espacoUsado, '\nCromossomo: ', melhor@cromossomo)
}

# Criaremos agora a função resolver que deverá generlizar o processo do AG => acompanhe

resolver = function (algoritmoGenetico, taxaMutacao, numeroGeracao, espacos, valores, limiteEspaco){
  ag = algoritmoGenetico
  # Precisamos agora inicializar a população => cria os 20 indivíduos
  ag = inicializaPopulacao(algoritmoGenetico = ag, espacos = espacos, valores = valores, limite = limiteEspaco)
  # Feito isso precisamos agora avaliar essa população
  for (i in 1:ag@tamanhoPopulacao){
    ag@populacao[[i]] = avaliacao(ag@populacao[[i]])
  }
  # Precisamos ordenar a população
  ag@populacao = ordenaPopulacao(ag@populacao)
  # Podemos agora pegar a melhor solução => observe que já podemos pegar o primeiro elemento (população já ordenada)
  ag@melhorSolucao = ag@populacao[[1]]
  # Para visualizar vamos usar a função desenvolvida no laboratório anterior
  visualizaGeracao(algoritmoGenetico = ag)

  # Até aqui => temos a primeira parte do AG. Precisamos agora executar o algoritmo levando em consideração o número de gerações definidas para seu projeto
  for (geracao in 1:numeroGeracao){
    soma = somaAvaliacoes(algoritmoGenetico = ag)
    novaPopulacao = c()
    for (individuosGerados in 1:(ag@tamanhoPopulacao / 2)){
      pai1 = selecionaPai(algoritmoGenetico = ag, somaAvaliacoes = soma)
      pai2 = selecionaPai(algoritmoGenetico = ag, somaAvaliacoes = soma)

      # Definidos os pais => precisamos agora gerar os filhos
      filhos = crossover(individuoA = ag@populacao[[pai1]], individuoB = ag@populacao[[pai2]])

      # Agora precisamos inserir na nova população estes novos indivíduos
      novaPopulacao = c(novaPopulacao, mutacao(individuo = filhos[[1]], taxaMutacao = taxaMutacao))
      novaPopulacao = c(novaPopulacao, mutacao(individuo = filhos[[2]], taxaMutacao = taxaMutacao))
      # Ao terminar essa executção teremos os novos individuos componentes da nova geração
    }
    # Agora vamos descartar ou melhor sobrecresver a geração antiga
    ag@populacao = novaPopulacao

    # Sobrescrito precisamos fazer novamente a avaliação => note que o fato de estarmos numa nova geração não significa que já encontramos a melhor solução
    for (i in 1:ag@tamanhoPopulacao){
    ag@populacao[[i]] = avaliacao(ag@populacao[[i]])
  }
    # Precisamos agora ordenar a nova populacao
    ag@populacao = ordenaPopulacao(ag@populacao)

    # Novamente precisamos visualizar a populacao -> o melhor de cada geração será visualizado aqui
    visualizaGeracao(algoritmoGenetico = ag)

    # Agora vamos capturar o melhor indivíduo -> lembrando que a população precisa estar ordenada

    ag = melhorIndividuo(algoritmoGenetico = ag, individuo = ag@populacao[[1]])

    # Aqui terminamos o for que realizará as ações já estudadas em todas as Gerações do seu projeto
  }
  # Por último vamos fazer um cat() para exibir a melhor solução => queremos agora exibir o melhor de todas as gerações => observe que este não está ordenado
  cat('\nMelhor solução -> G: ', ag@melhorSolucao@geracao, '\nValor: R$', ag@melhorSolucao@notaAvaliacao, '\nEspaço: ', ag@melhorSolucao@espacoUsado, '\nCromossomo: ', ag@melhorSolucao@cromossomo)

  return(ag)
}

# Devemos agora popular nossa classe -> lembre-se são quatorze produtos => façamos o primeiro para teste

# Como são muitos produtos, vamos melhorar essa entrada de dados e gerar uma lista de produtos

listaProdutos = c(new('Produto', nome = 'Geladeira Dako', espaco = 0.751, valor = 999.90),
                  new("Produto", nome = "Iphone 6", espaco = 0.0000899, valor = 2911.12),
                  new("Produto", nome = "TV 55' ", espaco = 0.400, valor = 4346.99),
                  new("Produto", nome = "TV 50' ", espaco = 0.290, valor = 3999.90),
                  new("Produto", nome = "TV 42' ", espaco = 0.200, valor = 2999.00),
                  new("Produto", nome = "Notebook Dell", espaco = 0.00350, valor = 2499.90),
                  new("Produto", nome = "Ventilador Panasonic", espaco = 0.496, valor = 199.90),
                  new("Produto", nome = "Microondas Electrolux", espaco = 0.0424, valor = 308.66),
                  new("Produto", nome = "Microondas LG", espaco = 0.0544, valor = 429.90),
                  new("Produto", nome = "Microondas Panasonic", espaco = 0.0319, valor = 299.29),
                  new("Produto", nome = "Geladeira Brastemp", espaco = 0.635, valor = 849.00),
                  new("Produto", nome = "Geladeira Consul", espaco = 0.870, valor = 1199.89),
                  new("Produto", nome = "Notebook Lenovo", espaco = 0.498, valor = 1999.90),
                  new("Produto", nome = "Notebook Asus", espaco = 0.527, valor = 3999.00)
                  )

# Definida a classe Individuos -> vamos agora construir uma maneira de testar e visualizar a proposta apontada para solução incial do problema. Criaremos as seguintes variáves: espaço do tipo lista -> receberá os espaços; valores do tipo lista -> receberá os valores dos produtos e nomes do tipo lista -> conterá os nomes dos produtos. Observe que as variáveis criadas representam exatamente cada um dos atributos do nosso ojeto Produtos

espacos = c()
valores = c()
nomes = c()

# Vamos agora criar um for para percorrer o objeto e carregar as variáeis criadas

for (produto in listaProdutos){
  espacos = c(espacos, produto@espaco)
  valores = c(valores, produto@valor)
  nomes = c(nomes, produto@nome)
}
# Vamos definir o limite de transporte
limite = 3

# Agora criaremos o nosso cenário de testes para nossa população
tamanho = 20

# Aqui preparamos a versão final de nosso AG => Traremos para cá a variável probabilidade de Mutação e criaremos a variável numero de gerações
probabilidadeMutacao = 0.05
numeroGeracoes = 100
# Vamos criar o nosso algoritmo genético usando a codificação já conhecida nossa
ag = new('algoritmoGenetico', tamanhoPopulacao = tamanho)

# A partir daqui estaremos criando condições para teste do nosso AG

ag = resolver(algoritmoGenetico = ag, taxaMutacao = probabilidadeMutacao, numeroGeracao = numeroGeracoes, espacos = espacos, valores = valores, limiteEspaco = limite)

# Vamos agora fazer um for para listarmos qual a lista de produtos a ser transportada neste frete

for (i in 1:length(listaProdutos)){
  if (ag@melhorSolucao@cromossomo[i] == '1'){
    cat('\nNome produto: ', nomes[i], 'R$: ', valores[i])
  }
}

# A partir daqui você deverá simular um grande número de vezes na tentativa de encontrar a melhor solução. Você poderá aumentar o número de gerações, enfim, você deverá adaptar seu algoritmos ao seu projeto na busca da melhor solução
# Observe que até aqui estamos considerando a quantidade de produtos igual a unidade, isso, com certeza não será um caso real, assim precisamos evoluir mais um nível nosso AG
