import os
import pandas as pd
import plotly.express as px
import streamlit as st
from Adquisition_Daily import actualizar_historico  # Importa tu función recolectora

st.set_page_config(page_title="Monitor Riesgo Macro y Oro", layout="wide")
st.title("📊 Monitor Patrimonial: Apalancamiento L/M0 y Poder en Oro")

ARCHIVO_CSV = "historico_macro_riesgo.csv"

# Si el CSV aún no existe, lo genera en ese momento
if not os.path.exists(ARCHIVO_CSV):
  with st.spinner("Generando primer registro histórico en tiempo real..."):
    actualizar_historico()

df = pd.read_csv(ARCHIVO_CSV)
ultimo = df.iloc[-1]

# Tarjetas de indicadores principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Oro Spot (USD/oz)", f"${ultimo['Oro_USD']:,.2f}")
col2.metric("Múltiplo EE. UU. (L/M0)", f"{ultimo['USA_L_M0']}x")
col3.metric("Oz Libres / Año", f"{ultimo['Oz_Libres_Anio']} oz")
col4.metric("Producto Libre (Umbral > 1.0)", f"{ultimo['Producto_Libre_MX']}")

# Gráfica histórica
fig = px.line(
    df,
    x="Fecha",
    y="Producto_Libre_MX",
    markers=True,
    title="Histórico Diario: Producto Libre vs Umbral de Ruptura (1.0)",
)
fig.add_hline(y=1.0, line_dash="dash", line_color="red")
st.plotly_chart(fig, use_container_width=True)

# Tabla de datos históricos
st.subheader("Registro Histórico Guardado")
st.dataframe(df.tail(30), use_container_width=True)
