import requests 
import csv
from datetime import datetime
import os

pasta_projeto = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(pasta_projeto, "historico_cotacao.csv")

resposta = requests.get("http://economia.awesomeapi.com.br/json/last/USD-BRL")
dados = resposta.json()["USDBRL"]

with open(caminho_csv, "a", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow([datetime.now(), dados["bid"], dados["ask"]])

print(f'salvo: {dados['bid']} / {dados["ask"]}')

# bid é a cotação de venda do dolar, ou seja, se voce quiser vender dolares esse é o valor em reais
# ask, ou offer, é o valor que voce paga no dolar