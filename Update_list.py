def cargar_manuales():
    enlaces_manuales = []
    try:
        with open("manuales.txt", "r", encoding="utf-8") as f:
            for linea in f:
                if "," in linea:
                    nombre, url = linea.strip().split(",")
                    enlaces_manuales.append(f"#EXTINF:-1, {nombre}\n{url}")
    except FileNotFoundError:
        print("No hay archivo manuales.txt")
    return enlaces_manuales

# En tu función de guardar, simplemente sumas las listas:
# lista_final = enlaces_manuales + peliculas_cuevana
