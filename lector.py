import networkx as nx
import sys

def leer_entrada(nombre_archivo):
    """Lee un archivo de texto y devuelve un grafo de NetworkX con aristas invertidas."""
    G = nx.DiGraph()
    try:
        with open(nombre_archivo, 'r') as f:
            # Saltamos la primera línea (metadatos)
            f.readline()

            for linea in f:
                nueva_linea = linea.strip()
                if nueva_linea: 
                    valores = nueva_linea.split()
                    if len(valores) >= 2:
                        ini = int(valores[0])
                        fin = int(valores[1])
                        # Aristas invertidas (hijo -> padre) según tu lógica original
                        G.add_edge(fin, ini)
        return G
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo '{nombre_archivo}'.")
        sys.exit(1)