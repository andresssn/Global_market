import io
import urllib.request
import pandas as pd
from .base_pais import PaisBase


class PaisUSA(PaisBase):

  def __init__(self):
    super().__init__("Estados Unidos")

  def _leer_fred(self, serie_id: str, respaldo: float) -> float:
    url = f"https://stlouisfed.org{serie_id}"
    try:
      req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
      with urllib.request.urlopen(req, timeout=10) as resp:
        df = pd.read_csv(io.StringIO(resp.read().decode("utf-8")))
      df = df[df[serie_id] != "."]
      return float(df.iloc[-1][serie_id])
    except Exception:
      return respaldo

  def obtener_datos(self) -> dict:
    m0_usa_t = self._leer_fred("BOGMBASE", 5450000.0) / 1_000_000.0
    m2_usa_t = self._leer_fred("WM2NS", 23410.0) / 1_000.0

    # Agregado L = M2 + Fondos Institucionales + Deuda en manos del público
    agregado_l_usa_t = m2_usa_t + 5.5 + 32.7

    return {
        "ingreso_bruto_usd": 161377.0,
        "tasa_impuestos": 0.18,
        "costo_subsistencia": 0.42,
        "m0_billones": m0_usa_t,
        "agregado_l_billones": agregado_l_usa_t,
        "tipo_cambio_usd": 1.0,
    }
