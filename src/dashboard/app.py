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


def _demo_affinity() -> pd.DataFrame:
    """Return product-pair affinity metrics for cross-sell analysis."""
    rows = [
        ("Banana", "Organic Strawberries", 820, 0.44, 1.82),
        ("Banana", "Organic Whole Milk", 730, 0.39, 1.61),
        ("Banana", "Organic Hass Avocado", 690, 0.37, 1.54),
        ("Banana", "Organic Baby Spinach", 620, 0.33, 1.36),
        ("Banana", "Large Lemon", 540, 0.29, 1.21),
        ("Bag of Organic Bananas", "Organic Raspberries", 680, 0.44, 1.79),
        ("Bag of Organic Bananas", "Organic Strawberries", 650, 0.42, 1.72),
        ("Bag of Organic Bananas", "Organic Whole Milk", 580, 0.38, 1.57),
        ("Organic Strawberries", "Organic Raspberries", 510, 0.42, 1.88),
        ("Organic Strawberries", "Organic Whole Milk", 470, 0.39, 1.48),
        ("Organic Baby Spinach", "Organic Hass Avocado", 450, 0.40, 1.66),
        ("Organic Baby Spinach", "Large Lemon", 410, 0.36, 1.44),
        ("Organic Hass Avocado", "Large Lemon", 390, 0.38, 1.59),
        ("Organic Whole Milk", "Organic Raspberries", 360, 0.46, 1.74),
        ("Large Lemon", "Organic Baby Spinach", 350, 0.36, 1.44),
    ]

    reverse_rows = [(b, a, c, round(conf * 0.92, 2), round(lift * 0.96, 2)) for a, b, c, conf, lift in rows]
    return pd.DataFrame(
        rows + reverse_rows,
        columns=["anchor_product", "paired_product", "orders_together", "confidence", "lift"],
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


def _demo_product_groups() -> pd.DataFrame:
    """Return basket group demo metrics for common product bundles."""
    return pd.DataFrame(
        {
            "group_name": [
                "Frutas organicas",
                "Cafe da manha",
                "Salada fresca",
                "Lanche saudavel",
                "Reposicao de laticinios",
                "Cesta basica de hortifruti",
            ],
            "products": [
                "Banana, Organic Strawberries, Organic Raspberries",
                "Banana, Organic Whole Milk, Organic Strawberries",
                "Organic Baby Spinach, Organic Hass Avocado, Large Lemon",
                "Bag of Organic Bananas, Organic Raspberries, Organic Whole Milk",
                "Organic Whole Milk, Organic Strawberries, Banana",
                "Banana, Organic Hass Avocado, Large Lemon",
            ],
            "orders": [940, 810, 760, 690, 620, 590],
            "avg_basket_size": [7.3, 8.1, 6.4, 7.8, 9.2, 6.9],
            "reorder_rate": [0.68, 0.62, 0.57, 0.54, 0.61, 0.49],
        }
    )


def _demo_hourly_sales(products: pd.DataFrame) -> pd.DataFrame:
    """Return product sales by hour for day-part analysis."""
    product_names = products["product_name"].tolist()
    rows = []
    for hour in range(24):
        for index, product in enumerate(product_names):
            morning_boost = 1.8 if product in {"Banana", "Bag of Organic Bananas"} and 7 <= hour <= 10 else 1
            afternoon_boost = 1.7 if product in {"Organic Baby Spinach", "Organic Hass Avocado"} and 16 <= hour <= 18 else 1
            evening_boost = 1.5 if product in {"Organic Whole Milk", "Large Lemon"} and 18 <= hour <= 21 else 1
            base = max(18, 120 - index * 9)
            hour_curve = 0.55 + (hour / 24 if hour <= 17 else (24 - hour) / 24)
            orders = int(base * hour_curve * morning_boost * afternoon_boost * evening_boost)
            rows.append((hour, product, orders))

    return pd.DataFrame(rows, columns=["order_hour_of_day", "product_name", "orders"])


def load_dashboard_data() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    bool,
]:
    """Load gold dashboard marts when present, otherwise use demo data."""
    orders_path = GOLD_DIR / "dashboard_orders.parquet"
    products_path = GOLD_DIR / "dashboard_products.parquet"
    departments_path = GOLD_DIR / "dashboard_departments.parquet"
    affinity_path = GOLD_DIR / "dashboard_product_affinity.parquet"
    groups_path = GOLD_DIR / "dashboard_product_groups.parquet"
    hourly_path = GOLD_DIR / "dashboard_hourly_sales.parquet"

    expected_paths = [
        orders_path,
        products_path,
        departments_path,
        affinity_path,
        groups_path,
        hourly_path,
    ]

    if all(path.exists() for path in expected_paths):
        return (
            pd.read_parquet(orders_path),
            pd.read_parquet(products_path),
            pd.read_parquet(departments_path),
            pd.read_parquet(affinity_path),
            pd.read_parquet(groups_path),
            pd.read_parquet(hourly_path),
            False,
        )

    products = _demo_products()
    return (
        _demo_orders(),
        products,
        _demo_departments(),
        _demo_affinity(),
        _demo_product_groups(),
        _demo_hourly_sales(products),
        True,
    )


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


