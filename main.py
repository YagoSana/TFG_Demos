import networkx as nx
from lector import leer_entrada
from imprimir import imprimir_grafo
import logging

G = leer_entrada("entrada.txt")

imprimir_grafo(G, "ÁRBOL DE LIBROS")
