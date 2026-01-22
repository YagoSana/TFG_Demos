import networkx as nx
from lector import leer_entrada
from imprimir import imprime_grafo, imprime_grafo_invertido
from validador import esGrafoValido
import logging


# ============================================================================
# PageRank en Referencias Bidireccionales
# ============================================================================

def fase1_pagerank_referencias(G, referencias_usuario, alpha=0.85):
    
    # Obtener todos los nodos que participan en referencias
    nodos_con_referencias = set()
    for u, v in referencias_usuario:
        nodos_con_referencias.add(u)
        nodos_con_referencias.add(v)
    
    # Crear grafo BIDIRECCIONAL de referencias
    G_referencias = nx.DiGraph()
    G_referencias.add_nodes_from(nodos_con_referencias)
    
    # Hacer referencias bidireccionales
    for u, v in referencias_usuario:
        G_referencias.add_edge(u, v)
        G_referencias.add_edge(v, u)  # BIDIRECCIONAL
    
    # Calcular PageRank en referencias
    if len(referencias_usuario) > 0:
        pr_referencias = nx.pagerank(G_referencias, alpha=alpha)
    else:
        # Si no hay referencias, distribución uniforme
        pr_referencias = {n: 1.0/len(nodos_con_referencias) for n in nodos_con_referencias}
    
    return pr_referencias, nodos_con_referencias


# ============================================================================
# PageRank en Árbol Completo Bidireccional
# ============================================================================

def fase2_pagerank_arbol_completo(G, referencias_usuario, nodos_con_referencias, pr_referencias, 
                                  peso_jerarquico=1.0, peso_referencia=1.0, usar_pesos=False, alpha=0.85):
    
    # Crear grafo bidireccional con TODAS las relaciones
    G_completo = nx.DiGraph()
    G_completo.add_nodes_from(G.nodes())
    
    # Copiar atributos de nodos
    for n in G.nodes():
        G_completo.nodes[n].update(G.nodes[n])
    
    # Primero añadir relaciones jerárquicas (del grafo original sin referencias)
    # Identificar cuáles son las referencias del usuario
    referencias_set = set(referencias_usuario)
    
    for u, v in G.edges():
        # Si NO es una referencia del usuario, es jerárquica
        if (u, v) not in referencias_set:
            G_completo.add_edge(u, v)
            G_completo.add_edge(v, u)  # BIDIRECCIONAL
            
            if usar_pesos:
                G_completo.edges[u, v]['weight'] = peso_jerarquico
                G_completo.edges[v, u]['weight'] = peso_jerarquico
    
    # Ahora añadir las referencias del usuario (bidireccionales)
    for u, v in referencias_usuario:
        G_completo.add_edge(u, v)
        G_completo.add_edge(v, u)  # BIDIRECCIONAL
        
        if usar_pesos:
            G_completo.edges[u, v]['weight'] = peso_referencia
            G_completo.edges[v, u]['weight'] = peso_referencia
    
    # Crear personalización usando resultados de Fase 1
    personalization = {}
    N = len(G_completo.nodes())
    for n in G_completo.nodes():
        if n in nodos_con_referencias:
            # Nodos con referencias usan su valor de Fase 1
            personalization[n] = pr_referencias.get(n, 1.0/N)
        else:
            # Nodos sin referencias usan distribución uniforme
            personalization[n] = 1.0 / N
    
    # Normalizar personalización
    total_pers = sum(personalization.values())
    personalization = {n: v/total_pers for n, v in personalization.items()}
    
    # Calcular PageRank final
    if usar_pesos:
        pr_final = nx.pagerank(G_completo, alpha=alpha, personalization=personalization, weight='weight')
    else:
        pr_final = nx.pagerank(G_completo, alpha=alpha, personalization=personalization)
    
    return pr_final


# ============================================================================
# ALGORITMO COMPLETO
# ============================================================================

