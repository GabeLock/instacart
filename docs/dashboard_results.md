# Resultados do Dashboard Streamlit

Esta pagina documenta os resultados apresentados na primeira versao executavel do dashboard Streamlit.

## Status atual

- Aplicacao: `src/dashboard/app.py`
- URL local usada no teste: `http://127.0.0.1:8501`
- Modo atual: demonstracao
- Objetivo: permitir visualizacao do produto analitico antes da ingestao real via Kaggle API
- Evolucao recente: dashboard interativo com afinidade de produtos, grupos de compra, analise por horario e tabela dinamica

O dashboard foi construido para tentar carregar arquivos Parquet da camada `data/gold`. Quando os marts ainda nao existem, ele usa uma base demonstrativa deterministica, sem inventar dados reais da Instacart.

## KPIs apresentados

| Indicador | Valor |
| --- | ---: |
| Pedidos ingeridos | 59.700 |
| Itens ingeridos | 238.800 |
| Tamanho medio da cesta | 4,00 |
| Ultima atualizacao simulada | 10/01/2026 |

## Evolucao da ingestao simulada

| Data simulada | Pedidos ingeridos | Itens ingeridos |
| --- | ---: | ---: |
| 2026-01-01 | 4.200 | 16.500 |
| 2026-01-02 | 4.600 | 18.100 |
| 2026-01-03 | 5.100 | 20.300 |
| 2026-01-04 | 5.300 | 21.700 |
| 2026-01-05 | 5.700 | 22.900 |
| 2026-01-06 | 6.100 | 24.400 |
| 2026-01-07 | 6.400 | 26.000 |
| 2026-01-08 | 6.900 | 27.900 |
| 2026-01-09 | 7.100 | 29.100 |
| 2026-01-10 | 7.600 | 30.600 |

## Produtos mais comprados

| Produto | Pedidos | Taxa de recompra |
| --- | ---: | ---: |
| Banana | 1.872 | 72% |
| Bag of Organic Bananas | 1.540 | 69% |
| Organic Strawberries | 1.221 | 61% |
| Organic Baby Spinach | 1.130 | 58% |
| Organic Hass Avocado | 1.018 | 63% |
| Large Lemon | 965 | 42% |
| Organic Raspberries | 842 | 55% |
| Organic Whole Milk | 788 | 67% |

## Afinidade de produtos

O usuario pode escolher um produto no filtro lateral e responder perguntas como:

- quem compra `Banana` tambem tem tendencia de comprar qual item;
- quais sao os dois produtos com maior chance de combinar com o item escolhido;
- qual combinacao possui maior `lift`, indicando associacao acima do esperado.

Exemplo para `Banana` no preview:

| Produto combinado | Pedidos juntos | Chance de sair junto | Lift |
| --- | ---: | ---: | ---: |
| Organic Strawberries | 820 | 44% | 1,82 |
| Organic Whole Milk | 730 | 39% | 1,61 |
| Organic Hass Avocado | 690 | 37% | 1,54 |

## Grupos de produtos

O dashboard apresenta grupos de produtos que mais saem juntos, como:

| Grupo | Produtos | Pedidos |
| --- | --- | ---: |
| Frutas organicas | Banana, Organic Strawberries, Organic Raspberries | 940 |
| Cafe da manha | Banana, Organic Whole Milk, Organic Strawberries | 810 |
| Salada fresca | Organic Baby Spinach, Organic Hass Avocado, Large Lemon | 760 |

## Analise por horario

A tela permite selecionar qualquer horario entre 00:00 e 23:00. Exemplos do preview:

| Horario | Produto lider esperado |
| ---: | --- |
| 09:00 | Banana |
| 17:00 | Organic Baby Spinach |

Tambem ha um mapa de calor cruzando hora do dia e produto, ajudando a identificar padroes de consumo por faixa horaria.

## Departamentos relevantes

| Departamento | Pedidos | Taxa de recompra |
| --- | ---: | ---: |
| produce | 7.200 | 64% |
| dairy eggs | 4.300 | 59% |
| snacks | 3.550 | 48% |
| beverages | 3.100 | 44% |
| frozen | 2.440 | 37% |
| pantry | 2.210 | 33% |

## Recomendacao de recompra

Na versao atual, a recomendacao usa a afinidade do produto selecionado, combinando chance de compra conjunta, lift e volume de pedidos juntos. Nas proximas fases, essa area sera conectada aos modelos de baseline, scikit-learn e LightGBM/XGBoost.

Produtos recomendados no preview:

1. Banana
2. Bag of Organic Bananas
3. Organic Whole Milk
4. Organic Hass Avocado
5. Organic Strawberries

## Como reproduzir

```powershell
cd "C:\Users\gamir\OneDrive\Documents\New project\instacart"
.venv\Scripts\streamlit run src/dashboard/app.py
```

Depois, abrir:

```text
http://127.0.0.1:8501
```

## Limitacao honesta

Estes numeros sao demonstrativos e servem para apresentar a experiencia do dashboard enquanto o pipeline real ainda esta sendo construido. Quando a camada gold for gerada, o dashboard passara a consumir os marts reais do projeto.
