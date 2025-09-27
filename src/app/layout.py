"""Componentes de layout para la app (Streamlit u otro framework)."""

try:
    import streamlit as st  # type: ignore
except ImportError:  # pragma: no cover
    st = None  # Fallback mínimo


def render_header(title: str = "Analítica de Datos"):
    if st:
        st.title(title)
    else:
        print(f"== {title} ==")
