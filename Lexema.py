import tkinter as tk
from tkinter import ttk, scrolledtext
import ply.lex as lex

class Vocabulario(object):
    palabras_reservadas = {
        'AREA': 'AREA', 'BASE': 'BASE', 'ALTURA': 'ALTURA',
    }

    tokens = [
        'IDENTIFICADOR', 'NUMERO',
        'OPERADOR', 'SIMBOLO', 'FIN',
    ] + list(palabras_reservadas.values())

    t_OPERADOR = r'[\+\*-/=]'
    t_SIMBOLO = r'[\(\)\[\]\{\};,]'
    t_ignore = ' \t'

    def t_NUMERO(self, t):
        r'\d*\.\d+|\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print(f"Float value too large {t.value}")
            t.value = 0
        if isinstance(t.value, float) and '.' in str(t.value):
            t.type = 'NUMERO'
        else:
            t.type = 'NUMERO'
            t.value = int(t.value)
        return t

    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.palabras_reservadas.get(t.value.upper(), 'IDENTIFICADOR')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.build()
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens

def analizar_codigo():
    codigo = entrada_codigo.get("1.0", "end-1c")
    vocabulario = Vocabulario()
    vocabulario.build()
    vocabulario.lexer.input(codigo)
    
    # Limpiar el Treeview antes de mostrar nuevos resultados
    for i in result_tree.get_children():
        result_tree.delete(i)

    # Insertar los resultados en el Treeview
    for tok in vocabulario.lexer:
        if tok.type == 'IDENTIFICADOR':
            result_tree.insert("", 'end', values=(tok.value, "", "X", "", "", ""))
        elif tok.type == 'NUMERO':
            result_tree.insert("", 'end', values=(tok.value, "", "", "", "X", ""))
        elif tok.type == 'OPERADOR':
            result_tree.insert("", 'end', values=(tok.value, "", "", "X", "", ""))
        elif tok.type == 'SIMBOLO':
            result_tree.insert("", 'end', values=(tok.value, "", "", "", "", "X"))
        elif tok.type in Vocabulario.palabras_reservadas.values():
            result_tree.insert("", 'end', values=(tok.value, "X", "", "", "", ""))

ventana = tk.Tk()
ventana.title("Analizador Léxico con Tkinter")

frame_izquierda = ttk.Frame(ventana)
frame_izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

entrada_codigo = scrolledtext.ScrolledText(frame_izquierda, width=40, height=10, wrap=tk.WORD)
entrada_codigo.pack(fill="both", expand=True)

boton_analizar = tk.Button(frame_izquierda, text="Analizar Código", command=analizar_codigo)
boton_analizar.pack(pady=5)

frame_derecha = ttk.Frame(ventana)
frame_derecha.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Configuración del Treeview
result_tree = ttk.Treeview(frame_derecha, columns=("Token", "Palabra_R", "IDENTIFICADOR", "OPERADOR", "NUMERO", "SÍMBOLO"), show="headings")
result_tree.heading("Token", text="Token")
result_tree.heading("Palabra_R", text="Palabra_R")
result_tree.heading("IDENTIFICADOR", text="IDENTIFICADOR")
result_tree.heading("OPERADOR", text="OPERADOR")
result_tree.heading("NUMERO", text="NUMERO")
result_tree.heading("SÍMBOLO", text="SÍMBOLO")

result_tree.column("Token", anchor="center")
result_tree.column("Palabra_R", anchor="center")
result_tree.column("IDENTIFICADOR", anchor="center")
result_tree.column("OPERADOR", anchor="center")
result_tree.column("NUMERO", anchor="center")
result_tree.column("SÍMBOLO", anchor="center")

result_tree.pack(fill="both", expand=True)

ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)

ventana.mainloop()
