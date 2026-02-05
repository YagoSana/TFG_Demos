import os
import networkx as nx

# Configuraciones de Estilo (CSS)
CSS_ESTILOS = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; }
    h1, h2 { color: #ffffff; text-align: center; }
    h3 { color: #bb86fc; border-bottom: 1px solid #333; padding-bottom: 5px; }
    
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 20px;
        margin-bottom: 40px;
    }
    
    .card {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        height: 600px; /* Un poco más alto para ver mejor */
        overflow-y: auto;
        font-family: 'Consolas', monospace;
        font-size: 13px;
    }
    
    .tree-line { white-space: pre; line-height: 1.5; }
    .node-name { color: #9e9e9e; }
    .node-leaf { color: #ffffff; font-weight: bold; }
    .score { color: #03dac6; font-weight: bold; }
    
    .table-container { overflow-x: auto; background-color: #1e1e1e; padding: 20px; border-radius: 8px; }
    table { width: 100%; border-collapse: collapse; font-family: 'Consolas', monospace; }
    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #333; }
    th { background-color: #2c2c2c; color: #bb86fc; }
    tr:hover { background-color: #252525; }
    
    .pos { color: #4caf50; font-weight: bold; }
    .neg { color: #f44336; font-weight: bold; }
    .neu { color: #757575; }
    
    .footer { margin-top: 30px; text-align: center; color: #666; font-size: 0.8em; }
</style>
"""

def _generar_string_arbol(G, pr, nodo, prefijo=""):
    """Función auxiliar recursiva para crear el HTML del árbol"""
    score = pr.get(nodo, 0)
    # Detectamos hoja si no tiene hijos salientes en la jerarquía (nivel mayor)
    nivel_actual = G.nodes[nodo].get('nivel', 0)
    hijos = [n for n in G.neighbors(nodo) if G.nodes[n].get('nivel', 0) > nivel_actual]
    es_hoja = len(hijos) == 0
    
    css_class = "node-leaf" if es_hoja else "node-name"
    
    # HTML de la línea actual
    html = f"<div class='tree-line'>{prefijo}<span class='{css_class}'>{nodo}</span> <span class='score'>{score:.6f}</span></div>"
    
    # Recursión ordenando alfabéticamente
    hijos.sort()
    for i, hijo in enumerate(hijos):
        es_ultimo = (i == len(hijos) - 1)
        # Recursión añadiendo espacios HTML (&nbsp;) para la indentación visual correcta
        html += _generar_string_arbol(G, pr, hijo, prefijo + ("&nbsp;&nbsp;&nbsp;&nbsp;" if es_ultimo else "│&nbsp;&nbsp;&nbsp;"))
        
    # Reemplazamos conectores ASCII por versiones HTML que no se rompan
    return html.replace("└── ", "└──&nbsp;").replace("├── ", "├──&nbsp;")

def exportar_html(G, pr1, pr2, pr3, nombre_archivo="index.html"):
    """
    Función principal a llamar desde tu script.
    Recibe el Grafo y los 3 diccionarios de PageRank.
    """
    print(f"\n--- Generando archivo HTML: {nombre_archivo} ---")
    
    # 1. Encontrar raíz (nodo con nivel 0)
    raices = [n for n in G.nodes if G.nodes[n].get('nivel') == 0]
    raiz = raices[0] if raices else list(G.nodes)[0]

    # 2. Generar HTML de los árboles
    html_v1 = _generar_string_arbol(G, pr1, raiz).replace("└──&nbsp;", "└── ").replace("├──&nbsp;", "├── ")
    html_v2 = _generar_string_arbol(G, pr2, raiz)
    html_v3 = _generar_string_arbol(G, pr3, raiz)

    # 3. Generar filas de la tabla
    rows_html = ""
    nodos_ordenados = sorted(G.nodes(), key=lambda x: pr3.get(x, 0), reverse=True)

    for nodo in nodos_ordenados:
        v1 = pr1.get(nodo, 0)
        v2 = pr2.get(nodo, 0)
        v3 = pr3.get(nodo, 0)
        
        d2 = v2 - v1
        d3 = v3 - v1
        
        class_d2 = "pos" if d2 > 0 else ("neg" if d2 < 0 else "neu")
        class_d3 = "pos" if d3 > 0 else ("neg" if d3 < 0 else "neu")
        sign_d2 = "+" if d2 > 0 else ""
        sign_d3 = "+" if d3 > 0 else ""
        
        rows_html += f"""
        <tr>
            <td style="color:#e0e0e0">{nodo}</td>
            <td>{v1:.6f}</td>
            <td>{v2:.6f}</td>
            <td class="{class_d2}">{sign_d2}{d2:.6f}</td>
            <td >{v3:.6f}</td>
            <td class="{class_d3}">{sign_d3}{d3:.6f}</td>
        </tr>
        """

    # 4. Ensamblar todo
    contenido = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Resultados TFG PageRank</title>
        {CSS_ESTILOS}
    </head>
    <body>
        <h1>Resultados del Algoritmo PageRank</h1>
        
        <div class="grid-container">
            <div class="card"><h3>V1: Base</h3>{html_v1}</div>
            <div class="card"><h3>V2: Pesos Hojas</h3>{html_v2}</div>
            <div class="card"><h3>V3: Final (Refs)</h3>{html_v3}</div>
        </div>
        
        <h2>Comparativa de Diferenciales</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Nodo</th><th>V1</th><th>V2</th><th>Δ V2</th><th>V3</th><th>Δ V3</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        <div class="footer">Generado automáticamente por generador_web.py</div>
    </body>
    </html>
    """
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    
    print(f"Archivo guardado en: {nombre_archivo}")