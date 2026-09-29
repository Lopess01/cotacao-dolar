import requests 
import csv
from datetime import datetime

resposta = requests.get("http://economia.awesomeapi.com.br/json/last/USD-BRL")
dados = resposta.json()["USDBRL"]

with open("historico_cotacao.csv", "a", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow([datetime.now(), dados["bid"], dados["ask"]])

print(f'salvo: {dados['bid']} / {dados["ask"]}')

# bid é a cotação de venda do dolar, 
# ou seja, se voce quiser vender dolares esse é o valor em reais

# ask, ou offer, é o valor que voce paga no dolares