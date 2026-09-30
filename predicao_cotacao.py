# Databricks notebook source
df = spark.table("cotacao_dolar").orderBy("data_hora")
display(df)

# COMMAND ----------

import pandas as pd

pdf = df.select("data_hora", "bid").toPandas()
pdf = pdf.sort_values("data_hora").reset_index(drop=True)

pdf["bid_anterior"] = pdf["bid"].shift(1)

pdf = pdf.dropna()

pdf.head()

# COMMAND ----------

tamanho_treino = int(len(pdf) * 0.8)

treino = pdf.iloc[:tamanho_treino]
teste = pdf.iloc[tamanho_treino:]

print(f"Treino: {len(treino)} linhas | Teste: {len(teste)} linhas")

# COMMAND ----------

from sklearn.metrics import mean_absolute_error

# Baseline: "a previsão de hoje é o valor de ontem"
mae_baseline = mean_absolute_error(teste["bid"], teste["bid_anterior"])
print(f"MAE do baseline (persistência): {mae_baseline:.4f}")

# COMMAND ----------

from sklearn.linear_model import LinearRegression

X_treino = treino[["bid_anterior"]]
y_treino = treino["bid"]

X_teste = teste[["bid_anterior"]]
y_teste = teste["bid"]

modelo = LinearRegression()
modelo.fit(X_treino, y_treino)

previsoes = modelo.predict(X_teste)

mae_modelo = mean_absolute_error(y_teste, previsoes)
print(f"MAE do modelo: {mae_modelo:.4f}")