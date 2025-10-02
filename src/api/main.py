from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al archivo HTML
html_path = os.path.join(current_dir, "templates", "heatmap_denuncias_lima.html")

@app.get("/")
async def root():
    """
    Sirve el archivo heatmap_denuncias_lima.html como respuesta principal.
    """
    return FileResponse(html_path)
