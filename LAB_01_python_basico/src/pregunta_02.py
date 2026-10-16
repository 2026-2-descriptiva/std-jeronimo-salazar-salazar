import gzip


def leer_datos():
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as f:
        return [line.rstrip("").split("	") for line in f if line.strip()]


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    conteo = {}
    for row in leer_datos():
        conteo[row[0]] = conteo.get(row[0], 0) + 1
    return sorted(conteo.items())
