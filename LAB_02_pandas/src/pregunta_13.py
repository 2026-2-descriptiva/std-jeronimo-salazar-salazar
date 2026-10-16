def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    import pandas as pd

    df0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    df2 = pd.read_csv("data/tbl2.tsv", sep="\t")

    resultado = df0.merge(df2, on="c0")
    resultado = resultado.groupby("c1")["c5b"].sum()
    resultado = resultado.sort_index()

    return resultado

