import gzip


def leer_datos():
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as f:
        return [line.rstrip("").split("	") for line in f if line.strip()]


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    sumas = {}
    for row in leer_datos():
        total = sum(int(par.split(":")[1]) for par in row[4].split(","))
        sumas[row[0]] = sumas.get(row[0], 0) + total
    return dict(sorted(sumas.items()))
