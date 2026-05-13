import requests
from bs4 import BeautifulSoup

def obtener_peliculas_cuevana():
    url = "https://cuevana.st/peliculas"
    headers = {'User-Agent': 'Mozilla/5.0'}
    peliculas_lista = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Busca los contenedores de películas en el sitio
            items = soup.find_all('li', class_='xxx') # El bot busca la estructura del sitio
            
            for item in items:
                titulo = item.find('h2').text.strip() if item.find('h2') else "Película sin título"
                link_web = item.find('a')['href'] if item.find('a') else ""
                
                if link_web:
                    # Formato para tu lista IPTV
                    peliculas_lista.append(f"#EXTINF:-1, {titulo}\n{link_web}")
        
        return peliculas_lista
    except Exception as e:
        print(f"Error al conectar con Cuevana: {e}")
        return []

def organizar_y_guardar():
    archivo_lista = "Lista IPTV"
    nuevas_pelis = obtener_peliculas_cuevana()
    
    with open(archivo_lista, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("\n# ---- TV EN VIVO ----\n# Próximamente...\n")
        
        f.write("\n# ---- PELICULAS (CUEVANA) ----\n")
        if nuevas_pelis:
            f.write("\n".join(nuevas_pelis))
        else:
            f.write("# No se pudieron obtener películas hoy.\n")
            
        f.write("\n\n# ---- SERIES ----\n# Próximamente...\n")
        f.write("\n# Actualización automática de Código Master TV")

if __name__ == "__main__":
    organizar_y_guardar()
