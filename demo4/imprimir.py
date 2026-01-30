import networkx as nx
import logging

def _imprimir_arbol_recursivo(grafo, nodo_actual, pagerank_dict, prefijo="", es_ultimo=True):
    """Función interna recursiva para dar formato de árbol."""
    try:
        hijos = list(grafo.predecessors(nodo_actual))
    except nx.NetworkXError:
        hijos = []

    hijos_ordenados = sorted(hijos, key=lambda h: pagerank_dict.get(h, 0), reverse=True)
    num_hijos = len(hijos_ordenados)

    for i, hijo in enumerate(hijos_ordenados):
        es_el_ultimo_hijo = (i == num_hijos - 1)
        conector = "└── " if es_el_ultimo_hijo else "├── "
        prefijo_siguiente = prefijo + "    " if es_el_ultimo_hijo else prefijo + "│   "
        
        rank = pagerank_dict.get(hijo, 0)
        print(f"{prefijo}{conector}[{hijo}] (Rank: {rank:.5f})")
        
        _imprimir_arbol_recursivo(grafo, hijo, pagerank_dict, prefijo_siguiente, es_el_ultimo_hijo)

def imprime_grafo(grafo, pagerank_dict, titulo="RESULTADOS"):
    """Identifica las raíces e inicia la impresión jerárquica del grafo."""
    print(f"\n========== {titulo} ==========")
    nodos_raiz = [nodo for nodo in grafo.nodes() if grafo.out_degree(nodo) == 0]
    
    if not nodos_raiz:
        logging.error("No se detectaron nodos raíz (ciclo detectado o grafo vacío).")
        return

    for raiz in nodos_raiz:
        print(f"[{raiz}] (Rank: {pagerank_dict[raiz]:.5f})")
        _imprimir_arbol_recursivo(grafo, raiz, pagerank_dict)



def _imprimir_arbol_recursivo_invertido(grafo, nodo_actual, pagerank_dict, prefijo="", es_ultimo=True):
    """Función interna recursiva para dar formato de árbol (Padre -> Hijo)."""
    try:
        # Ahora buscamos sucesores (hijos) en lugar de predecesores
        hijos = list(grafo.successors(nodo_actual))
    except nx.NetworkXError:
        hijos = []

    # Ordenamos los hijos por PageRank
    hijos_ordenados = sorted(hijos, key=lambda h: pagerank_dict.get(h, 0), reverse=True)
    num_hijos = len(hijos_ordenados)

    for i, hijo in enumerate(hijos_ordenados):
        es_el_ultimo_hijo = (i == num_hijos - 1)
        conector = "└── " if es_el_ultimo_hijo else "├── "
        prefijo_siguiente = prefijo + "    " if es_el_ultimo_hijo else prefijo + "│   "
        
        rank = pagerank_dict.get(hijo, 0)
        print(f"{prefijo}{conector}[{hijo}] (Rank: {rank:.5f})")
        
        # Llamada recursiva hacia los hijos
        _imprimir_arbol_recursivo_invertido(grafo, hijo, pagerank_dict, prefijo_siguiente, es_el_ultimo_hijo)

def imprime_grafo_invertido(grafo, pagerank_dict, titulo="RESULTADOS"):
    """Identifica las raíces (in_degree=0) e inicia la impresión jerárquica."""
    print(f"\n========== {titulo} ==========")
    
    # La raíz es el nodo que no tiene flechas entrando (in_degree == 0)
    nodos_raiz = [nodo for nodo in grafo.nodes() if grafo.in_degree(nodo) == 0]
    
    if not nodos_raiz:
        # Si no hay nodos con in_degree 0 y el grafo no está vacío, hay un ciclo
        if grafo.number_of_nodes() > 0:
            logging.error("No se detectaron nodos raíz (posible ciclo detectado).")
        return

    for raiz in nodos_raiz:
        print(f"[{raiz}] (Rank: {pagerank_dict.get(raiz, 0):.5f})")
        _imprimir_arbol_recursivo_invertido(grafo, raiz, pagerank_dict)