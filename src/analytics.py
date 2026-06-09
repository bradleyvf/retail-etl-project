import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


df = pd.read_csv(
    "../data/data_master_clean.csv"
)

np.random.seed(42)

df["frecuencia_compra"] = np.random.randint(
    1,50,len(df)
)

df["num_devoluciones"] = np.random.randint(
    0,10,len(df)
)

df["ticket_promedio"] = np.random.uniform(
    100,5000,len(df)
)

df["visitas_web"] = np.random.randint(
    1,100,len(df)
)

df["compras_online"] = np.random.randint(
    1,50,len(df)
)

variables = [
    "monto",
    "edad",
    "ingresos",
    "puntos_lealtad",
    "gastos_mensuales",
    "frecuencia_compra",
    "num_devoluciones",
    "ticket_promedio",
    "visitas_web",
    "compras_online"
]

X = df[variables]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=3)

componentes = pca.fit_transform(
    X_scaled
)

print("\nVarianza explicada:")
print(
    pca.explained_variance_ratio_
)

print(
    "\nVarianza acumulada:",
    pca.explained_variance_ratio_.sum()
)

plt.figure(figsize=(8,5))

sns.boxplot(
    x=df["monto"]
)

plt.title(
    "Detección de Outliers en Montos"
)

plt.savefig(
    "../images/boxplot_ventas.png"
)

plt.close()

plt.figure(figsize=(8,6))

plt.scatter(
    componentes[:,0],
    componentes[:,1]
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title(
    "Clientes tras PCA"
)

plt.savefig(
    "../images/scatter_pca.png"
)

plt.close()

print(
    "\nGráficas generadas correctamente"
)