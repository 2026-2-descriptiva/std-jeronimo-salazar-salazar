import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Una autoridad aeronáutica publica cada año un ranking de aerolíneas según
    su tasa de demora, y algunas aerolíneas se quejan de que es injusto: las
    demoras se acumulan a lo largo del día, de modo que una aerolínea con
    muchos vuelos en la tarde y la noche parece peor aunque opere igual de
    bien que las demás. Su tarea es construir un ranking que tenga en cuenta
    la mezcla de horarios de cada aerolínea.

    El archivo `data/flights_by_carrier_day_hour.csv.gz` tiene los vuelos
    nacionales entre 2006 y 2008, agregados por año, mes, día de la semana,
    hora programada de salida (`scheduled_departure_hour`) y aerolínea
    (`reporting_airline`). Use las columnas `operated_flights` (vuelos
    operados) y `delayed_departure_15_flights` (vuelos que salieron con 15
    minutos o más de demora).

    Siga estos pasos:

    1. Calcule la tasa nacional de demora de cada hora programada de salida:
       vuelos demorados sobre vuelos operados, con todas las aerolíneas
       juntas.
    2. Para cada aerolínea, calcule las demoras esperadas: en cada hora,
       multiplique sus vuelos operados por la tasa nacional de esa hora, y
       sume sobre todas las horas. Son las demoras que tendría si en cada hora
       se comportara como el promedio nacional.
    3. Divida las demoras observadas entre las esperadas. Un valor mayor que 1
       significa que la aerolínea se demora más de lo que explican sus
       horarios.

    Genere dos archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `hourly_delay_rates.csv`, con una fila por hora, de 0 a 23:
       `scheduled_departure_hour`, `operated_flights`,
       `delayed_departure_15_flights` y `delay_rate`.

    2. `carrier_adjusted_delays.csv`, con una fila por aerolínea:
       `reporting_airline`, `operated_flights`,
       `delayed_departure_15_flights`, `delay_rate` (la tasa sin ajustar),
       `expected_delayed_flights`, `observed_to_expected_ratio`, `crude_rank`
       y `adjusted_rank`. Incluya solamente aerolíneas con al menos 100 000
       vuelos operados. `crude_rank` es la posición según `delay_rate` y
       `adjusted_rank` la posición según `observed_to_expected_ratio`; en
       ambos, 1 es la peor aerolínea. Ordene la tabla por `adjusted_rank`.

    Compare los dos rankings: las aerolíneas que cambian de posición son las
    que el ranking sin ajustar juzga mal por sus horarios.

    La función también debe retornar las dos tablas, en el mismo orden.

    Ejemplo del formato de `carrier_adjusted_delays.csv`:

        reporting_airline,operated_flights,...,crude_rank,adjusted_rank
        EV,819223,...,1,1
        ...
    """

    df = pd.read_csv("data/flights_by_carrier_day_hour.csv.gz")
    cols = ["operated_flights", "delayed_departure_15_flights"]

    # 1. Tasa nacional de demora por hora
    hourly = df.groupby("scheduled_departure_hour")[cols].sum().reset_index()
    hourly[cols] = hourly[cols].astype(int)
    hourly["delay_rate"] = (
        hourly["delayed_departure_15_flights"] / hourly["operated_flights"]
    )

    # 2. Demoras esperadas de cada aerolínea según sus horarios
    by_hour = (
        df.groupby(["reporting_airline", "scheduled_departure_hour"])[cols]
        .sum()
        .reset_index()
        .merge(hourly[["scheduled_departure_hour", "delay_rate"]])
    )
    by_hour["expected_delayed_flights"] = (
        by_hour["operated_flights"] * by_hour["delay_rate"]
    )

    carriers = (
        by_hour.groupby("reporting_airline")[cols + ["expected_delayed_flights"]]
        .sum()
        .reset_index()
    )
    carriers[cols] = carriers[cols].astype(int)
    carriers = carriers[carriers["operated_flights"] >= 100000].copy()

    # 3. Razón observado / esperado y rankings
    carriers["delay_rate"] = (
        carriers["delayed_departure_15_flights"] / carriers["operated_flights"]
    )
    carriers["observed_to_expected_ratio"] = (
        carriers["delayed_departure_15_flights"] / carriers["expected_delayed_flights"]
    )
    carriers["crude_rank"] = carriers["delay_rate"].rank(ascending=False).astype(int)
    carriers["adjusted_rank"] = (
        carriers["observed_to_expected_ratio"].rank(ascending=False).astype(int)
    )
    carriers = carriers.sort_values("adjusted_rank")[
        ["reporting_airline", "operated_flights", "delayed_departure_15_flights",
         "delay_rate", "expected_delayed_flights", "observed_to_expected_ratio",
         "crude_rank", "adjusted_rank"]
    ]

    hourly.to_csv("submission/hourly_delay_rates.csv", index=False)
    carriers.to_csv("submission/carrier_adjusted_delays.csv", index=False)

    return hourly, carriers
