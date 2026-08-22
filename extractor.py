import re
from playwright.sync_api import sync_playwright

URL_TARGET = "https://famelack.com/tv"
ARCHIVO_SALIDA = "lista_famelack.m3u"

def extraer():
    enlaces = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Escuchar todas las peticiones de red para capturar m3u8 al vuelo
        page.on("request", lambda req: enlaces.add(req.url) if ".m3u8" in req.url else None)
        
        try:
            page.goto(URL_TARGET, wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"Aviso en carga: {e}")
            
        content = page.content()
        matches = re.findall(r'https?://[^\s\'"]+?\.m3u8[^\s\'"]*', content)
        for m in matches:
            enlaces.add(m)
            
        browser.close()
        
    return list(enlaces)

if __name__ == "__main__":
    links = extraer()
    print(f"Canales capturados: {len(links)}")
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for i, url in enumerate(links, start=1):
            f.write(f'#EXTINF:-1 tvg-id="famelack_{i}", Canal {i}\n{url}\n\n')
