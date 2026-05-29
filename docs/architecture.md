# Arquitetura

## Decisao principal

O dataset da Instacart e estatico. Para demonstrar uma arquitetura proxima de producao sem inventar uma API externa, o projeto simula uma ingestao diaria incremental liberando subconjuntos de pedidos ja existentes.

## Camadas

### Raw

Contem os arquivos originais do Kaggle sem modificacao.

### Bronze

Contem os dados ingeridos em lotes simulados. Cada execucao registra metadados como data simulada, identificador do lote, quantidade de linhas e status.

### Silver

Contem tabelas limpas, tipadas e integradas:

- pedidos;
- usuarios;
- produtos;
- corredores;
- departamentos;
- itens de pedido.

### Gold

Contem tabelas analiticas e features:

- mart de pedidos;
- mart de produtos;
- mart de usuarios;
- mart de recompra;
- base de treino usuario-produto;
- tabelas agregadas para dashboard.

## Orquestracao

Prefect sera usado por ser simples, local e suficiente para portfolio. Airflow seria adequado para ambientes maiores com multiplos times, backfills complexos e operacao distribuida, mas adicionaria complexidade desnecessaria neste primeiro momento.

## SQL

DuckDB sera usado como mecanismo SQL gratuito e local. Ele permite consultar CSV/Parquet com otima performance e criar marts analiticos sem depender de infraestrutura paga.

## Idempotencia

Cada lote simulado tera chave de controle por `run_date` e intervalo de pedidos. Antes de escrever em bronze/silver/gold, o pipeline verificara se o lote ja foi processado e substituira ou ignorara a particao correspondente, evitando duplicidades.

