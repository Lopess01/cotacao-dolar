# 💱 Pipeline de Cotação USD-BRL

Pipeline de dados end-to-end que coleta, armazena e analisa a cotação 
do dólar em tempo real, usando Python, Databricks e Delta Lake.

## O que o projeto faz

- **Coleta em tempo real**: busca a cotação atual USD-BRL via API pública
  (AwesomeAPI) a cada hora
- **Carga histórica**: popula a base com mais de 360 dias de dados
  históricos em uma única execução
- **Armazenamento**: grava os dados em uma tabela Delta Lake no Databricks
- **Automação**: um Job agendado no Databricks mantém a tabela atualizada
  automaticamente, sem intervenção manual
- **Modelagem preditiva**: testa um modelo simples de regressão linear
  para prever a cotação do dia seguinte

## Arquitetura:
    API (AwesomeAPI) → Python (requests) → PySpark → Delta Table → View formatada
    ↓
    Modelo de ML (scikit-learn)


## Tecnologias usadas

- **Python** (requests, python-dotenv, scikit-learn, pandas)
- **Apache Spark / PySpark** (via Databricks Connect)
- **Databricks** (Serverless Compute, Jobs, Secrets, Delta Lake)
- **SQL** (view formatada de exibição)
- **Git/GitHub** (versionamento)

## Estrutura do projeto:
    cotacao-dolar/
    ├── cotacao.py # Script de coleta em tempo real
    ├── carga_historica.py # Carga inicial de dados históricos (360 dias)
    ├── predicao_cotacao.py # Modelo preditivo (regressão linear)
    ├── databricks.yml # Configuração do bundle Databricks
    ├── pyproject.toml # Dependências do projeto
    └── README.md

## Segurança

A chave de API é armazenada como **Databricks Secret** (não exposta no 
código) e como variável de ambiente local via `.env` (excluído do 
repositório pelo `.gitignore`).

## Modelagem preditiva

Foi testado um modelo de regressão linear simples para prever a cotação 
do dia seguinte com base no valor do dia anterior, comparado a um 
baseline de persistência ("a cotação de amanhã será igual à de hoje").

**Resultados:**
| Modelo | MAE |
|---|---|
| Baseline (persistência) | 0.0203 |
| Regressão linear | 0.0200 |

O modelo superou o baseline por margem pequena — resultado esperado, já 
que séries de câmbio se aproximam de um comportamento de **random walk**, 
onde o valor mais recente já é o melhor preditor disponível. Isso reflete 
uma característica conhecida de mercados financeiros eficientes, não uma 
limitação do modelo em si.

## Próximos passos

- [ ] Testar features adicionais (média móvel, volatilidade)
- [ ] Adicionar coluna de origem do dado (histórico vs. tempo real)
- [ ] Dashboard de visualização da série temporal

## Autor

Renato Lopes — [GitHub](https://github.com/Lopess01)