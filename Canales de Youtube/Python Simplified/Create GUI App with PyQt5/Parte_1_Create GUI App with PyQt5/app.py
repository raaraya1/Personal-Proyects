# importar bibliotecas
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

# variables globales
widgets = {
    'logo':[],
    'button':[],
    'score':[],
    'question':[],
    'answer1':[],
    'answer2':[],
    'answer3':[],
    'answer4':[]
    }


# para crear la aplicacion
app = QApplication(sys.argv)

# para crear la ventana
window = QWidget()
window.setWindowTitle('Quien quiere ser un programador???')
window.setFixedWidth(1000)
window.move(200, 100)
window.setStyleSheet('background: #161219;')

# --------------------- CREAR LOS OBJETOS --------------------------------
# crear planilla
grid = QGridLayout()

# limpiar las variables globales
def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def show_frame1():
    clear_widgets()
    frame1()

# funciones de los botones
def start_game():
    clear_widgets()
    frame2()

# funcion para crear botones
def create_buttons(answer, l_margin, r_margin):
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        '*{border: 4px solid "#BC006C";' +
        'margin-left: ' + str(l_margin) + 'px;' +
        'margin-right: ' + str(r_margin) + 'px;' +
        'border-radius: 25px;' +
        'font-size: 16px;' +
        'font-family: "Shanti";' +
        'color: "white";' +
        'padding: 15px 0;' +
        'margin-top: 20px;}' +
        '*:hover{background: "#BC006C";}'
        )
    button.clicked.connect(show_frame1)

    return button


# crear pantalla de inicio
def frame1():
    # crear logo
    image = QPixmap('logo.png')
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet('margin-top: 100px;') # separacion arriba
    widgets['logo'].append(logo)
    # crear boton
    button = QPushButton('JUGAR')
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
            '*{border: 4px solid "#BC006C";' +
            'border-radius: 45px;' +
            'font-size: 35px;' +
            'color: "white";' +
            'padding: 25px 0;' +
            'margin: 100px 200px;}' +
            '*:hover{background: "#BC006C";}'
            )
    # ejecutable del boton
    button.clicked.connect(start_game)
    widgets['button'].append(button)
    # COLOCAR OBJETOS EN LA PLANILLA
    grid.addWidget(widgets['logo'][-1], 0, 0, 1, 2)  # (nombre widget, row, column)
    grid.addWidget(widgets['button'][-1], 1, 0, 1, 2)

def frame2():
    # puntaje
    score = QLabel('80')
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet('''
        font-size: 35px;
        color: 'white';
        padding: 15px 10px;
        margin: 20px 200px;
        background: '#64A314';
        border: 1px solid '#64A314';
        border-radius: 35px;
        ''')
    widgets['score'].append(score)
    # pregunta
    question = QLabel('Placeholder text will go here')
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        'font-family: Shanti;' +
        'font-size: 25px;' +
        'color: "white";' +
        'padding: 75px;'
    )
    widgets['question'].append(question)
    # botones de respuesta
    button1 = create_buttons('answer1', 85, 5)
    button2 = create_buttons('answer2', 5, 85)
    button3 = create_buttons('answer3', 85, 5)
    button4 = create_buttons('answer4', 5, 85)

    widgets['answer1'].append(button1)
    widgets['answer2'].append(button2)
    widgets['answer3'].append(button3)
    widgets['answer4'].append(button4)

    # imagen al final
    image = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet('margin-top: 75px; margin-bottom: 30px') # separacion arriba
    widgets['logo'].append(logo)


    # COLOCAR OBJETOS EN LA PLANILLA
    grid.addWidget(widgets['score'][-1], 0, 1)  # (nombre widget, row, column)
    grid.addWidget(widgets['question'][-1], 1, 0, 1, 2) # (nombre widget, row, column, rowspan, columnspan)
    grid.addWidget(widgets['answer1'][-1], 2, 0)
    grid.addWidget(widgets['answer2'][-1], 2, 1)
    grid.addWidget(widgets['answer3'][-1], 3, 0)
    grid.addWidget(widgets['answer4'][-1], 3, 1)
    grid.addWidget(widgets['logo'][-1], 4, 0, 1, 2)


# ahora llamamos al cuadro
frame1()

# --------------------- COLOCAR LOS OBJETOS EN LA VENTANA -----------------
# ahora colocamos esta planilla en la ventana
window.setLayout(grid)


# para mostrar la ventana
window.show()

# para cerrar la aplicacion
sys.exit(app.exec())
