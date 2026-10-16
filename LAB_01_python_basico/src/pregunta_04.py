import gzip


def leer_datos():
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as f:
        return [line.rstrip("").split("	") for line in f if line.strip()]


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    conteo = {}
    for row in leer_datos():
        mes = row[2].split("-")[1]
        conteo[mes] = conteo.get(mes, 0) + 1
    return sorted(conteo.items())
