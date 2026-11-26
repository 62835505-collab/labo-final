# dfa_cajero_automatico.py
# ---------------------------------------------------------------------------
# Caso práctico: Autómata Finito Determinista (AFD) de un cajero automático.
#
# Modela el flujo de uso de un cajero: insertar tarjeta, ingresar el PIN
# (dígito por dígito), reintentar si el PIN es incorrecto, elegir una opción
# del menú (retirar efectivo o consultar saldo) y finalizar expulsando la
# tarjeta.
#
# Alfabeto:
#   a -> tecla numérica (ingresar un dígito / elegir "retirar")
#   b -> confirmar / aceptar / elegir "consultar saldo"
#   c -> cancelar / PIN incorrecto confirmado
#
# Estados (7 en total):
#   q0 -> Inicio (tarjeta insertada)
#   q1 -> Ingresando PIN                (BUCLE con 'a': cada dígito tecleado)
#   q2 -> PIN incorrecto
#   q3 -> Menú principal
#   q4 -> Retirar efectivo              (BUCLE con 'a': pedir más billetes)
#   q5 -> Consultar saldo
#   q6 -> Fin de operación / tarjeta expulsada  (ESTADO FINAL)
# ---------------------------------------------------------------------------
import sys, matplotlib.pyplot as plt, networkx as nx
from matplotlib.patches import FancyArrowPatch

# === Definición del DFA ===
states = {"q0","q1","q2","q3","q4","q5","q6"}
alphabet = {"a","b","c"}
delta = {("q0","a"):"q1",
        ("q1","a"):"q1",   # BUCLE: sigue ingresando dígitos del PIN
        ("q1","b"):"q3",   # PIN confirmado correcto -> menú
        ("q1","c"):"q2",   # PIN confirmado incorrecto
        ("q2","a"):"q1",   # reintentar ingreso de PIN
        ("q2","c"):"q6",   # cancela tras fallar -> fin (tarjeta retenida)
        ("q3","a"):"q4",   # elige "retirar efectivo"
        ("q3","b"):"q5",   # elige "consultar saldo"
        ("q3","c"):"q6",   # cancela operación -> fin
        ("q4","a"):"q4",   # BUCLE: pide otro monto/billetes
        ("q4","b"):"q6",   # confirma retiro -> fin
        ("q5","b"):"q6"}   # vuelve/finaliza tras ver saldo -> fin

q0, F = "q0", {"q6"}

# === Simulación ===
def run(s):
    q, steps = q0, [q0]
    for i,ch in enumerate(s):
        if (q,ch) not in delta: raise ValueError(f"Sin transición desde {q} con '{ch}' en pos {i}")
        q = delta[(q,ch)]; steps.append(q)
    return steps, steps[-1] in F

# === Palabras de prueba (requeridas por la rúbrica) ===
ACEPTADAS = [
    "abab", "abbb", "abc", "acc", "aacc",
    "aaabab", "acabc", "aaabc", "aabaab", "acaabc",
]
RECHAZADAS = [
    "a", "ab", "ac", "aba", "cab",
]

def probar_lote():
    print(f"{'Cadena':<10} {'Resultado':<10} Estado final / motivo")
    print("-"*55)
    for s in ACEPTADAS + RECHAZADAS:
        try:
            steps, ok = run(s)
            resultado = "ACEPTA" if ok else "RECHAZA"
            print(f"{s:<10} {resultado:<10} {steps[-1]}")
        except ValueError as e:
            print(f"{s:<10} {'RECHAZA':<10} {e}")

# === Grafo y layout ===
G = nx.MultiDiGraph(); G.add_nodes_from(states)
for (q,a),p in delta.items(): G.add_edge(q,p,key=a,label=a)
pos = nx.spring_layout(G, seed=7)

# === Dibujo por paso ===
def _mid(p1,p2,o=0.10):
    (x1,y1),(x2,y2)=p1,p2; mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; nx_,ny_=-dy,dx; L=(nx_**2+ny_**2)**0.5 or 1
    return mx+o*nx_/L, my+o*ny_/L

def draw_step(current, idx, sym=None):
    plt.clf(); nodes=list(G.nodes())
    nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_size=[900 if n==current else 600 for n in nodes],linewidths=[3 if n in F else 1 for n in nodes],edgecolors="black")
    nx.draw_networkx_labels(G,pos)
    seen={}
    for u,v,k,d in G.edges(keys=True,data=True):
        if u==v:
            x,y=pos[u]; plt.gca().add_patch(FancyArrowPatch((x,y),(x+1e-4,y+1e-4),connectionstyle="arc3,rad=0.45",arrowstyle='-|>',mutation_scale=18))
            plt.text(x,y+0.18,d['label'],fontsize=11,ha='center'); continue
        i=seen.get((u,v),0); seen[(u,v)]=i+1; rad=0.25 if i%2==0 else -0.25
        nx.draw_networkx_edges(G,pos,edgelist=[(u,v)],connectionstyle=f"arc3,rad={rad}",arrows=True,arrowstyle='-|>',arrowsize=20)
        lx,ly=_mid(pos[u],pos[v],0.10 if i%2==0 else -0.10); plt.text(lx,ly,d['label'],fontsize=11,ha='center',va='center')
    plt.axis('off'); plt.title(f"Paso {idx}: {current}" + (f" | '{sym}'" if sym else "")); plt.pause(1.0)

def mostrar_diagrama_estatico():
    """Dibuja el AFD completo (sin animación), útil para capturas de pantalla."""
    draw_step(q0, 0)
    plt.show()

# === core/main ===
if __name__=='__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        probar_lote()
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "--diagrama":
        mostrar_diagrama_estatico()
        sys.exit(0)

    s = sys.argv[1] if len(sys.argv)>1 else input("Cadena (a/b/c): ").strip()
    try:
        steps, ok = run(s); print("ACEPTA" if ok else "RECHAZA", f"(estado final: {steps[-1]})")
        plt.ion(); draw_step(steps[0],0)
        for i,ch in enumerate(s,1): draw_step(steps[i],i,ch)
        plt.ioff(); plt.show()
    except Exception as e:
        print("RECHAZA:", e)
