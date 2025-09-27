"""Ejemplo de módulo de scraping.
Reemplazar con lógica real (requests, selenium, playwright, etc.).
"""
from typing import List, Dict


def obtener_items_demo() -> List[Dict]:
    """Devuelve datos mock para pruebas iniciales."""
    return [
        {"id": 1, "titulo": "Ejemplo 1", "precio": 10.5},
        {"id": 2, "titulo": "Ejemplo 2", "precio": 23.0},
    ]


if __name__ == "main":  # pragma: no cover
    print(obtener_items_demo())