def algoritmo_dos_fases_completo(G, referencias_usuario, alpha=0.85):
    
    
    # PageRank en referencias bidireccionales
    pr_referencias, nodos_con_referencias = fase1_pagerank_referencias(G, referencias_usuario, alpha)
    
    # PageRank en árbol completo - 3 variantes
    
    # Variante 1: SIN PESOS (todas las relaciones valen igual)
    pr_sin_pesos = fase2_pagerank_arbol_completo(
        G, referencias_usuario, nodos_con_referencias, pr_referencias,
        peso_jerarquico=1.0,
        peso_referencia=1.0,
        usar_pesos=False,
        alpha=alpha
    )
    
    # Variante 2: CON PESOS - Referencias 2x más importantes
    pr_peso_referencias = fase2_pagerank_arbol_completo(
        G, referencias_usuario, nodos_con_referencias, pr_referencias,
        peso_jerarquico=1.0,
        peso_referencia=2.0,
        usar_pesos=True,
        alpha=alpha
    )
    
    # Variante 3: CON PESOS - Jerarquía 2x más importante
    pr_peso_jerarquia = fase2_pagerank_arbol_completo(
        G, referencias_usuario, nodos_con_referencias, pr_referencias,
        peso_jerarquico=2.0,
        peso_referencia=1.0,
        usar_pesos=True,
        alpha=alpha
    )
    
    # Variantes adicionales para experimentación
    pr_ref_5x = fase2_pagerank_arbol_completo(
        G, referencias_usuario, nodos_con_referencias, pr_referencias,
        peso_jerarquico=1.0,
        peso_referencia=5.0,
        usar_pesos=True,
        alpha=alpha
    )
    
    pr_jer_5x = fase2_pagerank_arbol_completo(
        G, referencias_usuario, nodos_con_referencias, pr_referencias,
        peso_jerarquico=5.0,
        peso_referencia=1.0,
        usar_pesos=True,
        alpha=alpha
    )
    
    return {
        'fase1_referencias': pr_referencias,
        'nodos_con_referencias': nodos_con_referencias,
        'sin_pesos': pr_sin_pesos,
        'peso_referencias_2x': pr_peso_referencias,
        'peso_jerarquia_2x': pr_peso_jerarquia,
        'peso_referencias_5x': pr_ref_5x,
        'peso_jerarquia_5x': pr_jer_5x
    }


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

print("="*70)
print(" PAGERANK DOS FASES BIDIRECCIONAL ")
print("="*70)

# LEER ENTRADA
parentesco = 0
G = leer_entrada("entrada.txt", parentesco)

parentesco = 1
G2 = leer_entrada("entrada.txt", parentesco)

# VALIDAR ESTRUCTURA
valido = esGrafoValido(G)
if not valido:
    logging.error("La estructura del grafo no es válida. Terminando el programa.")
    exit(1)

# DEFINIR REFERENCIAS DEL USUARIO
# Estas son las referencias que el usuario proporciona (pueden ser entre cualquier nodo)
referencias_usuario = [
    (15, 18),
    (19, 17),
    (20, 18)
]

# Añadir las referencias al grafo (sin hacerlas bidireccionales todavía)
for u, v in referencias_usuario:
    if not G.has_edge(u, v):
        G.add_edge(u, v)

# Hacer lo mismo para G2 (inverso)
referencias_usuario_g2 = [
    (18, 15),
    (17, 19),
    (18, 20)
]
for u, v in referencias_usuario_g2:
    if not G2.has_edge(u, v):
        G2.add_edge(u, v)

# ASIGNACIÓN DE ETIQUETAS
for n in G.nodes():
    G.nodes[n]["etiqueta"] = "importante" if n % 2 == 0 else "normal"

for n in G2.nodes():
    G2.nodes[n]["etiqueta"] = "importante" if n % 2 == 0 else "normal"

# Identificar nodos hoja
nodos_hoja = [n for n in G.nodes() if G.in_degree(n) == 0]

print("\nCalculando algoritmo de dos fases...")

# EJECUTAR ALGORITMO COMPLETO
resultados = algoritmo_dos_fases_completo(G, referencias_usuario)

# PageRank normal como baseline
pr_normal = nx.pagerank(G, alpha=0.85)

# ============================================================================
# TABLA 1: RESULTADOS FASE 1 (Referencias)
# ============================================================================

print("\n" + "="*70)
print("PageRank en REFERENCIAS BIDIRECCIONALES")
print("Referencias del usuario:", referencias_usuario)
print("="*70)

print("\n{:<10} {:<20}".format("Nodo", "PageRank Referencias"))
print("-"*35)

nodos_con_referencias = resultados['nodos_con_referencias']
for nodo in sorted(nodos_con_referencias):
    valor = resultados['fase1_referencias'].get(nodo, 0)
    print("{:<10} {:<20.6f}".format(nodo, valor))

