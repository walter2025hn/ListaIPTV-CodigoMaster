import re
import time
from playwright.sync_api import sync_playwright

URL_TARGET = "https://famelack.com/tv"
ARCHIVO_SALIDA = "lista_famelack.m3u"

def extraer():
    enlaces = set()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Emular un navegador de escritorio completo
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        # 1. Monitorear las peticiones de red en tiempo real
        def manejar_peticion(request):
            url = request.url
            if any(ext in url for ext in [".m3u8", ".mpd", "/live/", "/hls/", "stream"]):
                # Filtrar archivos js/css/png que puedan coincidir
                if not any(url.endswith(ext) for ext in [".js", ".css", ".png", ".jpg"]):
                    enlaces.add(url)

        page.on("request", manejar_peticion)

        print(f"Cargando {URL_TARGET}...")
        try:
            page.goto(URL_TARGET, wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)  # Dar tiempo a que los reproductores e iframes carguen

            # 2. Extraer enlaces iframe embedded
            for frame in page.frames:
                try:
                    src = frame.url
                    if src and src != "about:blank":
                        enlaces.add(src)
                except Exception:
                    pass

            # 3. Buscar enlaces de transmisión dentro del código HTML generado
            content = page.content()
            matches_m3u8 = re.findall(r'https?://[^\s\'"]+?\.m3u8[^\s\'"]*', content)
            matches_embed = re.findall(r'https?://[^\s\'"]+?/live/[^\s\'"]*', content)
            
            for m in matches_m3u8 + matches_embed:
                enlaces.add(m)

        except Exception as e:
            print(f"Aviso durante el rastreo: {e}")

        browser.close()

    return list(enlaces)

if __name__ == "__main__":
    links = extraer()
    print(f"Total de señales/enlaces capturados: {len(links)}")

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n\n")

        if links:
            for i, url in enumerate(links, start=1):
                f.write(f'#EXTINF:-1 tvg-id="famelack_{i}" group-title="Famelack", Canal Famelack {i}\n')
                f.write(f"{url}\n\n")
        else:
            # Respaldo en caso de que la transmisión principal use iframe directo
            f.write('#EXTINF:-1 tvg-id="famelack_main" group-title="Famelack", Famelack TV Directo\n')
            f.write("https://famelack.com/tv\n\n")
