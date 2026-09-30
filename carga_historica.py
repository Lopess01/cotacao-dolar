import requests
from databricks.connect import DatabricksSession
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, TimestampNTZType, DoubleType

# Mesmo fuso usado no cotacao.py: data_hora é gravada no horário de Brasília (sem fuso)
fuso_brasilia = timezone(timedelta(hours=-3))
TABELA = "cotacao_dolar"
DIAS = 360

load_dotenv()
API_KEY = os.environ.get("AWESOMEAPI_TOKEN")
spark = DatabricksSession.builder.serverless().profile("Renato").getOrCreate()

# 1. Busca o histórico diário dos últimos DIAS dias em uma única chamada
resposta = requests.get(
    f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{DIAS}",
    params={"token": API_KEY},
)
resposta.raise_for_status()
historico = resposta.json()

# 2/3. Converte cada item para (data_hora, bid, ask).
# "timestamp" vem como string em segundos desde epoch (UTC); convertemos para
# Brasília e tiramos o tzinfo para gravar como TIMESTAMP_NTZ, igual ao cotacao.py.
linhas = [
    (
        datetime.fromtimestamp(int(item["timestamp"]), fuso_brasilia).replace(tzinfo=None),
        float(item["bid"]),
        float(item["ask"]),
    )
    for item in historico
]

# Mesmo schema da tabela cotacao_dolar
schema = StructType([
    StructField("data_hora", TimestampNTZType()),
    StructField("bid", DoubleType()),
    StructField("ask", DoubleType()),
])

df = spark.createDataFrame(linhas, schema=schema).dropDuplicates(["data_hora"])

# 4. Evita duplicar: remove as linhas cujo data_hora já existe na tabela
if spark.catalog.tableExists(TABELA):
    existentes = spark.table(TABELA).select("data_hora")

    # Aviso se a tabela já tem registros dentro do período baixado
    inicio = min(l[0] for l in linhas)
    fim = max(l[0] for l in linhas)
    no_periodo = existentes.filter(F.col("data_hora").between(inicio, fim)).count()
    if no_periodo > 0:
        print(f"Aviso: a tabela já tem {no_periodo} registro(s) entre {inicio} e {fim}")

    df = df.join(existentes, on="data_hora", how="left_anti")

# 5. Insere e mostra quantas linhas entraram
inseridas = df.count()
if inseridas > 0:
    df.write.format("delta").mode("append").saveAsTable(TABELA)

print(f"Linhas inseridas na tabela Delta: {inseridas} (de {len(linhas)} recebidas da API)")