# ============================================================================
# TABLA 2: COMPARACIÓN DE LAS 3 VARIANTES PRINCIPALES
# ============================================================================

print("\n" + "="*70)
print("FASE 2: COMPARACIÓN DE LAS 3 VARIANTES PRINCIPALES")
print("="*70)

print("\n{:<10} {:<20} {:<20} {:<20} {:<20}".format(
    "Nodo", "Sin Pesos", "Peso Refs 2x", "Peso Jerárq 2x", "Normal (baseline)"))
print("-"*90)

for nodo in sorted(G.nodes()):
    sin_p = resultados['sin_pesos'].get(nodo, 0)
    ref_2x = resultados['peso_referencias_2x'].get(nodo, 0)
    jer_2x = resultados['peso_jerarquia_2x'].get(nodo, 0)
    normal = pr_normal.get(nodo, 0)
    print("{:<10} {:<20.6f} {:<20.6f} {:<20.6f} {:<20.6f}".format(
        nodo, sin_p, ref_2x, jer_2x, normal))

# ============================================================================
# TABLA 3: CONFIGURACIONES EXPERIMENTALES (Pesos extremos)
# ============================================================================

print("\n" + "="*70)
print("CONFIGURACIONES EXPERIMENTALES (Pesos extremos)")
print("="*70)

print("\n{:<10} {:<20} {:<20} {:<20} {:<20}".format(
    "Nodo", "Sin Pesos", "Refs 2x", "Refs 5x", "Jerárq 5x"))
print("-"*90)

for nodo in sorted(G.nodes()):
    sin_p = resultados['sin_pesos'].get(nodo, 0)
    ref_2x = resultados['peso_referencias_2x'].get(nodo, 0)
    ref_5x = resultados['peso_referencias_5x'].get(nodo, 0)
    jer_5x = resultados['peso_jerarquia_5x'].get(nodo, 0)
    print("{:<10} {:<20.6f} {:<20.6f} {:<20.6f} {:<20.6f}".format(
        nodo, sin_p, ref_2x, ref_5x, jer_5x))

# ============================================================================
# TABLA 4: DIFERENCIAS respecto a Sin Pesos
# ============================================================================

print("\n" + "="*70)
print("DIFERENCIAS respecto a SIN PESOS")
print("="*70)

print("\n{:<10} {:<20} {:<20} {:<20}".format(
    "Nodo", "Sin Pesos", "Diff Refs 2x", "Diff Jerárq 2x"))
print("-"*70)

for nodo in sorted(G.nodes()):
    sin_p = resultados['sin_pesos'].get(nodo, 0)
    ref_2x = resultados['peso_referencias_2x'].get(nodo, 0)
    jer_2x = resultados['peso_jerarquia_2x'].get(nodo, 0)
    
    diff_ref = ref_2x - sin_p
    diff_jer = jer_2x - sin_p
    
    print("{:<10} {:<20.6f} {:<+20.6f} {:<+20.6f}".format(
        nodo, sin_p, diff_ref, diff_jer))

# ============================================================================
# ÁRBOLES CON FORMATO ORIGINAL
# ============================================================================

print("\n" + "="*70)
print("RESULTADOS DETALLADOS CON FORMATO ORIGINAL")
print("="*70)

imprime_grafo(G, pr_normal, 
              "BASELINE: PageRank Normal (direccional original)")

print("\n--- RESULTADOS DOS FASES ---\n")

imprime_grafo(G, resultados['sin_pesos'], 
              "DOS FASES - SIN PESOS (todas las relaciones valen igual)")

imprime_grafo(G, resultados['peso_referencias_2x'], 
              "DOS FASES - PESO EN REFERENCIAS 2x (referencias más importantes)")

imprime_grafo(G, resultados['peso_jerarquia_2x'], 
              "DOS FASES - PESO EN JERARQUÍA 2x (jerarquía más importante)")

print("\n--- CASOS EXTREMOS ---\n")

imprime_grafo(G, resultados['peso_referencias_5x'], 
              "DOS FASES - Referencias 5x más importantes")

imprime_grafo(G, resultados['peso_jerarquia_5x'], 
              "DOS FASES - Jerarquía 5x más importante")


