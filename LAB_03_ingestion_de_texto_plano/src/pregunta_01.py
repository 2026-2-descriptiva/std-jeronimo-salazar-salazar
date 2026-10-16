def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    import re

    import pandas as pd

    with open("data/clusters_report.txt", encoding="utf-8") as file:
        lines = file.readlines()[4:]

    rows = []
    for line in lines:
        if not line.strip():
            continue
        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$", line)
        if match:
            cluster, cantidad, porcentaje, palabras = match.groups()
            rows.append(
                [int(cluster), int(cantidad), float(porcentaje.replace(",", ".")), palabras]
            )
        else:
            rows[-1][3] += " " + line.strip()

    for row in rows:
        palabras = re.sub(r"\s+", " ", row[3]).strip().rstrip(".")
        row[3] = re.sub(r"\s*,\s*", ", ", palabras)

    return pd.DataFrame(
        rows,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )
