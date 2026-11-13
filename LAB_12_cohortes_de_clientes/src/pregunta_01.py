import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    df = pd.read_csv("data/sales.csv.gz")
    df["order_month"] = pd.to_datetime(df["OrderDate"]).dt.to_period("M")
    df["first_month"] = df.groupby("CustomerID")["order_month"].transform("min")
    df["period_index"] = (df["order_month"] - df["first_month"]).apply(lambda x: x.n)
    df["cohort_month"] = df["first_month"].astype(str)

    retention = (
        df.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )
    retention["cohort_size"] = retention.groupby("cohort_month")[
        "active_customers"
    ].transform("first")
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    )

    retention.to_csv("submission/cohort_retention.csv", index=False)

    # Mapa de calor: los períodos no observados quedan como NaN (vacíos)
    matrix = retention.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    image = ax.imshow(matrix, cmap="Blues")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix.iloc[i, j]
            if pd.notna(value):
                ax.text(j, i, f"{value:.0%}", ha="center", va="center")
    ax.set_xticks(range(matrix.shape[1]), matrix.columns)
    ax.set_yticks(range(matrix.shape[0]), matrix.index)
    ax.set_xlabel("Período (meses desde la primera compra)")
    ax.set_ylabel("Cohorte")
    ax.set_title("Retención de clientes por cohorte")
    fig.colorbar(image, ax=ax, label="Retención")
    fig.savefig("submission/cohort_retention_heatmap.png")
    plt.close(fig)

    return retention
