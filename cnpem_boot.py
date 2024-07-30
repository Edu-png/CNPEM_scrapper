# -*- coding: utf-8 -*-
"""CNPEM_boot

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VexwOXLiw1xP4undTFQC8UY7ZsKpCW5Y
"""

!pip install beautifulsoup4 pandas openpyxl requests

!sudo apt-get install ca-certificates

!pip install --upgrade python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

# URL da página a ser raspada
url = "https://pages.cnpem.br/trabalheconosco/vagas-abertas/"

# Desativar os avisos de verificação SSL (NÃO recomendado para ambientes de produção)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Definindo o user agent:

HEADERS = ({'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1) Gecko/20100101 Firefox/52.2', 'Accept-Language': 'pt-br, en;q=0.9,*;q=0.8'})

#Aqui colocamos também que a lingua preferível é o pt-br, podendo ser inglês em segundo caso.

# Desativar a verificação SSL (NÃO recomendado para ambientes de produção)
response = requests.get(url, verify=False, headers = HEADERS)

# Verificar se a solicitação foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontre todas as entradas de vagas na página
    vagas = soup.find_all('div', class_='post-entry-content')

    # Inicialize listas para armazenar os dados
    titulos = []
    datas = []
    resumos = []

    # Loop pelas vagas e extrair informações pela página 1 (única)
    for vaga in vagas:
        titulo = vaga.find('h3').text.strip()
        data = vaga.find('time', class_='entry-date updated').text.strip()
        resumo = vaga.find('div', class_='entry-excerpt').text.strip()

        titulos.append(titulo)
        datas.append(data)
        resumos.append(resumo)

    # Criar um DataFrame do pandas
    data_dict = {
        'Título da Vaga': titulos,
        'Data': datas,
        'Resumo': resumos
    }

    df = pd.DataFrame(data_dict)

    # Salvar os dados na planilha
    nome_arquivo = 'vagas_cnpem.xlsx'
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')

    print(f'Dados extraídos e salvos em "{nome_arquivo}" com sucesso!')
else:
    print("Falha ao acessar a página.")
