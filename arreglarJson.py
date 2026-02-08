import json

# Tus campos seleccionados
campos_deseados = {
    'average_rating',
    #'similar_books',
    'description',
    #'authors',
    'book_id',
    'ratings_count',
    'title',
    #'title_without_series'
}

data_simplificada = []


# Abrimos el original para leer línea a línea
with open('archivo.json', 'r', encoding='utf-8') as f:
    for linea in f:
        linea = linea.strip()
        if not linea:
            continue
            
        try:
            item = json.loads(linea)
            filtrado = {k: item[k] for k in campos_deseados if k in item}
            data_simplificada.append(filtrado)
            
        except json.JSONDecodeError:
            continue


with open('archivo_final_limpio.json', 'w', encoding='utf-8') as f:
    json.dump(data_simplificada, f, ensure_ascii=False, indent=4)
