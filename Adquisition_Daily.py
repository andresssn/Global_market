from datetime import datetime
import os
from paises import PAISES_ACTIVOS
import pandas as pd
import yfinance as yf

ARCHIVO_CSV = "historico_macro_riesgo.csv"


def obtener_precio_oro() -> float:
  try:
    return float(yf.Ticker("GC=F").history(period="5d")["Close"].iloc[-1])
  except Exception:
    return 3885.60


def actualizar_historico():
  fecha_hoy = datetime.now().strftime("%Y-%m-%d")
  oro_usd = obtener_precio_oro()

  filas_hoy = []
  for pais in PAISES_ACTIVOS:
    resultado = pais.evaluar_riesgo(oro_usd)
    resultado["Fecha"] = fecha_hoy
    filas_hoy.append(resultado)

  df_nuevos = pd.DataFrame(filas_hoy)

  if os.path.exists(ARCHIVO_CSV):
    df_actual = pd.read_csv(ARCHIVO_CSV)
    if "Pais" in df_actual.columns:
      df_actual = df_actual[df_actual["Fecha"] != fecha_hoy]
      df_final = pd.concat([df_actual, df_nuevos], ignore_index=True)
    else:
      df_final = df_nuevos
  else:
    df_final = df_nuevos

  # Ordenar columnas con Fecha al inicio
  columnas = [
      "Fecha",
      "Pais",
      "Oro_USD",
      "Tipo_Cambio",
      "Multiplo_L_M0",
      "Oz_Libres_Anio",
      "Producto_Libre",
  ]
  df_final = df_final[columnas]
  df_final.to_csv(ARCHIVO_CSV, index=False)
  print(
      f"[{fecha_hoy}] Procesados {len(filas_hoy)} objetos país correctamente."
  )


if __name__ == "__main__":
  actualizar_historico()
