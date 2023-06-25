from tkinter import  *
from tkinter.scrolledtext import *
import Lexer as lexer
from idlelib.percolator import Percolator
import idlelib.colorizer as ic
import LL1ParserExcep as LL1

def verificar_codigo(event=None):
    # Habilitar la edición de la consola
    output_window.config(state=NORMAL)
    output_window.delete(1.0, END)
    output_window.config(state=DISABLED)
    
    texto = text.get("1.0", END)  # Obtiene el texto del campo de entrada
    palabras = texto.split()  # Divide el texto en palabras

    if not (palabras == []):
        result, error = lexer.run('archivo.txt', texto)
        if error:
            # Habilitar la edición de la consola programáticamente
            output_window.config(state=NORMAL)
            output_window.delete(1.0, END)
            output_window.insert(1.0, error.as_string())
            output_window.config(state=DISABLED)
def run(event=None):
    filetxt = text.get("1.0", END)  # Obtiene el texto del campo de entrada
    if filetxt != '\n':
        result, error = lexer.run('archivo.txt', filetxt)
        parse = []
        if error:
                # Habilitar la edición de la consola programáticamente
                output_window.config(state=NORMAL)
                output_window.delete(1.0, END)
                output_window.insert(1.0, error.as_string())
                output_window.config(state=DISABLED)
        else:
            #print(result) 
            out = ''
            for token in result:
                
                if token.type != lexer.TT_EOF: parse.append(token)
                    
                if token.type == ';':
                    out += " "+token.type + "\n"
                elif token.type == 'KEYWORD':
                    out += "\n"+token.type+": "+token.value+"\n"
                else:
                    out += " "+token.type
            #print(out)
        if error:
                # Habilitar la edición de la consola programáticamente
                output_window.config(state=NORMAL)
                output_window.delete(1.0, END)
                output_window.insert(1.0, error.as_string())
                output_window.config(state=DISABLED)
        else:
            parse.append(lexer.Token(type_='PARSE',value_="$"))
            #print(parse)
            parser = LL1.Parser()
            parser.main(parse)
            error = parser.algorithm()
            
            if error:
                # Habilitar la edición de la consola programáticamente
                output_window.config(state=NORMAL)
                output_window.delete(1.0, END)
                output_window.insert(1.0, error.as_string())
                output_window.config(state=DISABLED)
            else:
                # Habilitar la edición de la consola programáticamente
                output_window.config(state=NORMAL)
                output_window.delete(1.0, END)
                output_window.insert(1.0, "Sintaxis valida")
                output_window.config(state=DISABLED)
    else:
        # Habilitar la edición de la consola programáticamente
        output_window.config(state=NORMAL)
        output_window.delete(1.0, END)
        output_window.insert(1.0, "Texto Vacio")
        output_window.config(state=DISABLED)        
            
            
window = Tk()
window.geometry("1000x800")
window.title("Analizador Léxico")

# create and configure menu
menu = Menu(window)
window.config(menu=menu)


# create input frame
input_frame = Frame(window)
input_frame.pack(fill=BOTH, side=TOP, padx=15, pady=20)

# Title Label
title_label = Label(input_frame, text = "Compiler", font=("Arial Bold", 20), fg = "#2B3239")
title_label.pack(side=TOP, padx=25, pady=15)

# create input_window window for writing code
input_window = ScrolledText(input_frame, font=("Arial", 10), wrap=None)
input_window.pack(padx = 10, side=LEFT, fill=BOTH, expand=True)

# Área de texto para ingresar el código
text = ScrolledText(input_window, font=("Arial", 10))
text.pack(fill=BOTH, side=LEFT,expand=True)  # Rellena y expande el widget de texto
Percolator(text).insertfilter(ic.ColorDelegator())



text.bind('<KeyRelease>', verificar_codigo)  # Asocia la función verificar_texto al evento de liberación de tecla

# create output frames
output_frame = Frame(window)
output_frame.pack(fill=X,side=BOTTOM, padx=15, pady=20, expand=False)

# Title Label
output_label = Label(output_frame, text = "Console", font=("Arial Bold", 14), fg = "#2B3239")
output_label.pack(side=TOP, padx=20, pady=15)

# create output window to display output of written code
output_window = ScrolledText(output_frame,state=DISABLED,font=("Arial Bold", 15), height=10)
output_window.pack(padx = 10, pady = 10, side=BOTTOM,  fill=BOTH, expand=1)
output_window.config(fg="red")

# create menus
file_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
view_menu = Menu(menu, tearoff=0)
theme_menu = Menu(menu, tearoff=0)


# function for light mode window
def light():
    window.config(bg="#CFDCE7")
    title_label.config(fg="#2B3239",bg="#CFDCE7")
    input_frame.config(bg="#CFDCE7")
    input_window.config(fg="#2B3239", bg="white")

    #OUTPUT
    output_label.config(fg="#2B3239", bg="#CFDCE7")
    output_frame.config( bg="#CFDCE7")
    output_window.config(fg="#2B3239", bg="white")
    #status_bars.config(fg="#2B3239",bg="#CFDCE7")

# function for dark mode window
def dark():
    window.config(bg="#183A59")
    title_label.config(fg="white",bg="#183A59")
    input_frame.config(bg="white")
    input_window.config(fg="white", bg="black")
    #OUTPUT
    output_label.config(fg="white", bg="#183A59")
    output_frame.config(bg="#183A59")
    output_window.config(fg="red", bg="black")

# add commands to change themes
theme_menu.add_command(label="light", command=light)
theme_menu.add_command(label="dark", command=dark)

# add menu labels
menu.add_cascade(label="Archivo", menu=file_menu)
menu.add_cascade(label="Editar", menu=edit_menu)
menu.add_cascade(label="Ejecutar", menu=run_menu)
menu.add_cascade(label="Ver", menu=view_menu)
menu.add_cascade(label="Tema", menu=theme_menu)
run_menu.add_command(label="Ejecutar", accelerator="F5", command=run)
# Ejecutar la window principal de Tkinter
window.mainloop()