from .mexico import PaisMexico
from .usa import PaisUSA

# Lista de objetos que ejecutará el sistema automáticamente
PAISES_ACTIVOS = [
    PaisMexico(),
    PaisUSA(),
]
