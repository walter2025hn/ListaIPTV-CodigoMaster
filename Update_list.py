import requests
from bs4 import BeautifulSoup

def obtener_peliculas_cuevana():
    url = "https://cuevana.st/peliculas"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    peliculas_lista = []
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos todos los enlaces que estén dentro de la sección de películas
            # Cuevana suele usar etiquetas 'a' con títulos dentro de figuras o divs
            for item in soup.find_all('a'):
                titulo = item.find('h2') or item.find('span')
                link = item.get('href', '')
                
                if titulo and '/pelicula/' in link:
                    nombre = titulo.text.strip()
                    # Si el link es relativo, le ponemos el dominio
                    url_completa = link if link.startswith('http') else f"https://cuevana.st{link}"
                    peliculas_lista.append(f"#EXTINF:-1, {nombre}\n{url_completa}")
        
        # Eliminamos duplicados
        return list(set(peliculas_lista))
    except Exception as e:
        print(f"Error: {e}")
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
            f.write("# No se encontraron películas. Revisando conexión...\n")
            
        f.write("\n\n# ---- SERIES ----\n# Próximamente...\n")
        f.write("\n# Actualización automática de Código Master TV")

if __name__ == "__main__":
    organizar_y_guardar()
