import requests
import re

# 1. LISTA DE FUENTES (Aquí es donde el bot busca más contenido)
# Puedes agregar canales de YouTube, repositorios de GitHub o sitios de m3u8
FUENTES_EXTRA = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hn.m3u", # Canales de Honduras
    "https://lista-de-ejemplo.com/peliculas.m3u8"
]

def verificar_link(url):
    """Revisa si el link responde con un video real."""
    try:
        # Probamos una conexión rápida de 5 segundos
        r = requests.get(url, timeout=5, stream=True)
        return r.status_code == 200
    except:
        return False

def extraer_manuales():
    """Extrae tus links de manuales.txt para procesarlos."""
    enlaces_validados = []
    try:
        with open("manuales.txt", "r", encoding="utf-8") as f:
            for linea in f:
                if "," in linea:
                    nombre, url = linea.strip().split(",")
                    print(f"Chequeando: {nombre}...")
                    if verificar_link(url):
                        enlaces_validados.append(f'#EXTINF:-1 tvg-logo="" group-title="MIS CANALES ✅", {nombre}\n{url}')
                    else:
                        # Si está caído, le cambia el nombre para avisarte en Televizo
                        enlaces_validados.append(f'#EXTINF:-1 tvg-logo="" group-title="LINKS CAÍDOS ❌", {nombre} (CAÍDO)\n{url}')
    except:
        print("No se encontró manuales.txt")
    return enlaces_validados

def buscar_nuevos_links():
    """Busca links .m3u8 en las fuentes extra para darte más contenido."""
    nuevos = []
    for fuente in FUENTES_EXTRA:
        try:
            res = requests.get(fuente, timeout=10)
            # Buscamos patrones de links de video
            links = re.findall(r'(https?://[^\s]+\.(?:m3u8|mp4|ts))', res.text)
            for link in links[:10]: # Solo traemos los primeros 10 para no saturar
                nuevos.append(f'#EXTINF:-1 tvg-logo="" group-title="BOT: DESCUBRIMIENTOS", Canal Nuevo\n{link}')
        except:
            continue
    return nuevos

def generar_lista_final():
    manuales = extraer_manuales()
    descubrimientos = buscar_nuevos_links()
    
    with open("Lista IPTV", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("\n# ---- TUS CANALES VERIFICADOS ----\n")
        f.write("\n".join(manuales) + "\n")
        
        f.write("\n# ---- NUEVO CONTENIDO ENCONTRADO ----\n")
        f.write("\n".join(descubrimientos) + "\n")
        
        f.write("\n# Actualizado por Código Master TV Bot")

if __name__ == "__main__":
    generar_lista_final()
