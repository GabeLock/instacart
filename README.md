# Instacart Market Basket Analysis

Projeto de portfolio de engenharia de dados e ciencia de dados usando o dataset historico **Instacart Market Basket Analysis**, publicado no Kaggle.

O objetivo e simular uma solucao real de dados para analisar pedidos de clientes ao longo do tempo e prever quais produtos um usuario tende a comprar novamente no proximo pedido.

> Importante: o dataset da Instacart e historico e estatico. A ingestao diaria deste projeto sera uma simulacao realista para fins de arquitetura e portfolio. Os pedidos existentes serao liberados progressivamente por um criterio tecnico controlado, como `order_number`, `days_since_prior_order` e uma data simulada de processamento. O projeto nao usa, nem inventa, uma API real da Instacart.

## Problema de negocio

Empresas de varejo precisam entender padroes de recompra, recorrencia de consumo e preferencias dos clientes para melhorar recomendacoes, reposicao de estoque, campanhas e experiencia de compra.

Este projeto responde perguntas como:

- quais produtos e departamentos sao mais recorrentes;
- como o comportamento muda por dia da semana e hora do dia;
- quais usuarios possuem maior tendencia de recompra;
- quais produtos recomendar para o proximo pedido de um usuario.

## Dataset

Dataset esperado:

- `aisles.csv`
- `departments.csv`
- `products.csv`
- `orders.csv`
- `order_products__prior.csv`
- `order_products__train.csv`
- `sample_submission.csv`

Origem: [Instacart Market Basket Analysis no Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis/data)

## Arquitetura resumida

O projeto usa uma arquitetura em camadas:

- `raw`: arquivos originais baixados do Kaggle, sem alteracao.
- `bronze`: cargas ingeridas e padronizadas, incluindo lotes diarios simulados.
- `silver`: dados limpos, tipados, validados e integrados.
- `gold`: tabelas analiticas, features, data marts e bases para dashboard/modelagem.

Fluxo planejado:

1. Download seguro dos arquivos via Kaggle API.
2. Simulacao de ingestao diaria incremental a partir do historico.
3. Validacao de schema, chaves e duplicidades.
4. Transformacoes SQL e Python para silver/gold.
5. Feature engineering para recompra.
6. Treinamento e comparacao de baseline, scikit-learn e modelo robusto.
7. Atualizacao do dashboard Streamlit a partir da camada gold.
8. Relatorio analitico complementar em R Markdown.

## Stack

- Python para ingestao, ETL, feature engineering, machine learning, orquestracao e Streamlit.
- R para EDA complementar e relatorio analitico.
- DuckDB como SQL gratuito/local para modelagem analitica e consultas.
- Prefect como orquestrador leve.
- Docker para execucao reprodutivel quando fizer sentido.
- Pytest para testes automatizados.

## Configuracao do Kaggle API

Voce precisa ter uma conta Kaggle e aceitar os termos da competicao/dataset.

Opcao 1: arquivo `kaggle.json`

1. Acesse sua conta Kaggle.
2. Va em `Account` > `API` > `Create New Token`.
3. Baixe o arquivo `kaggle.json`.
4. Salve em:
   - Windows: `C:\Users\<seu_usuario>\.kaggle\kaggle.json`
   - Linux/Mac: `~/.kaggle/kaggle.json`

Opcao 2: variaveis de ambiente

Copie `.env.example` para `.env` e preencha:

```bash
KAGGLE_USERNAME=seu_usuario
KAGGLE_KEY=sua_chave
```

Nunca versionar `.env`, `kaggle.json` ou dados pesados.

## Como rodar localmente

```bash
make setup
make download-data
make run-pipeline
make train-model
make dashboard
```

Comandos principais:

- `make setup`: cria ambiente e instala dependencias.
- `make download-data`: baixa o dataset para `data/raw`.
- `make run-pipeline`: executa pipeline diario simulado.
- `make train-model`: treina baseline e modelos preditivos.
- `make dashboard`: abre o dashboard Streamlit.
- `make test`: executa testes automatizados.

## Pipeline diario simulado

O pipeline aceitara parametros como:

```bash
python -m src.orchestration.pipeline --run-date 2026-01-01 --batch-size 5000
```

O lote sera registrado em metadados de processamento. Se o mesmo dia simulado for reprocessado, a carga deve ser idempotente e nao duplicar pedidos.

## Dashboard

O dashboard Streamlit sera executado com:

```bash
streamlit run src/dashboard/app.py
```

Ele exibira:

- visao geral dos pedidos;
- evolucao da ingestao simulada;
- produtos e departamentos mais comprados;
- produtos mais recomprados;
- comportamento por dia da semana e hora;
- perfil de recompra por usuario;
- previsao de proxima compra e recomendacoes;
- data/hora da ultima atualizacao do pipeline.

## Limitacoes

- A ingestao diaria e simulada porque o dataset e historico.
- O dataset nao contem eventos em tempo real, precos, promocoes ou estoque.
- A avaliacao preditiva depende da separacao temporal simulada e da estrutura `prior/train`.
- O projeto prioriza clareza e demonstracao de arquitetura, nao maxima performance em competicao Kaggle.

## Proximos passos

- Implementar download via Kaggle API.
- Criar simulador incremental idempotente.
- Construir transformacoes bronze, silver e gold.
- Adicionar validacoes e testes.
- Treinar modelos e publicar metricas.
- Criar dashboard Streamlit e relatorio em R.

