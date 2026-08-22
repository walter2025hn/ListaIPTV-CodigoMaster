import re
import requests
from bs4 import BeautifulSoup

URL_TARGET = "https://famelack.com/tv"
ARCHIVO_SALIDA = "lista_famelack.m3u"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extraer_canales():
    print(f"Conectando a {URL_TARGET}...")
    try:
        res = requests.get(URL_TARGET, headers=headers, timeout=20)
        res.raise_for_status()
    except Exception as e:
        print(f"Error al cargar la página: {e}")
        return []

    html_content = res.text
    canales = []

    # 1. Buscar enlaces m3u8 directos en el HTML / scripts
    m3u8_matches = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', html_content)
    for link in m3u8_matches:
        canales.append(link)

    # 2. Buscar enlaces de reproductores embebidos (iframe / embed / src)
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup.find_all(['iframe', 'source', 'video']):
        src = tag.get('src')
        if src and ('m3u8' in src or 'stream' in src):
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                src = 'https://famelack.com' + src
            canales.append(src)

    # Eliminar duplicados manteniendo el orden
    canales_unicos = list(dict.fromkeys(canales))
    return canales_unicos

def generar_m3u(enlaces):
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n\n")
        
        for i, url in enumerate(enlaces, start=1):
            f.write(f'#EXTINF:-1 tvg-id="famelack_{i}" group-title="Famelack", Canal {i}\n')
            f.write(f"{url}\n\n")

if __name__ == "__main__":
    links = extraer_canales()
    print(f"Se encontraron {len(links)} transmisiones.")
    if links:
        generar_m3u(links)
        print(f"Archivo '{ARCHIVO_SALIDA}' generado correctamente.")
    else:
        print("No se encontraron enlaces directos m3u8.")
