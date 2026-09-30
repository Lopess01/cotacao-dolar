import requests
from databricks.connect import DatabricksSession
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from pyspark.sql.types import StructType, StructField, TimestampNTZType, DoubleType

fuso_brasilia = timezone(timedelta(hours=-3))
agora_brasilia = datetime.now(fuso_brasilia).replace(tzinfo=None)
load_dotenv()
API_KEY = os.environ.get("AWESOMEAPI_TOKEN")
spark = DatabricksSession.builder.serverless().profile("Renato").getOrCreate()

resposta = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
dados = resposta.json()["USDBRL"]

# TimestampNTZ guarda o horário "de parede", sem conversão para UTC
schema = StructType([
    StructField("data_hora", TimestampNTZType()),
    StructField("bid", DoubleType()),
    StructField("ask", DoubleType()),
])

df = spark.createDataFrame(
    [(agora_brasilia, float(dados["bid"]), float(dados["ask"]))],
    schema=schema,
)

df.write.format("delta").mode("append").saveAsTable("cotacao_dolar")

print(f"Salvo na tabela Delta: {dados['bid']} / {dados['ask']}")
