import networkx as nx

from lector import leer_entrada
from imprimir import imprime_grafo, imprime_grafo_invertido
from validador import esGrafoValido

import logging

def asignar_relaciones(G):
    """Crear relaciones de referencias entre <documentos>. Eventualmente, estas relaciones vendrán en un archivo externo."""
    G.add_edge(15, 18)
    G.add_edge(19, 17)
    G.add_edge(20, 18)

# LEER ENTRADA
print(" - Leyendo el archivo de entrada - ")
parentesco = 0 #valor para indicar que este grafo es de hijos -> padres
G = leer_entrada("entrada.txt", parentesco)

#prueba con el grafo invertido
parentesco = 1 #valor para indicar que este grafo es de padres -> hijos
G2 = leer_entrada("entrada.txt", parentesco)

# VALIDAR ESTRUCTURA
print(" - Validando la estructura del grafo - ")
valido = esGrafoValido(G)
if not valido:
    logging.error("La estructura del grafo no es válida. Terminando el programa.")
    exit(1)

# CREAR RELACIONES DE REFERENCIA ENTRE HOJAS
print(" - Creando relaciones de referencia entre hojas - ")
asignar_relaciones(G)
#asignar_relaciones(G2)
G2.add_edge(18, 15)
G2.add_edge(17, 19)
G2.add_edge(18, 20)

# ASIGNACIÓN DE ETIQUETAS
for n in G.nodes():
    G.nodes[n]["etiqueta"] = "importante" if n % 2 == 0 else "normal"

for n in G2.nodes():
    G2.nodes[n]["etiqueta"] = "importante" if n % 2 == 0 else "normal"


# CÁLCULOS DE PAGERANK
print(" - Calculando PageRank con diferentes configuraciones - ")

# A) PageRank Normal
pr_normal = nx.pagerank(G, alpha=0.85)

# B) PageRank con nstart (nodos hoja)
nodos_hoja = [n for n in G.nodes() if G.in_degree(n) == 0]
dicc_nstart = {n: (100 if n in nodos_hoja else 0) for n in G.nodes()}
pr_nstart = nx.pagerank(G, alpha=0.85, nstart=dicc_nstart)

# C) Personalization Suavizada (Hojas)
N = len(G.nodes())
extra = 0.3
personalization_hojas = {
    n: (1 - extra) * (1/N) + extra * (1/len(nodos_hoja) if n in nodos_hoja else 0)
    for n in G.nodes()
}
pr_pers_hojas = nx.pagerank(G, alpha=0.85, personalization=personalization_hojas)

# D) Personalization Suavizada (Etiquetas)
nodos_obj = [n for n in G.nodes() if G.nodes[n].get("etiqueta") == "importante"]
if nodos_obj:
    pers_etiqueta = {
        n: (1 - extra) * (1/N) + extra * (1/len(nodos_obj) if n in nodos_obj else 0)
        for n in G.nodes()
    }
    pr_pers_etiqueta = nx.pagerank(G, alpha=0.85, personalization=pers_etiqueta)
else:
    pr_pers_etiqueta = pr_normal


#prueba para g2
pr_normal2 = nx.pagerank(G2, alpha=0.85)

nodos_obj2 = [n for n in G2.nodes() if G2.nodes[n].get("etiqueta") == "importante"]
if nodos_obj2:
    pers_etiqueta2 = {
        n: (1 - extra) * (1/N) + extra * (1/len(nodos_obj2) if n in nodos_obj2 else 0)
        for n in G2.nodes()
    }
    pr_pers_etiqueta2 = nx.pagerank(G2, alpha=0.85, personalization=pers_etiqueta2)
else:
    pr_pers_etiqueta2 = pr_normal2


# IMPRESIÓN DE RESULTADOS
print(" - Imprimiendo resultados - ")
imprime_grafo(G, pr_normal, "PAGE RANK NORMAL")
imprime_grafo(G, pr_nstart, "PAGE RANK CON NSTART")
imprime_grafo(G, pr_pers_hojas, "PERSONALIZATION SUAVIZADA (HOJAS)")
imprime_grafo(G, pr_pers_etiqueta, "PERSONALIZATION SUAVIZADA (ETIQUETAS)")

print(" - Imprimiendo resultados para el grafo invertido - ")
imprime_grafo_invertido(G2, pr_normal2, "PAGE RANK NORMAL")
imprime_grafo_invertido(G2, pr_pers_etiqueta2, "PERSONALIZATION SUAVIZADA (ETIQUETAS)")
