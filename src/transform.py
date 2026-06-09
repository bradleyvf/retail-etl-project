import pandas as pd
import sqlite3
import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler

conn = sqlite3.connect("../data/ventas.db")

ventas = pd.read_sql(
    """
    SELECT *
    FROM ventas_historicas
    ORDER BY id_transaccion DESC
    LIMIT 500
    """,
    conn
)

conn.close()

with open(
    "../data/perfiles_usuarios.json",
    "r",
    encoding="utf-8"
) as f:

    perfiles = pd.DataFrame(json.load(f))

inventario = pd.read_csv(
    "../data/inventario.csv"
)

ventas = ventas.drop_duplicates()

inventario = inventario.drop_duplicates()

inventario = inventario.dropna()

ventas["fecha"] = pd.to_datetime(
    ventas["fecha"],
    format="%d/%m/%Y"
)

ventas["region"] = (
    ventas["region"]
    .str.lower()
    .replace({
        "mex": "mexico",
        "mx": "mexico",
        "méxico": "mexico"
    })
)

master = ventas.merge(
    perfiles,
    on="customer_id",
    how="left"
)

master["segmento_cliente"] = np.where(
    (master["monto"] > 1000)
    &
    (master["edad"] < 30),
    "Premium Joven",
    "Regular"
)

cols = [
    "monto",
    "ingresos",
    "puntos_lealtad",
    "gastos_mensuales"
]

scaler = MinMaxScaler()

master[cols] = scaler.fit_transform(
    master[cols]
)

master.to_csv(
    "../data/data_master_clean.csv",
    index=False
)

print("ETL completado correctamente")
print(master.head())