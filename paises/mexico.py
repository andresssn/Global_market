import yfinance as yf
from .base_pais import PaisBase


class PaisMexico(PaisBase):

  def __init__(self):
    super().__init__("México")

  def obtener_datos(self) -> dict:
    # 1. Obtención de tipo de cambio en vivo
    try:
      fx = float(yf.Ticker("USDMXN=X").history(period="5d")["Close"].iloc[-1])
    except Exception:
      fx = 18.59

    # 2. Aquí puedes conectar la API de Banxico en el futuro; por ahora valores base
    m0_mxn = 3.53  # Billones MXN
    m4_mxn = 22.20  # Billones MXN

    # 3. Parámetros patrimoniales locales
    ingreso_mensual_mxn = 250000.0
    ingreso_bruto_usd = (ingreso_mensual_mxn * 12) / fx

    return {
        "ingreso_bruto_usd": ingreso_bruto_usd,
        "tasa_impuestos": 0.12,
        "costo_subsistencia": 0.22,
        "m0_billones": m0_mxn,
        "agregado_l_billones": m4_mxn,
        "tipo_cambio_usd": fx,
    }

  #if __name__ == "__main__":
  #  mx = PaisMexico()
  #  print(mx.evaluar_riesgo(precio_oro_usd=3885.60))

