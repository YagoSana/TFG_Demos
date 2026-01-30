# Demo para comprender el uso de networkX
import networkx as nx
import sys

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


# ============================
#   COMIENZO DEL PROGRAMA
# ============================

# Crear un grafo dirigido
G = nx.DiGraph()

# Leer de un documento de texto de entrada
try:
    nombre_archivo = "entrada.txt"
    with open(nombre_archivo, 'r') as f:
        # lee la primera linea (nodos y aristas, no necesaria)
        primera_linea = f.readline()

        for linea in f:
            nueva_linea = linea.strip()
            if nueva_linea: 
                valores = nueva_linea.split()
                if len(valores) >= 2:
                    ini = int(valores[0])
                    fin = int(valores[1])
                    # aristas invertidas (hijo -> padre)
                    G.add_edge(fin, ini)

except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo '{nombre_archivo}'.")
    sys.exit(1)

print("Nodos del grafo:")
print(G.nodes())
print("Aristas del grafo:")
print(G.edges())

# ==========================================
#   ASIGNACIÓN DE ETIQUETAS A LOS NODOS
# ==========================================

#asignar una etiqueta fija según alguna condición
# (Cambia la lógica por la que tú quieras)
for n in G.nodes():
    if n % 2 == 0:   # ejemplo: los nodos pares son importantes
        G.nodes[n]["etiqueta"] = "importante"
    else:
        G.nodes[n]["etiqueta"] = "normal"

# ============================
#   PAGE RANK NORMAL
# ============================
pagerank1 = nx.pagerank(G, alpha=0.85)


# ============================
#   DETECTAR NODOS HOJA
# ============================
nodos_hoja = [n for n in G.nodes() if G.in_degree(n) == 0]


# ============================
#   PERSONALIZATION SUAVIZADA 
# ============================

N = len(G.nodes())

# vector uniforme U
uniforme = {n: 1/N for n in G.nodes()}

# vector reforzado para nodos hoja H
refuerzo_hojas = {
    n: (1/len(nodos_hoja)) if n in nodos_hoja else 0 
    for n in G.nodes()
}

# peso extra que mantendrá memoria de ser hoja (ajustable)
extra = 0.3  

personalization_suave = {
    n: (1 - extra) * uniforme[n] + extra * refuerzo_hojas[n]
    for n in G.nodes()
}

pagerank_personalizado = nx.pagerank(G, alpha=0.85, personalization=personalization_suave)

# ============================
#  PERSONALIZATION SUAVIZADA BASADA EN ETIQUETAS
# ============================

# ejemplo: queremos reforzar nodos con etiqueta "importante"
VALOR_ETIQUETA = "importante"
NOMBRE_CAMPO = "etiqueta"   # el atributo del nodo que miramos

# obtener nodos que tienen esa etiqueta
nodos_objetivo = [
    n for n in G.nodes() 
    if NOMBRE_CAMPO in G.nodes[n] and G.nodes[n][NOMBRE_CAMPO] == VALOR_ETIQUETA
]

if not nodos_objetivo:
    print("Advertencia: no hay nodos con la etiqueta objetivo. Se usará PageRank normal.")
    nodos_objetivo = []


# 1) vector uniforme U
N = len(G.nodes())
uniforme = {n: 1/N for n in G.nodes()}

# 2) vector reforzado R para los nodos con etiqueta objetivo
if nodos_objetivo:
    refuerzo_etiqueta = {
        n: (1/len(nodos_objetivo)) if n in nodos_objetivo else 0
        for n in G.nodes()
    }
else:
    # Si no hay nodos objetivo, que el refuerzo sea cero
    refuerzo_etiqueta = {n: 0 for n in G.nodes()}


# 3) porcentaje de refuerzo (ajusta este valor)
extra = 0.3

# 4) combinación suave
personalization_suave = {
    n: (1 - extra) * uniforme[n] + extra * refuerzo_etiqueta[n]
    for n in G.nodes()
}

# 5) ejecutar PageRank personalizado
pagerank_personalizado_etiqueta = nx.pagerank(G, alpha=0.85, personalization=personalization_suave)

# ============================
#   Calcular PageRank con nstart
# ============================
# nstart se usa solo como vector inicial, NO afecta al resultado final
dicc_nstart = {n: 0 for n in G.nodes()}
for h in nodos_hoja:
    dicc_nstart[h] = 100

pagerank_nstart = nx.pagerank(G, alpha=0.85, nstart=dicc_nstart)


# ============================
#   IMPRIMIR ÁRBOLES
# ============================

nodos_raiz = [nodo for nodo in G.nodes() if G.out_degree(nodo) == 0]

print("\n========== PAGE RANK NORMAL ==========")
if nodos_raiz:
    for raiz in nodos_raiz:
        print(f"[{raiz}] (Rank: {pagerank1[raiz]:.5f})")
        imprimir_arbol_recursivo(G, raiz, pagerank1)

print("\n========== PAGE RANK CON nstart ==========")
if nodos_raiz:
    for raiz in nodos_raiz:
        print(f"[{raiz}] (Rank: {pagerank_nstart[raiz]:.5f})")
        imprimir_arbol_recursivo(G, raiz, pagerank_nstart)

print("\n========== PAGE RANK CON PERSONALIZATION SUAVIZADA ==========")
if nodos_raiz:
    for raiz in nodos_raiz:
        print(f"[{raiz}] (Rank: {pagerank_personalizado[raiz]:.5f})")
        imprimir_arbol_recursivo(G, raiz, pagerank_personalizado)

print("\n========== PAGE RANK CON PERSONALIZATION SUAVIZADA ETIQUETA ==========")
if nodos_raiz:
    for raiz in nodos_raiz:
        print(f"[{raiz}] (Rank: {pagerank_personalizado[raiz]:.5f})")
        imprimir_arbol_recursivo(G, raiz, pagerank_personalizado_etiqueta)
