# Model Card

## Objetivo

Prever se um usuario comprara novamente um produto no proximo pedido.

## Abordagens planejadas

- Baseline por produtos historicamente recomprados pelo usuario.
- Modelo supervisionado com scikit-learn.
- Modelo robusto com LightGBM ou XGBoost, conforme viabilidade local.

## Metricas

- Precision.
- Recall.
- F1-score.
- Precision@k ou Recall@k para recomendacao.

## Limitacoes

O dataset nao contem precos, estoque, promocoes ou eventos externos. A avaliacao sera baseada na separacao temporal disponivel e na simulacao incremental documentada.

