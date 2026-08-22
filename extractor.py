import re
import requests
from bs4 import BeautifulSoup

# URL de la página web que quieres rastrear
URL_ORIGEN = "https://famelack.com/tv"  # Cambia esta URL
ARCHIVO_SALIDA = "lista_canales.m3u"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def extraer_enlaces():
    try:
        response = requests.get(URL_ORIGEN, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al conectar con la página: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Opción A: Buscar todas las etiquetas <a> con href
    enlaces = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Filtra por enlaces .m3u8 o streamings (ajusta la regla según la web)
        if ".m3u8" in href or "stream" in href:
            enlaces.append(href)

    # Opción B: Buscar directamente enlaces .m3u8 con Expresiones Regulares en todo el código HTML
    enlaces_regex = re.findall(r'https?://[^\s\'"]+\.m3u8', response.text)

    # Combinar y quitar duplicados
    todos_los_enlaces = list(set(enlaces + enlaces_regex))
    return todos_los_enlaces


def guardar_lista_m3u(enlaces):
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for i, url in enumerate(enlaces, start=1):
            f.write(f"#EXTINF:-1 tvg-id=\"canal{i}\", Canal {i}\n")
            f.write(f"{url}\n\n")


if __name__ == "__main__":
    links = extraer_enlaces()
    print(f"Se encontraron {len(links)} enlaces.")
    if links:
        guardar_lista_m3u(links)
        print(f"Lista guardada en {ARCHIVO_SALIDA}")
