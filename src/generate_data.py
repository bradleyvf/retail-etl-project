import pandas as pd
import numpy as np
import sqlite3
import json
from faker import Faker
import random

fake = Faker("es_MX")

ventas = []

regiones = [
    "México",
    "mex",
    "mx",
    "Norte",
    "Sur",
    "Centro"
]

for i in range(1, 10001):

    ventas.append([
        i,
        random.randint(1, 2000),
        round(random.uniform(50, 5000), 2),
        fake.date_between(
            start_date="-2y",
            end_date="today"
        ).strftime("%d/%m/%Y"),
        random.choice(regiones),
        random.randint(1, 50)
    ])

ventas_df = pd.DataFrame(
    ventas,
    columns=[
        "id_transaccion",
        "customer_id",
        "monto",
        "fecha",
        "region",
        "id_tienda"
    ]
)

conn = sqlite3.connect("../data/ventas.db")

ventas_df.to_sql(
    "ventas_historicas",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Ventas SQL creadas")

perfiles = []

for i in range(1, 2001):

    perfiles.append({
        "customer_id": i,
        "edad": random.randint(18, 70),
        "preferencias": random.choice([
            "Tecnologia",
            "Moda",
            "Hogar",
            "Deportes"
        ]),
        "geolocalizacion": fake.city(),
        "ingresos": random.randint(
            10000,
            100000
        ),
        "puntos_lealtad": random.randint(
            0,
            10000
        ),
        "gastos_mensuales": random.randint(
            1000,
            50000
        )
    })

with open(
    "../data/perfiles_usuarios.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        perfiles,
        f,
        ensure_ascii=False,
        indent=4
    )

print("JSON creado")

productos = []

for i in range(1000):

    productos.append([
        random.choice([
            "Laptop",
            "Mouse",
            "Monitor",
            "Teclado",
            "Tablet"
        ]),
        random.choice([
            "Electrónica",
            "Accesorios"
        ]),
        random.randint(1, 500),
        round(
            random.uniform(
                100,
                20000
            ),
            2
        )
    ])

inventario = pd.DataFrame(
    productos,
    columns=[
        "producto",
        "categoria",
        "stock",
        "precio"
    ]
)

for col in inventario.columns:

    inventario.loc[
        inventario.sample(
            frac=0.10
        ).index,
        col
    ] = np.nan

# 5% duplicados

duplicados = inventario.sample(
    frac=0.05
)

inventario = pd.concat(
    [inventario, duplicados],
    ignore_index=True
)

inventario.to_csv(
    "../data/inventario.csv",
    index=False
)

print("Inventario CSV creado")
print("Proceso terminado")
