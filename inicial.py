import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

# Função para extrair avaliações de um site
def extrair_avaliacoes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    avaliacoes = soup.find_all('div', class_='avaliacao') # substitua 'div' e 'avaliacao' pelos seletores corretos do site
    return avaliacoes

# Função para analisar o sentimento de uma avaliação
def analisar_sentimento(avaliacao):
    blob = TextBlob(avaliacao)
    sentimento = blob.sentiment.polarity
    if sentimento > 0:
        return 'positivo'
    elif sentimento < 0:
        return 'negativo'
    else:
        return 'neutro'

# Função para gerar um resumo conciso das avaliações
def gerar_resumo(avaliacoes):
    resumo = '\n'.join(avaliacao.text for avaliacao in avaliacoes)
    return resumo

# Função para calcular os índices de positividade, negatividade e neutralidade das avaliações
def calcular_indices(avaliacoes, sentimentos):
    total_avaliacoes = len(avaliacoes)
    positividade = sentimentos.count('positivo')
    negatividade = sentimentos.count('negativo')
    neutralidade = sentimentos.count('neutro')
    indice_positividade = positividade / total_avaliacoes
    indice_negatividade = negatividade / total_avaliacoes
    indice_neutralidade = neutralidade / total_avaliacoes
    return indice_positividade, indice_negatividade, indice_neutralidade

# Função para apresentar os resultados em uma interface amigável
def apresentar_resultados(resumo, pontos_positivos, pontos_negativos, indice_positividade, indice_negatividade, indice_neutralidade):
    print('Resumo das avaliações:')
    print(resumo)
    print('Pontos positivos:')
    for ponto in pontos_positivos:
        print('- ' + ponto)
    print('Pontos negativos:')
    for ponto in pontos_negativos:
        print('- ' + ponto)
    print('Índice de positividade:', indice_positividade)
    print('Índice de negatividade:', indice_negatividade)
    print('Índice de neutralidade:', indice_neutralidade)

# Exemplo de uso
url = 'https://www.exemplo.com/produto'
avaliacoes = extrair_avaliacoes(url)
sentimentos = [analisar_sentimento(avaliacao) for avaliacao in avaliacoes]
resumo = gerar_resumo(avaliacoes)
pontos_positivos = ['Ótima qualidade', 'Entrega rápida']
pontos_negativos = ['Preço alto', 'Tamanho incorreto']
indice_positividade, indice_negatividade, indice_neutralidade = calcular_indices(avaliacoes, sentimentos)
apresentar_resultados(resumo, pontos_positivos, pontos_negativos, indice_positividade, indice_negatividade, indice_neutralidade)