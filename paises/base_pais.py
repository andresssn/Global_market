from abc import ABC, abstractmethod


class PaisBase(ABC):

  def __init__(self, nombre: str):
    self.nombre = nombre

  @abstractmethod
  def obtener_datos(self) -> dict:
    """
        Cada país implementa este método como quiera (API, scraping o fijo),
        pero SIEMPRE debe regresar un diccionario con estas 6 llaves exactas:
        - ingreso_bruto_usd (float)
        - tasa_impuestos (float)
        - costo_subsistencia (float)
        - m0_billones (float)
        - agregado_l_billones (float)
        - tipo_cambio_usd (float)
        """
    pass

  def evaluar_riesgo(self, precio_oro_usd: float) -> dict:
    datos = self.obtener_datos()

    multiplo_l_m0 = datos["agregado_l_billones"] / datos["m0_billones"]
    flujo_libre_usd = (
        datos["ingreso_bruto_usd"]
        * (1 - datos["tasa_impuestos"])
        * (1 - datos["costo_subsistencia"])
    )
    oz_libres = flujo_libre_usd / precio_oro_usd
    producto_libre = oz_libres * multiplo_l_m0

    return {
        "Pais": self.nombre,
        "Oro_USD": round(precio_oro_usd, 2),
        "Tipo_Cambio": round(datos["tipo_cambio_usd"], 2),
        "Multiplo_L_M0": round(multiplo_l_m0, 2),
        "Oz_Libres_Anio": round(oz_libres, 2),
        "Producto_Libre": round(producto_libre, 2),
    }
