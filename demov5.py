import networkx as nx
from lector import leer_entrada
from imprimir import imprimir_grafo
import logging

# ============================================================================
# VERSIÓN 1: Solo Jerarquías SIN Pesos
# ============================================================================

def version1_sin_pesos(G, alpha=0.85):
    """
    PageRank básico sobre jerarquías bidireccionales.
    Todas las relaciones valen igual.
    """
    # Crear grafo bidireccional
    G_bi = nx.DiGraph()
    G_bi.add_nodes_from(G.nodes(data=True))
    
    # Hacer bidireccionales las relaciones jerárquicas
    for u, v in G.edges():
        G_bi.add_edge(u, v)
        G_bi.add_edge(v, u)
    
    # PageRank sin pesos
    pr = nx.pagerank(G_bi, alpha=alpha)
    
    return pr


# ============================================================================
# VERSIÓN 2: Jerarquías CON Pesos a "Libros" (Nodos Hoja)
# ============================================================================

def version2_con_pesos_libros(G, peso_libro=2.0, alpha=0.85):
    """
    PageRank con mayor peso para nodos hoja (los "libros"/géneros finales).
    Los nodos intermedios (categorías) tienen peso 1.0.
    """
    # Identificar nodos hoja usando el nivel jerárquico
    niveles = [G.nodes[n].get('nivel', 0) for n in G.nodes()]
    max_nivel = max(niveles) if niveles else 0
    
    nodos_hoja = set()
    for nodo in G.nodes():
        if G.nodes[nodo].get('nivel', 0) == max_nivel:
            nodos_hoja.add(nodo)
    
    # Crear grafo bidireccional con pesos
    G_bi = nx.DiGraph()
    G_bi.add_nodes_from(G.nodes(data=True))
    
    for u, v in G.edges():
        # Si el destino es un libro (hoja), darle mayor peso
        if v in nodos_hoja:
            peso = peso_libro
        else:
            peso = 1.0
        
        G_bi.add_edge(u, v, weight=peso)
        G_bi.add_edge(v, u, weight=peso)
    
    # PageRank con pesos
    pr = nx.pagerank(G_bi, alpha=alpha, weight='weight')
    
    return pr


# ============================================================================
# VERSIÓN 3: Con Referencias Y Pesos
# ============================================================================

def version3_con_referencias_y_pesos(G, referencias, peso_libro=2.0, peso_referencia=3.0, alpha=0.85):
    """
    PageRank con:
    - Pesos a libros (nodos hoja)
    - Referencias cruzadas con su propio peso
    """
    # Identificar nodos hoja usando nivel máximo
    niveles = [G.nodes[n].get('nivel', 0) for n in G.nodes()]
    max_nivel = max(niveles) if niveles else 0
    
    nodos_hoja = set()
    for nodo in G.nodes():
        if G.nodes[nodo].get('nivel', 0) == max_nivel:
            nodos_hoja.add(nodo)
    
    # Crear grafo completo
    G_completo = nx.DiGraph()
    G_completo.add_nodes_from(G.nodes(data=True))
    
    # Añadir relaciones jerárquicas con pesos
    referencias_set = set(referencias)
    for u, v in G.edges():
        # Solo si no es una referencia
        if (u, v) not in referencias_set:
            peso = peso_libro if v in nodos_hoja else 1.0
            G_completo.add_edge(u, v, weight=peso)
            G_completo.add_edge(v, u, weight=peso)
    
    # Añadir referencias con su peso
    for u, v in referencias:
        G_completo.add_edge(u, v, weight=peso_referencia)
        G_completo.add_edge(v, u, weight=peso_referencia)
    
    # PageRank con pesos
    pr = nx.pagerank(G_completo, alpha=alpha, weight='weight')
    
    return pr


# ============================================================================
# IMPRIMIR RESULTADOS
# ============================================================================

def imprimir_arbol_con_pesos(G, pr, titulo):
    """
    Imprime el árbol con los valores de PageRank al lado de cada nodo
    """
    print(f"\n{'='*70}")
    print(f"{titulo}")
    print(f"{'='*70}\n")
    
    # Empezar por los nodos que tienen nivel 0 (raíz)
    raices_reales = [n for n, attr in G.nodes(data=True) if attr.get('nivel') == 0]
    
    for raiz in sorted(raices_reales):
        score = pr.get(raiz, 0)
        print(f"[{raiz}] {score:.6f}")
        _imprimir_recursivo_con_pesos(G, raiz, "", pr)


def _imprimir_recursivo_con_pesos(G, nodo_actual, prefijo, pr):
    """
    Función recursiva para imprimir árbol con pesos
    """
    nivel_actual = G.nodes[nodo_actual].get('nivel', 0)
    
    # Filtramos vecinos que tengan un nivel mayor al actual
    hijos = []
    for vecino in G.neighbors(nodo_actual):
        nivel_vecino = G.nodes[vecino].get('nivel', 0)
        if nivel_vecino > nivel_actual:
            hijos.append(vecino)
    
    hijos.sort()
    num_hijos = len(hijos)
    
    for i, hijo in enumerate(hijos):
        es_ultimo = (i == num_hijos - 1)
        conector = "└── " if es_ultimo else "├── "
        score = pr.get(hijo, 0)
        
        print(f"{prefijo}{conector}{hijo} {score:.6f}")
        
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
        _imprimir_recursivo_con_pesos(G, hijo, nuevo_prefijo, pr)


def tabla_comparativa_final(G, pr_v1, pr_v2, pr_v3):
    """
    Tabla comparativa única y completa de las tres versiones con análisis
    """
    print(f"\n{'='*90}")
    print("TABLA COMPARATIVA FINAL - TODAS LAS VERSIONES")
    print(f"{'='*90}")
    
    # Ordenar por V1 para mantener consistencia
    nodos_ordenados = sorted(pr_v1.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Nodo':<35} {'V1 (base)':<15} {'V2 (pesos)':<15} {'V3 (refs)':<15} {'ΔV2':<10} {'ΔV3':<10}")
    print("-"*90)
    
    for nodo, score_v1 in nodos_ordenados:
        score_v2 = pr_v2[nodo]
        score_v3 = pr_v3[nodo]
        diff_v2 = score_v2 - score_v1
        diff_v3 = score_v3 - score_v1
        
        print(f"{nodo:<35} {score_v1:<15.6f} {score_v2:<15.6f} {score_v3:<15.6f} {diff_v2:+<10.4f} {diff_v3:+<10.4f}")
    
   

# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

# LEER ENTRADA
G = leer_entrada("entrada.txt")

# Referencias entre géneros relacionados
referencias = [
    ("Historical mystery", "Detective mystery"),
    ("Mystery thriller", "Psychological thriller"),
]

# EJECUTAR LAS 3 VERSIONES
pr_v1 = version1_sin_pesos(G)
pr_v2 = version2_con_pesos_libros(G, peso_libro=2.0)
pr_v3 = version3_con_referencias_y_pesos(G, referencias, peso_libro=2.0, peso_referencia=3.0)

# MOSTRAR ÁRBOLES CON PESOS
imprimir_arbol_con_pesos(G, pr_v1, "VERSIÓN 1: Sin Pesos (Baseline)")
imprimir_arbol_con_pesos(G, pr_v2, "VERSIÓN 2: Con Pesos a Libros (2x)")
imprimir_arbol_con_pesos(G, pr_v3, "VERSIÓN 3: Con Referencias y Pesos (refs=3x, libros=2x)")

# TABLA COMPARATIVA FINAL
tabla_comparativa_final(G, pr_v1, pr_v2, pr_v3)
