import logging

def imprimir_grafo(G, titulo):
    print(f"\n========== {titulo} ==========")
    
    # Empezar por los nodos que tienen nivel 0 (raíz)
    raices_reales = [n for n, attr in G.nodes(data=True) if attr.get('nivel') == 0]
    
    # Usar un for por si hubiera múltiples raíces pero deberia haber una solo
    for raiz in sorted(raices_reales):
        print(f"[{raiz}]")
        _imprimir_recursivo_tree(G, raiz, "")

def _imprimir_recursivo_tree(G, nodo_actual, prefijo):
    # Obtenemos el nivel del nodo actual para solo ir a niveles superiores
    nivel_actual = G.nodes[nodo_actual].get('nivel', 0)
    
    # Filtramos vecinos que tengan un nivel mayor al actual (para asegurar que bajamos en el árbol)
    hijos = []
    for vecino in G.neighbors(nodo_actual):
        nivel_vecino = G.nodes[vecino].get('nivel', 0)
        if nivel_vecino > nivel_actual:
            hijos.append(vecino)
    
    hijos.sort() # Orden alfabético para los hermanos
    num_hijos = len(hijos)
    
    for i, hijo in enumerate(hijos):
        es_ultimo = (i == num_hijos - 1)
        conector = "└── " if es_ultimo else "├── "
        
        print(f"{prefijo}{conector}{hijo}")
        
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
        _imprimir_recursivo_tree(G, hijo, nuevo_prefijo)