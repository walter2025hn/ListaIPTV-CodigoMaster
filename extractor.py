iimport re
from curl_cffi import requests

URL_TARGET = "https://famelack.com/tv"
ARCHIVO_SALIDA = "lista_famelack.m3u"

def extraer_canales():
    print(f"Conectando a {URL_TARGET} emulando Chrome...")
    try:
        # impersonate="chrome120" salta las protecciones TLS de Cloudflare
        session = requests.Session()
        res = session.get(URL_TARGET, impersonate="chrome120", timeout=25)
        html = res.text
        print(f"Respuesta recibida. Tamaño HTML: {len(html)} bytes")
    except Exception as e:
        print(f"Error en la petición: {e}")
        return []

    enlaces = set()

    # Extraer URLs .m3u8 usando expresiones regulares
    patron_m3u8 = r'https?://[^\s\'"]+?\.m3u8[^\s\'"]*'
    matches = re.findall(patron_m3u8, html)
    for m in matches:
        enlaces.add(m)

    # Extraer URLs de streams/iframes
    patron_stream = r'https?://[^\s\'"]+?/live/[^\s\'"]+'
    matches_stream = re.findall(patron_stream, html)
    for m in matches_stream:
        enlaces.add(m)

    return list(enlaces)

def generar_m3u(canales):
    # Generar el archivo siempre para forzar el commit en GitHub
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n\n")
        if canales:
            for i, url in enumerate(canales, start=1):
                f.write(f'#EXTINF:-1 tvg-id="famelack_{i}" group-title="Famelack", Canal {i}\n')
                f.write(f"{url}\n\n")
        else:
            # Entrada por defecto en caso de no hallar fuentes m3u8 directas
            f.write('#EXTINF:-1 tvg-id="famelack_web" group-title="Famelack", Famelack TV Web\n')
            f.write("https://famelack.com/tv\n")

if __name__ == "__main__":
    links = extraer_canales()
    print(f"Enlaces encontrados: {len(links)}")
    generar_m3u(links)
    print(f"Archivo '{ARCHIVO_SALIDA}' guardado con éxito.")
