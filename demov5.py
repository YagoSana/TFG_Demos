import networkx as nx
from lector import leer_entrada
from imprimir import imprimir_arbol_con_pesos, tabla_comparativa_final
from generaHTML import exportar_html
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

exportar_html(G, pr_v1, pr_v2, pr_v3, "index.html")