import networkx as nx
from lector import leer_entrada
from imprimir import imprime_grafo

def ejecutar_analisis():
    # 1. LEER ENTRADA
    G = leer_entrada("entrada.txt")

    # 2. ASIGNACIÓN DE ETIQUETAS
    for n in G.nodes():
        G.nodes[n]["etiqueta"] = "importante" if n % 2 == 0 else "normal"

    # 3. CÁLCULOS DE PAGERANK
    
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

    # 4. IMPRESIÓN DE RESULTADOS
    imprime_grafo(G, pr_normal, "PAGE RANK NORMAL")
    imprime_grafo(G, pr_nstart, "PAGE RANK CON NSTART")
    imprime_grafo(G, pr_pers_hojas, "PERSONALIZATION SUAVIZADA (HOJAS)")
    imprime_grafo(G, pr_pers_etiqueta, "PERSONALIZATION SUAVIZADA (ETIQUETAS)")

if __name__ == "__main__":
    ejecutar_analisis()