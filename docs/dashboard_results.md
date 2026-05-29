# Resultados do Dashboard Streamlit

Esta pagina documenta os resultados apresentados na primeira versao executavel do dashboard Streamlit.

## Status atual

- Aplicacao: `src/dashboard/app.py`
- URL local usada no teste: `http://127.0.0.1:8501`
- Modo atual: demonstracao
- Objetivo: permitir visualizacao do produto analitico antes da ingestao real via Kaggle API

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

Na versao atual, a recomendacao usa uma ordenacao simples por taxa de recompra e volume historico. Nas proximas fases, essa area sera conectada aos modelos de baseline, scikit-learn e LightGBM/XGBoost.

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
