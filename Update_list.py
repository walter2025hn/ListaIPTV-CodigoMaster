def organizar_lista():
    # Nombre de tu archivo de lista
    archivo_lista = "Lista IPTV"
    
    # Estructura inicial de la lista
    cabecera = "#EXTM3U\n"
    
    # Diccionario para organizar categorías
    categorias = {
        "TV EN VIVO": [],
        "PELICULAS": [],
        "SERIES": []
    }

    # Ejemplo de cómo agregar contenido organizado
    # (Aquí es donde luego pondremos el bot que busca los links)
    categorias["TV EN VIVO"].append('#EXTINF:-1, Canal de Ejemplo\nhttp://link-del-canal.com')
    categorias["PELICULAS"].append('#EXTINF:-1, Película de Ejemplo\nhttp://link-de-la-peli.com')
    categorias["SERIES"].append('#EXTINF:-1, Serie de Ejemplo\nhttp://link-de-la-serie.com')

    with open(archivo_lista, "w", encoding="utf-8") as f:
        f.write(cabecera)
        
        for nombre_cat, contenido in categorias.items():
            f.write(f"\n# ---- {nombre_cat} ----\n")
            if contenido:
                f.write("\n".join(contenido) + "\n")
            else:
                f.write("# Próximamente...\n")
        
        f.write("\n# Última actualización automática realizada")

if __name__ == "__main__":
    organizar_lista()
