import networkx as nx

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
        print("No se detectaron nodos raíz (ciclo detectado o grafo vacío).")
        return

    for raiz in nodos_raiz:
        print(f"[{raiz}] (Rank: {pagerank_dict[raiz]:.5f})")
        _imprimir_arbol_recursivo(grafo, raiz, pagerank_dict)