def render_overview(orders: pd.DataFrame, products: pd.DataFrame, departments: pd.DataFrame) -> None:
    """Render high-level ingestion and product overview."""
    latest_run = orders["run_date"].max()
    total_orders = int(orders["orders_ingested"].sum())
    total_items = int(orders["items_ingested"].sum())
    avg_basket = total_items / total_orders if total_orders else 0

    metric_cols = st.columns(4)
    metric_cols[0].metric("Pedidos ingeridos", f"{total_orders:,}".replace(",", "."))
    metric_cols[1].metric("Itens ingeridos", f"{total_items:,}".replace(",", "."))
    metric_cols[2].metric("Tamanho medio da cesta", f"{avg_basket:.2f}")
    metric_cols[3].metric("Ultima atualizacao", latest_run.strftime("%d/%m/%Y"))

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


def render_affinity(affinity: pd.DataFrame, selected_product: str, top_n: int) -> None:
    """Render product affinity and top pair recommendations."""
    selected_affinity = (
        affinity[affinity["anchor_product"] == selected_product]
        .sort_values(["confidence", "lift", "orders_together"], ascending=False)
        .head(top_n)
    )
    top_two = selected_affinity.head(2)

    st.subheader(f"Quem compra {selected_product} tambem tende a comprar")

    if top_two.empty:
        st.warning("Nao ha combinacoes suficientes para o produto selecionado.")
        return

    cards = st.columns(2)
    for index, (_, row) in enumerate(top_two.iterrows()):
        cards[index].metric(
            row["paired_product"],
            f"{row['confidence']:.0%}",
            f"lift {row['lift']:.2f}",
        )

    left, right = st.columns((1, 1))
    with left:
        fig = px.bar(
            selected_affinity.sort_values("confidence", ascending=True),
            x="confidence",
            y="paired_product",
            orientation="h",
            color="lift",
            labels={
                "confidence": "Chance de sair junto",
                "paired_product": "Produto combinado",
                "lift": "Lift",
            },
        )
        fig.update_xaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.dataframe(
            selected_affinity.rename(
                columns={
                    "paired_product": "produto_combinado",
                    "orders_together": "pedidos_juntos",
                    "confidence": "chance_compra_conjunta",
                    "lift": "lift",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


def render_groups(groups: pd.DataFrame, top_n: int) -> None:
    """Render common product bundles."""
    top_groups = groups.sort_values("orders", ascending=False).head(top_n)
    st.subheader("Grupos de produtos que mais saem juntos")

    fig = px.bar(
        top_groups.sort_values("orders", ascending=True),
        x="orders",
        y="group_name",
        color="reorder_rate",
        orientation="h",
        labels={
            "orders": "Pedidos",
            "group_name": "Grupo",
            "reorder_rate": "Taxa de recompra",
        },
    )
    fig.update_coloraxes(colorbar_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        top_groups.rename(
            columns={
                "group_name": "grupo",
                "products": "produtos",
                "orders": "pedidos",
                "avg_basket_size": "tamanho_medio_cesta",
                "reorder_rate": "taxa_recompra",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_hourly(hourly_sales: pd.DataFrame, selected_hour: int, top_n: int) -> None:
    """Render product sales by selected hour and dynamic heatmap."""
    by_hour = (
        hourly_sales[hourly_sales["order_hour_of_day"] == selected_hour]
        .sort_values("orders", ascending=False)
        .head(top_n)
    )
    best_product = by_hour.iloc[0]["product_name"] if not by_hour.empty else "sem dados"

    st.subheader(f"No horario das {selected_hour:02d}:00, vende mais")
    st.metric("Produto lider", best_product)

    left, right = st.columns((1, 1.15))
    with left:
        fig = px.bar(
            by_hour.sort_values("orders", ascending=True),
            x="orders",
            y="product_name",
            orientation="h",
            labels={"orders": "Pedidos", "product_name": "Produto"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        pivot = hourly_sales.pivot_table(
            index="order_hour_of_day",
            columns="product_name",
            values="orders",
            aggfunc="sum",
            fill_value=0,
        )
        fig = px.imshow(
            pivot,
            aspect="auto",
            labels={"x": "Produto", "y": "Hora", "color": "Pedidos"},
        )
        st.plotly_chart(fig, use_container_width=True)


def render_dynamic_table(
    products: pd.DataFrame,
    affinity: pd.DataFrame,
    hourly_sales: pd.DataFrame,
    selected_product: str,
    selected_hour: int,
) -> None:
    """Render a flexible table combining product, affinity and hourly metrics."""
    product_metrics = products.rename(columns={"product_name": "anchor_product"})
    hourly_metrics = hourly_sales[hourly_sales["order_hour_of_day"] == selected_hour].rename(
        columns={"product_name": "anchor_product", "orders": "orders_at_selected_hour"}
    )
    table = (
        affinity.merge(product_metrics, on="anchor_product", how="left")
        .merge(hourly_metrics[["anchor_product", "orders_at_selected_hour"]], on="anchor_product", how="left")
        .fillna({"orders_at_selected_hour": 0})
    )

    only_selected = st.checkbox("Mostrar apenas produto selecionado", value=True)
    if only_selected:
        table = table[table["anchor_product"] == selected_product]

    table = table.sort_values(["confidence", "lift"], ascending=False)
    st.subheader("Tabela dinamica de afinidade e horario")
    st.dataframe(
        table.rename(
            columns={
                "anchor_product": "produto_base",
                "paired_product": "produto_combinado",
                "orders_together": "pedidos_juntos",
                "confidence": "chance_compra_conjunta",
                "lift": "lift",
                "orders": "pedidos_produto_base",
                "reorder_rate": "taxa_recompra_produto_base",
                "orders_at_selected_hour": f"pedidos_as_{selected_hour:02d}h",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    """Render the Streamlit dashboard."""
    orders, products, departments, affinity, groups, hourly_sales, is_demo = load_dashboard_data()
    render_header(is_demo)

    with st.sidebar:
        st.header("Filtros")
        product_options = sorted(products["product_name"].unique())
        default_product_index = product_options.index("Banana") if "Banana" in product_options else 0
        selected_product = st.selectbox(
            "Produto para analisar",
            product_options,
            index=default_product_index,
        )
        selected_hour = st.selectbox("Horario da compra", list(range(24)), index=9)
        top_n = st.slider("Quantidade de resultados", min_value=3, max_value=10, value=5)

    tabs = st.tabs(
        [
            "Visao geral",
            "Afinidade de produtos",
            "Grupos de compra",
            "Analise por horario",
            "Tabela dinamica",
            "Previsao de compra",
        ]
    )

    with tabs[0]:
        render_overview(orders, products, departments)

    with tabs[1]:
        render_affinity(affinity, selected_product, top_n)

    with tabs[2]:
        render_groups(groups, top_n)

    with tabs[3]:
        render_hourly(hourly_sales, selected_hour, top_n)

    with tabs[4]:
        render_dynamic_table(products, affinity, hourly_sales, selected_product, selected_hour)

    with tabs[5]:
        st.subheader("Previsao de proxima compra")
        user_id = st.number_input("Usuario", min_value=1, value=42, step=1)
        top_recommendations = (
            affinity[affinity["anchor_product"] == selected_product]
            .sort_values(["confidence", "lift", "orders_together"], ascending=False)
            .head(5)
        )

        st.write(
            f"Para o usuario `{user_id}`, partindo do produto `{selected_product}`, "
            "os itens recomendados para recompra/complemento sao:"
        )
        st.dataframe(
            top_recommendations.rename(
                columns={
                    "paired_product": "produto_recomendado",
                    "orders_together": "pedidos_juntos",
                    "confidence": "probabilidade_proxy_compra_conjunta",
                    "lift": "lift",
                }
            )[["produto_recomendado", "pedidos_juntos", "probabilidade_proxy_compra_conjunta", "lift"]],
            use_container_width=True,
            hide_index=True,
        )

    st.caption(f"Dashboard renderizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}.")


if __name__ == "__main__":
    main()
