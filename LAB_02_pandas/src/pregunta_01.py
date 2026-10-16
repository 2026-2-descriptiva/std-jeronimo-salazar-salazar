def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """

    import pandas as pd

    df = pd.read_csv("data/tbl0.tsv", sep="\t")
    return len(df)