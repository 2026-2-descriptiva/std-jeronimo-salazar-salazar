import gzip


def leer_datos():
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as f:
        return [line.rstrip("").split("	") for line in f if line.strip()]


def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """

    rows = leer_datos()
    return sum(int(row[1]) for row in rows)
