import networkx as nx

import logging

def esGrafoValido(G):
    """Verifica si el grafo es un bosque (colección de árboles) donde cada nodo apunta a lo sumo a un padre."""
   
    # Comprobar si hay ciclos
    if not nx.is_directed_acyclic_graph(G):
        logging.error("El grafo contiene ciclos (no es un árbol).")
        return False

    # Cada nodo debe tener como máximo un grado de salida de 1, porque son aristas invertidas (hijo -> padre)
    for nodo in G.nodes():
        if G.out_degree(nodo) > 1:
            print(f"ERROR: El nodo {nodo} tiene más de un padre (no es un árbol puro).")
            return False

    return True