import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    df = pd.read_csv("data/superstore_orders.csv.gz", sep=";", decimal=",")
    df["loss"] = df["Profit"] < 0
    df["lost"] = -df["Profit"].where(df["loss"], 0)
    df["discount_band"] = pd.cut(
        df["Discount"],
        bins=[-1, 0, 0.05, 0.10, float("inf")],
        labels=["0%", "1%-5%", "6%-10%", "más de 10%"],
    )

    # 1. Resumen general
    summary = pd.DataFrame(
        {
            "lines": [len(df)],
            "orders": [df["Order ID"].nunique()],
            "sales": [df["Sales"].sum()],
            "profit": [df["Profit"].sum()],
            "profit_margin": [df["Profit"].sum() / df["Sales"].sum()],
            "loss_lines": [df["loss"].sum()],
            "loss_line_rate": [df["loss"].mean()],
            "lost_profit": [df["lost"].sum()],
        }
    )

    # 2. Resumen por rango de descuento
    discounts = (
        df.groupby("discount_band", observed=False)
        .agg(
            lines=("Sales", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            loss_line_rate=("loss", "mean"),
            lost_profit=("lost", "sum"),
        )
        .reset_index()
    )
    discounts["profit_margin"] = discounts["profit"] / discounts["sales"]
    discounts = discounts[
        ["discount_band", "lines", "sales", "profit", "profit_margin",
         "loss_line_rate", "lost_profit"]
    ]

    # 3. Segmentos segmento-categoría que más pierden
    segments = (
        df.groupby(["Customer Segment", "Product Category"])
        .agg(
            lines=("Sales", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            lost_profit=("lost", "sum"),
        )
        .reset_index()
    )
    segments["profit_margin"] = segments["profit"] / segments["sales"]
    segments = segments[segments["lines"] >= 100]
    segments = segments.sort_values("lost_profit", ascending=False).head(5)
    segments = segments[
        ["Customer Segment", "Product Category", "lines", "sales", "profit",
         "profit_margin", "lost_profit"]
    ]

    summary.to_csv("submission/profitability_summary.csv", index=False)
    discounts.to_csv("submission/discount_summary.csv", index=False)
    segments.to_csv("submission/priority_segments.csv", index=False)

    return summary, discounts, segments
