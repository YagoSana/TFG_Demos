# Demo para comprender el uso de networkX
import networkx as nx

#funcion recursiva para imprimir el arbol de nodos
def imprimir_arbol_recursivo(grafo, nodo_actual, pagerank_dict, prefijo="", es_ultimo=True):
    
    # Obtener predecesores (hijos del árbol invertido)
    try:
        hijos = list(grafo.predecessors(nodo_actual))
    except nx.NetworkXError:
        hijos = []

    # Ordenar los hijos por su valor de PageRank (descendente)
    hijos_ordenados = sorted(hijos, key=lambda h: pagerank_dict.get(h, 0), reverse=True)

    # Iterar e imprimir recursivamente
    num_hijos = len(hijos_ordenados)
    for i, hijo in enumerate(hijos_ordenados):
        es_el_ultimo_hijo = (i == num_hijos - 1)
        
        # Dibuja las líneas del árbol como el comando "tree"
        conector = "└── " if es_el_ultimo_hijo else "├── "
        prefijo_siguiente = prefijo + "    " if es_el_ultimo_hijo else prefijo + "│   "
        
        # Obtener el rango para imprimirlo
        rank = pagerank_dict.get(hijo, 0)
        print(f"{prefijo}{conector}[{hijo}] (Rank: {rank:.5f})")
        
        # Llamada recursiva para los nietos
        imprimir_arbol_recursivo(grafo, hijo, pagerank_dict, prefijo_siguiente, es_el_ultimo_hijo)

#COMIENZO DEL PROGRAMA PRINCIPAL
# Crear un grafo dirigido
G = nx.DiGraph()

# NetworkX añade nodos automaticamente al crear aristas
# Leer de un documento de texto de entrada, los nodos del grafo
# Los 2 primeros valores son el num de nodos y aristas que ignoraremos, están en el fichero por similitud a otros formatos (domjudge)

try:
    nombre_archivo = "entrada.txt"
    with open(nombre_archivo, 'r') as f:
        #lee la primera linea que no es necesario en NetworkX para construir el grafo
        primera_linea = f.readline()

        for linea in f:
            nueva_linea = linea.strip()

            if nueva_linea: #si la linea tiene contenido
                valores = nueva_linea.split()
                #insertar los valores como aristas invertidas para dar importancia "hacia arriba"
                if len(valores) >= 2:
                    ini = int(valores[0])
                    fin = int(valores[1])
                    G.add_edge(fin, ini)
except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo '{nombre_archivo}'.")
    sys.exit(1) # Salir si el archivo no existe

print("Nodos del grafo:")
print(G.nodes())
print("Aristas del grafo:")
print(G.edges())

# Aplicar algoritmo PageRank
pagerank1 = nx.pagerank(G, alpha=0.85) #factor de amortiguamiento típico es 0.85
# Calcular PageRank con parámetros de importancia a nodos iniciales
# Nstart es un diccionario con valores iniciales para cada nodo

# Identificar nodos "hoja" (donde empieza el flujo del grafo invertido)
# Los nodos hoja son los que tienen grado 0 de entrada (nadie les apunta) <- REVISAR
nodos_hoja = [n for n in G.nodes() if G.in_degree(n) == 0]

# Asignar un peso inicial igual para todos los nodos hoja
diccionario_pesos = {nodo: 0 for nodo in G.nodes()} # Inicializar todos a 0
for nodo in nodos_hoja:
    diccionario_pesos[nodo] = 100 # Valor alto inventado 

# Probar con nstart y personalization para mostrar que nstart solo afecta la inicialización y que con muchas iteraciones (pagerank hace unas cuantas) se diluye el efecto
pagerank2 = nx.pagerank(G, alpha=0.85, nstart=diccionario_pesos)
pagerank3 = nx.pagerank(G, alpha=0.85, personalization=diccionario_pesos)
print("PageRank de los nodos:")

# Ordenar los nodos por su valor de PageRank en forma de árbol descendente
# Como suponemos conexo el grafo completo y representa un arbol de directorio, solo debe haber una raiz
nodos_raiz = [nodo for nodo in G.nodes() if G.out_degree(nodo) == 0]

print("Imprimir arbol normal:")
if not nodos_raiz:
    print("Advertencia: No se encontró un nodo raíz claro (out_degree == 0)")
else:
    # Solo hay una raiz pero por si hubiera casos excepcionales o errores, lo ponemos en un foreach que solo itera 1 vez
    for raiz in nodos_raiz:
        rank_raiz = pagerank1.get(raiz, 0)
        print(f"[{raiz}] (Rank: {rank_raiz:.5f})") 
        # Llamar a la función recursiva para sus hijos
        imprimir_arbol_recursivo(G, raiz, pagerank1, prefijo="", es_ultimo=True)
    print() #\n
    print("Imprimir arbol con nstart:")
    for raiz in nodos_raiz:
        rank_raiz = pagerank2.get(raiz, 0)
        print(f"[{raiz}] (Rank: {rank_raiz:.5f})") 
        # Llamar a la función recursiva para sus hijos
        imprimir_arbol_recursivo(G, raiz, pagerank2, prefijo="", es_ultimo=True)
    # Añadir una línea en blanco para separar la salida en terminal
    print()
    print("Imprimir arbol con personalization:")
    for raiz in nodos_raiz:
        rank_raiz = pagerank3.get(raiz, 0)
        print(f"[{raiz}] (Rank: {rank_raiz:.5f})") 
        # Llamar a la función recursiva para sus hijos
        imprimir_arbol_recursivo(G, raiz, pagerank3, prefijo="", es_ultimo=True)
