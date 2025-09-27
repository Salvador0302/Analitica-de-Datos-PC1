"""Punto de entrada de la aplicación (Streamlit).
Ejecutar con: streamlit run src/main.py
"""
from src.app.layout import render_header
from src.data_collection.scraper_example import obtener_items_demo
from src.utils.logger import logger

try:
    import streamlit as st  # type: ignore
except ImportError:  # pragma: no cover
    st = None


def main():
    render_header()
    data = obtener_items_demo()
    logger.info("Datos de ejemplo cargados: %d registros", len(data))
    if st:
        st.subheader("Datos demo")
        st.dataframe(data)
    else:
        print(data)


if __name__ == "__main__":  # pragma: no cover
    main()
