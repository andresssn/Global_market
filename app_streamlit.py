import os
from Adquisition_Daily import actualizar_historico
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Monitor Global L/M0 y Oro", layout="wide")
st.title("🌍 Monitor Patrimonial Multipaís: Apalancamiento L/M0 y Oro")

ARCHIVO_CSV = "historico_macro_riesgo.csv"

# Si el CSV no existe o aún tiene el formato viejo sin columna 'Pais', lo regenera
if not os.path.exists(ARCHIVO_CSV):
  with st.spinner("Generando primer registro multipaís..."):
    actualizar_historico()
else:
  df_check = pd.read_csv(ARCHIVO_CSV)
  if "Pais" not in df_check.columns:
    with st.spinner("Migrando historial al nuevo formato multipaís..."):
      actualizar_historico()

df = pd.read_csv(ARCHIVO_CSV)
fecha_reciente = df["Fecha"].max()
df_hoy = df[df["Fecha"] == fecha_reciente]

# 1. Tarjetas dinámicas: crea una columna automáticamente por cada objeto País activo
oro_actual = df_hoy["Oro_USD"].iloc[0]
st.subheader(
    f"Snapshot Actual ({fecha_reciente}) — Oro Spot: ${oro_actual:,.2f} USD/oz"
)

cols = st.columns(len(df_hoy))
for idx, (_, fila) in enumerate(df_hoy.iterrows()):
  with cols[idx]:
    st.metric(
        label=f"{fila['Pais']} (L/M0: {fila['Multiplo_L_M0']}x)",
        value=f"{fila['Oz_Libres_Anio']} oz/año",
        delta=f"Índice Ruptura: {fila['Producto_Libre']}",
    )

st.divider()

# 2. Gráficas comparativas automáticas (crecen solas al agregar países)
col_izq, col_der = st.columns(2)

with col_izq:
  fig1 = px.line(
      df,
      x="Fecha",
      y="Producto_Libre",
      color="Pais",
      markers=True,
      title="Evolución del Producto Libre vs Umbral Crítico (1.0)",
  )
  fig1.add_hline(
      y=1.0,
      line_dash="dash",
      line_color="red",
      annotation_text="Umbral Crítico (1.0)",
  )
  st.plotly_chart(fig1, use_container_width=True)

with col_der:
  fig2 = px.bar(
      df_hoy,
      x="Pais",
      y="Oz_Libres_Anio",
      color="Pais",
      title="Capacidad Anual de Acumulación (Onzas Libres)",
  )
  st.plotly_chart(fig2, use_container_width=True)

# 3. Tabla histórica completa
st.subheader("Registro Histórico Multipaís")
st.dataframe(
    df.sort_values(by=["Fecha", "Pais"], ascending=[False, True]),
    use_container_width=True,
)
