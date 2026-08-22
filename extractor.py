import re
import json
import requests
from bs4 import BeautifulSoup

URL_TARGET = "https://famelack.com/tv"
ARCHIVO_SALIDA = "lista_famelack.m3u"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://famelack.com/"
}

def extraer_canales():
    print(f"Obteniendo datos de {URL_TARGET}...")
    try:
        session = requests.Session()
        res = session.get(URL_TARGET, headers=headers, timeout=20)
        res.raise_for_status()
        html = res.text
    except Exception as e:
        print(f"Error al conectar con la página: {e}")
        return []

    enlaces = set()

    # 1. Búsqueda de URLs m3u8 con Expresiones Regulares en todo el HTML/JS
    patron_m3u8 = r'https?://[^\s\'"]+?\.m3u8[^\s\'"]*'
    coincidencias = re.findall(patron_m3u8, html)
    for link in coincidencias:
        enlaces.add(link)

    # 2. Análisis del DOM con BeautifulSoup (Buscando elementos de video, iframe y fuentes)
    soup = BeautifulSoup(html, "html.parser")
    
    # Buscar en etiquetas iframe, embed, video, source
    for tag in soup.find_all(['iframe', 'source', 'video', 'embed']):
        src = tag.get('src') or tag.get('data-src')
        if src:
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                src = 'https://famelack.com' + src
            
            if '.m3u8' in src or 'stream' in src:
                enlaces.add(src)

    # 3. Extraer scripts inline para buscar configuraciones JSON cargadas en variables
    scripts = soup.find_all('script')
    for s in scripts:
        if s.string:
            # Buscar cualquier URL que termine en m3u8 dentro de bloques de JavaScript
            found_urls = re.findall(r'["\'](https?://[^\s\'"]+\.m3u8[^\s\'"]*)["\']', s.string)
            for u in found_urls:
                enlaces.add(u)

    return list(enlaces)

def generar_m3u(canales):
    if not canales:
        print("No se encontraron enlaces para guardar.")
        return False
        
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n\n")
        for i, url in enumerate(canales, start=1):
            f.write(f'#EXTINF:-1 tvg-id="famelack_{i}" group-title="Famelack", Canal {i}\n')
            f.write(f"{url}\n\n")
    return True

if __name__ == "__main__":
    links = extraer_canales()
    print(f"Resultados encontrados: {len(links)}")
    if generar_m3u(links):
        print(f"Archivo '{ARCHIVO_SALIDA}' creado con éxito.")
