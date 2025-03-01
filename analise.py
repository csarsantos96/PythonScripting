
import csv
import json
import os
import time
from datetime import datetime
from sys import argv
from random import random

import requests
import pandas as pd
import seaborn as sns


def extract_data():
    """Extrai a taxa CDI do site do BCB e salva os dados em 'taxa-cdi.csv'."""
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        cdi = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        # O site retorna uma lista de dicionários, pegamos o valor da última entrada
        data_json = json.loads(response.text)
        dado = data_json[-1]['valor']
        # Criando as variáveis de data e hora
        data_e_hora = datetime.now()
        data_str = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora_str = datetime.strftime(data_e_hora, '%H:%M:%S')
        # Ajustando a taxa com um fator aleatório
        cdi = float(dado) + (random() - 0.5)

    # Verifica se o arquivo CSV existe; caso não, cria e escreve o cabeçalho
    csv_file = './taxa-cdi.csv'
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', encoding='utf8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(['data', 'hora', 'taxa'])

    # Adiciona os dados extraídos ao arquivo CSV
    with open(csv_file, mode='a', encoding='utf8', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow([data_str, hora_str, cdi])

    print("Extração concluída. Dados salvos em 'taxa-cdi.csv'.")


def create_graph(graph_name):
    """Cria um gráfico da taxa CDI a partir dos dados em 'taxa-cdi.csv' e salva em um arquivo PNG."""
    # Carrega os dados do arquivo CSV
    df = pd.read_csv('./taxa-cdi.csv')
    # Cria o gráfico utilizando o seaborn
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    grafico.set_xticklabels(labels=df['hora'], rotation=90)
    # Salva o gráfico no arquivo PNG com o nome passado como parâmetro
    grafico.get_figure().savefig(f"{graph_name}.png")
    print(f"Gráfico salvo como '{graph_name}.png'.")


def main():
    if len(argv) < 2:
        print("Uso: python analise.py <nome-do-grafico>")
        return

    graph_name = argv[1]

    extract_data()
    create_graph(graph_name)
    print("Análise concluída com sucesso.")


if __name__ == '__main__':
    main()
