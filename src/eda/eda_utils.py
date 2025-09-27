"""Funciones auxiliares para EDA.
Agregar aquí funciones de perfilado, estadísticas descriptivas, visualizaciones, etc.
"""
from __future__ import annotations
from typing import Optional
import pandas as pd


def resumen_basico(df: pd.DataFrame, max_cols: int = 20) -> pd.DataFrame:
    """Devuelve estadísticas descriptivas básicas.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame de entrada.
    max_cols : int
        Límite de columnas a mostrar para evitar saturar salida.
    """
    subset = df.iloc[:, :max_cols]
    desc = subset.describe(include="all", datetime_is_numeric=True).T
    return desc
