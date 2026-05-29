"""Streamlit dashboard for the Instacart portfolio project.

The app is intentionally able to run before the Kaggle data is downloaded.
When gold-layer files become available, the loading functions can be extended
without changing the page structure.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_DIR = PROJECT_ROOT / "data" / "gold"


def _demo_orders() -> pd.DataFrame:
    """Return a small deterministic dataset for the first dashboard run."""
    return pd.DataFrame(
        {
            "run_date": pd.date_range("2026-01-01", periods=10, freq="D"),
            "orders_ingested": [4200, 4600, 5100, 5300, 5700, 6100, 6400, 6900, 7100, 7600],
            "items_ingested": [16500, 18100, 20300, 21700, 22900, 24400, 26000, 27900, 29100, 30600],
        }
    )


def _demo_products() -> pd.DataFrame:
    """Return product-level demo metrics shaped like the future gold mart."""
    return pd.DataFrame(
        {
            "product_name": [
                "Banana",
                "Bag of Organic Bananas",
                "Organic Strawberries",
                "Organic Baby Spinach",
                "Organic Hass Avocado",
                "Large Lemon",
                "Organic Raspberries",
                "Organic Whole Milk",
            ],
            "orders": [1872, 1540, 1221, 1130, 1018, 965, 842, 788],
            "reorder_rate": [0.72, 0.69, 0.61, 0.58, 0.63, 0.42, 0.55, 0.67],
        }
    )


def _demo_departments() -> pd.DataFrame:
    """Return department demo metrics for the first portfolio preview."""
    return pd.DataFrame(
        {
            "department": ["produce", "dairy eggs", "snacks", "beverages", "frozen", "pantry"],
            "orders": [7200, 4300, 3550, 3100, 2440, 2210],
            "reorder_rate": [0.64, 0.59, 0.48, 0.44, 0.37, 0.33],
        }
    )


def load_dashboard_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, bool]:
    """Load gold dashboard marts when present, otherwise use demo data."""
    orders_path = GOLD_DIR / "dashboard_orders.parquet"
    products_path = GOLD_DIR / "dashboard_products.parquet"
    departments_path = GOLD_DIR / "dashboard_departments.parquet"

    if orders_path.exists() and products_path.exists() and departments_path.exists():
        return (
            pd.read_parquet(orders_path),
            pd.read_parquet(products_path),
            pd.read_parquet(departments_path),
            False,
        )

    return _demo_orders(), _demo_products(), _demo_departments(), True


def render_header(is_demo: bool) -> None:
    """Render the dashboard header and project status."""
    st.set_page_config(page_title="Instacart Analytics", layout="wide")
    st.title("Instacart Market Basket Analytics")
    st.caption("Portfolio de dados: ingestao simulada, marts analiticos e previsao de recompra.")

    if is_demo:
        st.info(
            "Visualizacao em modo demonstracao. Baixe o dataset Kaggle e execute o pipeline "
            "para substituir estes dados pelos marts da camada gold."
        )


def main() -> None:
    """Render the Streamlit dashboard."""
    orders, products, departments, is_demo = load_dashboard_data()
    render_header(is_demo)

    latest_run = orders["run_date"].max()
    total_orders = int(orders["orders_ingested"].sum())
    total_items = int(orders["items_ingested"].sum())
    avg_basket = total_items / total_orders if total_orders else 0

    metric_cols = st.columns(4)
    metric_cols[0].metric("Pedidos ingeridos", f"{total_orders:,}".replace(",", "."))
    metric_cols[1].metric("Itens ingeridos", f"{total_items:,}".replace(",", "."))
    metric_cols[2].metric("Tamanho medio da cesta", f"{avg_basket:.2f}")
    metric_cols[3].metric("Ultima atualizacao", latest_run.strftime("%d/%m/%Y"))

    st.divider()

    left, right = st.columns((1.25, 1))
    with left:
        st.subheader("Evolucao da ingestao diaria simulada")
        fig = px.line(
            orders,
            x="run_date",
            y=["orders_ingested", "items_ingested"],
            markers=True,
            labels={"run_date": "Data simulada", "value": "Quantidade", "variable": "Metrica"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Produtos mais comprados")
        fig = px.bar(
            products.sort_values("orders", ascending=True),
            x="orders",
            y="product_name",
            orientation="h",
            labels={"orders": "Pedidos", "product_name": "Produto"},
        )
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Produtos mais recomprados")
        fig = px.bar(
            products.sort_values("reorder_rate", ascending=True),
            x="reorder_rate",
            y="product_name",
            orientation="h",
            labels={"reorder_rate": "Taxa de recompra", "product_name": "Produto"},
        )
        fig.update_xaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Departamentos relevantes")
        fig = px.scatter(
            departments,
            x="orders",
            y="reorder_rate",
            size="orders",
            color="department",
            labels={
                "orders": "Pedidos",
                "reorder_rate": "Taxa de recompra",
                "department": "Departamento",
            },
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Previsao de proxima compra")
    user_id = st.number_input("Usuario", min_value=1, value=42, step=1)
    top_recommendations = products.sort_values(["reorder_rate", "orders"], ascending=False).head(5)

    st.write(f"Produtos recomendados para recompra do usuario `{user_id}`:")
    st.dataframe(
        top_recommendations.rename(
            columns={
                "product_name": "produto",
                "orders": "pedidos_historicos",
                "reorder_rate": "probabilidade_proxy_recompra",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(f"Dashboard renderizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}.")


if __name__ == "__main__":
    main()
