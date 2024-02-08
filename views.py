from django.shortcuts import render
from textblob import TextBlob
import os
import requests
from bs4 import BeautifulSoup

def index(request):
    return render(request, 'index.html')

def results(request):
    product_url = request.POST['product_url']

    # Extrair avaliações
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    avaliacoes = soup.find_all('div', class_='avaliacao')

    # Analisar sentimento
    sentimentos = [TextBlob(avaliacao.text).sentiment.polarity for avaliacao in avaliacoes]

    # Gerar resumo
    resumo = TextBlob('\n'.join(avaliacao.text for avaliacao in avaliacoes)).sentiment.polarity

    # Calcular índices
    positividade = sentimentos.count('positivo')
    negatividade = sentimentos.count('negativo')
    neutralidade = sentimentos.count('neutro')
    total_avaliacoes = len(avaliacoes)
    indice_positividade = positividade / total_avaliacoes
    indice_negatividade = negatividade / total_avaliacoes
    indice_neutralidade = neutralidade / total_avaliacoes

    # Pontos positivos e negativos
    pontos_positivos = []
    pontos_negativos = []
    for avaliacao, sentimento in zip(avaliacoes, sentimentos):
        if sentimento > 0:
            pontos_positivos.append(avaliacao.text)
        elif sentimento < 0:
            pontos_negativos.append(avaliacao.text)

    # Contexto para a página de resultados
    contexto = {
        'summary': {
            'title': 'Resumo de Avaliações',
            'summary': resumo,
            'positive_points': pontos_positivos,
            'negative_points': pontos_negativos,
            'positivity_index': indice_positividade,
            'negativity_index': indice_negatividade,
            'neutrality_index': indice_neutralidade,
        }
    }

    return render(request, 'results.html', contexto)
