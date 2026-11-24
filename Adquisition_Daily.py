from datetime import datetime
import os
import pandas as pd
import yfinance as yf

ARCHIVO_CSV = "historico_macro_riesgo.csv"

# Tus parámetros base para el registro histórico diario
INGRESO_MENSUAL_MXN = 250000.0
TASA_IMPUESTOS = 0.12
COSTO_SUBSISTENCIA = 0.22
DEUDA_USA_T = 32.7
FONDOS_INST_USA_T = 5.5
M4_MEXICO_B = 22.20
M0_MEXICO_B = 3.53


def obtener_dato_fred(serie_id):
  url = f"https://stlouisfed.org{serie_id}"
  df = pd.read_csv(url)
  df = df[df[serie_id] != "."]
  return float(df.iloc[-1][serie_id])


def actualizar_historico():
  oro = float(yf.Ticker("GC=F").history(period="5d")["Close"].iloc[-1])
  usd_mxn = float(yf.Ticker("USDMXN=X").history(period="5d")["Close"].iloc[-1])
  m0_usa = obtener_dato_fred("BOGMBASE") / 1_000_000.0
  m2_usa = obtener_dato_fred("WM2NS") / 1_000.0

  agregado_l_usa = m2_usa + FONDOS_INST_USA_T + DEUDA_USA_T
  multiplo_usa = agregado_l_usa / m0_usa
  multiplo_mx = M4_MEXICO_B / M0_MEXICO_B

  ingreso_anual_usd = (INGRESO_MENSUAL_MXN * 12) / usd_mxn
  flujo_libre_usd = (
      ingreso_anual_usd * (1 - TASA_IMPUESTOS) * (1 - COSTO_SUBSISTENCIA)
  )
  oz_libres = flujo_libre_usd / oro
  producto_libre_mx = oz_libres * multiplo_mx

  nuevo_registro = pd.DataFrame([{
      "Fecha": datetime.now().strftime("%Y-%m-%d"),
      "Oro_USD": round(oro, 2),
      "USD_MXN": round(usd_mxn, 2),
      "USA_L_M0": round(multiplo_usa, 2),
      "MX_M4_M0": round(multiplo_mx, 2),
      "Oz_Libres_Anio": round(oz_libres, 2),
      "Producto_Libre_MX": round(producto_libre_mx, 2),
  }])

  if os.path.exists(ARCHIVO_CSV):
    df_actual = pd.read_csv(ARCHIVO_CSV)
    # Evitar duplicados si se corre dos veces el mismo día
    df_actual = df_actual[
        df_actual["Fecha"] != nuevo_registro["Fecha"].iloc[0]
    ]
    df_final = pd.concat([df_actual, nuevo_registro], ignore_index=True)
  else:
    df_final = nuevo_registro

  df_final.to_csv(ARCHIVO_CSV, index=False)
  print("Historial actualizado:", nuevo_registro.to_dict(orient="records"))


if __name__ == "__main__":
  actualizar_historico()
