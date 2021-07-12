import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile

# este comando indica el inicion de la interfaz
root = tk.Tk()

# esto para aumentar el tamaño de la ventana
canvas = tk.Canvas(root, width=600, height=300)

# esto separa la interfaz en 3 columnas identicas e invisibles
canvas.grid(columnspan=3, rowspan=3)

# para cargar el logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo  # muy necesaria

# luego, para cargar el logo en la interfaz
logo_label.grid(column=1, row=0)

# instrucciones
instructions = tk.Label(root, text='seleccionar un PDF para extrar su contenido', font='Ralway')
instructions.grid(columnspan=3, column=0, row=1)

# Boton para cargar el PDF

# ahora le vamos a dar una funcion al Boton
def open_file():
    # para cambiar el texto del boton
    brownse_text.set('cargando...')
    file = askopenfile(parent=root, mode='rb', title='Escoger un arhivo', filetype=[('Pdf file', '*.pdf')])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()

        # ventana de texto
        text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
        text_box.insert(1.0, page_content)

        # esto es para centrar el text_box
        text_box.tag_configure('center', justify='center')
        text_box.tag_add('center', 1.0, 'end')

        # ahora lo cargamos
        text_box.grid(column=1, row=3)

        brownse_text.set('Cargar')



## el texto del boton
brownse_text = tk.StringVar()
brownse_text.set('Cargar')

# insertar el boton en la interfaz
brownse_btn = tk.Button(root, textvariable=brownse_text, command=lambda:open_file(), font='Raleway', bg='#20bebe', height=2, width=15)
brownse_btn.grid(column=1, row=2)


# esto es para darle mas espacio al final
canvas = tk.Canvas(root, width=600, height=250)
canvas.grid(columnspan=3, rowspan=3)

root.mainloop()
