import subprocess
import sys
def install_packages():
    # Instalar PyQt5
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyqt5'])
    # Instalar fpdf
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'fpdf'])
if __name__ == '__main__':    install_packages()

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QDialog,
    QLabel,
    QFileDialog,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette
from fpdf import FPDF


class DiccionarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Diccionario")

        # Parámetros ajustables para el tamaño de la ventana emergente
        self.dialog_width = 700
        self.dialog_height = 900
        self.resize(self.dialog_width, self.dialog_height)

        # Establecer paleta de colores
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.white)

        # Título
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label = QLabel("Diccionario")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setPalette(palette)

        # Tabla para mostrar el contenido del diccionario
        self.tabla = QTableWidget(self)
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(
            ["CATEGORÍA", "NOMBRE DEL TOKEN", "SIGNO DEL TOKEN"]
        )
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setStyleSheet(
            "background-color: #333; alternate-background-color: #444; color: #fff;"
        )

        # Entradas de texto
        agregar_entrada_label = QLabel("AGREGAR ENTRADA")
        agregar_entrada_label.setFont(QFont("Arial", 16, QFont.Bold))
        agregar_entrada_label.setPalette(palette)

        self.categoriaLineEdit = QLineEdit(self)
        self.nombreTokenLineEdit = QLineEdit(self)
        self.signoTokenLineEdit = QLineEdit(self)

        categoriaLabel = QLabel("Categoría:")
        categoriaLabel.setPalette(palette)
        nombreTokenLabel = QLabel("Nombre del token:")
        nombreTokenLabel.setPalette(palette)
        signoTokenLabel = QLabel("Signo del token:")
        signoTokenLabel.setPalette(palette)

        categoriaLayout = QVBoxLayout()
        categoriaLayout.addWidget(categoriaLabel)
        categoriaLayout.addWidget(self.categoriaLineEdit)

        nombreTokenLayout = QVBoxLayout()
        nombreTokenLayout.addWidget(nombreTokenLabel)
        nombreTokenLayout.addWidget(self.nombreTokenLineEdit)

        signoTokenLayout = QVBoxLayout()
        signoTokenLayout.addWidget(signoTokenLabel)
        signoTokenLayout.addWidget(self.signoTokenLineEdit)

        inputLayout = QHBoxLayout()
        inputLayout.addLayout(categoriaLayout)
        inputLayout.addLayout(nombreTokenLayout)
        inputLayout.addLayout(signoTokenLayout)

        agregarEntradaLayout = QVBoxLayout()
        agregarEntradaLayout.addWidget(agregar_entrada_label)
        agregarEntradaLayout.addSpacing(20)
        agregarEntradaLayout.addLayout(inputLayout)
        agregarEntradaLayout.addSpacing(20)

        # Botones inferiores
        self.guardarBtn = QPushButton("Guardar", self)
        self.guardarBtn.clicked.connect(self.saveToDiccionarioFile)
        self.añadirBtn = QPushButton("Añadir", self)
        self.añadirBtn.clicked.connect(self.addEntry)
        self.eliminarBtn = QPushButton("Eliminar", self)
        self.eliminarBtn.clicked.connect(self.removeLastEntry)
        self.guardarPDFBtn = QPushButton("GuardarPDF", self)
        self.guardarPDFBtn.clicked.connect(self.guardarEnPDF)
        self.salirBtn = QPushButton("Salir", self)
        self.salirBtn.clicked.connect(self.close)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.guardarBtn)
        bottomLayout.addWidget(self.añadirBtn)
        bottomLayout.addWidget(self.eliminarBtn)
        bottomLayout.addWidget(self.guardarPDFBtn)
        bottomLayout.addStretch(1)
        bottomLayout.addWidget(self.salirBtn)

        # Layout final
        finalLayout = QVBoxLayout()
        finalLayout.addWidget(title_label)
        finalLayout.addWidget(self.tabla)
        finalLayout.addLayout(agregarEntradaLayout)
        finalLayout.addLayout(bottomLayout)

        self.setLayout(finalLayout)

        # Cargar el contenido del archivo Diccionario.txt
        self.loadDiccionario()

    def loadDiccionario(self):
        try:
            with open("Diccionario.txt", "r") as file:
                lines = file.readlines()
                self.tabla.setRowCount(len(lines))
                for row, line in enumerate(lines):
                    categoria, nombreToken, signoToken = line.strip().split()
                    self.tabla.setItem(row, 0, QTableWidgetItem(categoria))
                    self.tabla.setItem(row, 1, QTableWidgetItem(nombreToken))
                    self.tabla.setItem(row, 2, QTableWidgetItem(signoToken))
        except Exception as e:
            print(f"Error al cargar el archivo Diccionario.txt: {e}")

    def addEntry(self):
        categoria = self.categoriaLineEdit.text()
        nombreToken = self.nombreTokenLineEdit.text()
        signoToken = self.signoTokenLineEdit.text()
        currentRowCount = self.tabla.rowCount()
        self.tabla.insertRow(currentRowCount)
        self.tabla.setItem(currentRowCount, 0, QTableWidgetItem(categoria))
        self.tabla.setItem(currentRowCount, 1, QTableWidgetItem(nombreToken))
        self.tabla.setItem(currentRowCount, 2, QTableWidgetItem(signoToken))

    def saveToDiccionarioFile(self):
        try:
            with open("Diccionario.txt", "w") as file:
                rowCount = self.tabla.rowCount()
                for row in range(rowCount):
                    categoria = self.tabla.item(row, 0).text()
                    nombreToken = self.tabla.item(row, 1).text()
                    signoToken = self.tabla.item(row, 2).text()
                    file.write(f"{categoria} {nombreToken} {signoToken}\n")
        except Exception as e:
            print(f"Error al guardar en el archivo Diccionario.txt: {e}")

    def guardarEnPDF(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Guardar PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if not filepath:
            return

        # Asegurarse de que el archivo tenga la extensión .pdf
        if not filepath.endswith(".pdf"):
            filepath += ".pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(200, 220, 255)
        col_widths = [60, 60, 60]  # Define the width of the columns

        # Calculate left margin to center the table
        page_width = 210  # A4 width in mm
        total_table_width = sum(col_widths)
        left_margin = (page_width - total_table_width) / 2
        pdf.set_left_margin(left_margin)

        # Add header
        headers = ["Categoría", "Nombre del Token", "Signo del Token"]
        for col, header in enumerate(headers):
            pdf.set_font("Arial", "B", 14)
            pdf.cell(col_widths[col], 10, header, 1, 0, "C", 1)
        pdf.ln()

        # Add content from the table
        pdf.set_font("Arial", size=12)  # Set font for table content
        for row in range(self.tabla.rowCount()):
            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(row, col)
                if item and item.text():
                    content = item.text()
                    pdf.cell(col_widths[col], 10, content, 1)
            pdf.ln()

        # Save the PDF
        pdf.output(filepath)

    def removeLastEntry(self):
        lastRow = self.tabla.rowCount() - 1
        if lastRow >= 0:
            self.tabla.removeRow(lastRow)


class AnalizadorLexico(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Analizador Léxico")

        # Fuente para cada widget
        font_textEdit = QFont("Arial", 12)
        font_buttons = QFont("Verdana", 10, QFont.Bold)

        # Definición de colores
        background_color = "#222"
        panel_color = "#333"
        button_color = "#555"

        # Aplicar estilos personalizados
        self.applyDarkTheme(background_color, panel_color, button_color)

        # Título
        title_font = QFont("Arial", 30, QFont.Bold)
        title_label = QLabel("Analizador Léxico")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_palette = QPalette()
        title_palette.setColor(QPalette.WindowText, Qt.white)
        title_label.setPalette(title_palette)

        # Panel 1: Editor de texto
        self.textEdit1 = QTextEdit(self)
        self.textEdit1.setFont(font_textEdit)
        self.textEdit1.setTextColor(Qt.white)

        # Botones superiores
        self.diccionarioBtn = QPushButton("Diccionario", self)
        self.diccionarioBtn.setFont(font_buttons)
        self.diccionarioBtn.setFixedHeight(50)
        self.diccionarioBtn.clicked.connect(self.showDiccionarioDialog)

        self.importarBtn = QPushButton("Importar", self)
        self.importarBtn.setFont(font_buttons)
        self.importarBtn.setFixedHeight(50)
        self.importarBtn.clicked.connect(self.importarArchivo)

        self.limpiarTextoBtn = QPushButton("Limpiar Texto", self)
        self.limpiarTextoBtn.setFont(font_buttons)
        self.limpiarTextoBtn.setFixedHeight(50)
        self.limpiarTextoBtn.clicked.connect(self.limpiarTexto)

        self.limpiarTablaBtn = QPushButton("Limpiar Tabla", self)
        self.limpiarTablaBtn.setFont(font_buttons)
        self.limpiarTablaBtn.setFixedHeight(50)
        self.limpiarTablaBtn.clicked.connect(self.limpiarTabla)

        self.escanearBtn = QPushButton("Escanear", self)
        self.escanearBtn.setFont(font_buttons)
        self.escanearBtn.setFixedHeight(50)
        self.escanearBtn.clicked.connect(self.escanearTexto)

        self.guardarBtn = QPushButton("Guardar", self)
        self.guardarBtn.setFont(font_buttons)
        self.guardarBtn.setFixedHeight(50)
        self.guardarBtn.clicked.connect(self.guardarResultados)

        topButtonLayout = QHBoxLayout()
        topButtonLayout.addWidget(self.diccionarioBtn)
        topButtonLayout.addWidget(self.importarBtn)
        topButtonLayout.addWidget(self.limpiarTextoBtn)
        topButtonLayout.addWidget(self.limpiarTablaBtn)
        topButtonLayout.addWidget(self.escanearBtn)
        topButtonLayout.addWidget(self.guardarBtn)

        # Panel 2: Tabla de resultados
        self.tablaResultados = QTableWidget(self)
        self.tablaResultados.setColumnCount(5)
        self.tablaResultados.setHorizontalHeaderLabels(
            ["Linea", "Posición", "Categoría", "Nombre", "Signo"]
        )
        header = self.tablaResultados.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.tablaResultados.setStyleSheet(
            "background-color: #333; alternate-background-color: #444; color: #fff;"
        )

        # Layout de los paneles
        panelsLayout = QHBoxLayout()
        panelsLayout.addWidget(self.textEdit1)
        panelsLayout.addWidget(self.tablaResultados)

        # Layout final
        finalLayout = QVBoxLayout()
        finalLayout.addWidget(title_label)
        finalLayout.addLayout(topButtonLayout)
        finalLayout.addLayout(panelsLayout)

        centralWidget = QWidget(self)
        centralWidget.setLayout(finalLayout)
        self.setCentralWidget(centralWidget)

        # Maximizar la ventana al inicio
        self.showMaximized()

    def importarArchivo(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Importar Archivo", "", "Todos los archivos (*)", options=options
        )
        if filepath:
            with open(filepath, "r") as file:
                content = file.read()
                self.textEdit1.setPlainText(content)

    def limpiarTexto(self):
        self.textEdit1.clear()

    def applyDarkTheme(self, bg_color, panel_color, btn_color):
        dark_palette = f"""
        QWidget {{
            background-color: {bg_color};
        }}
        QTextEdit, QLineEdit {{
            color: #b1b1b1;
            background-color: {panel_color};
            border: 1px solid #444;
            border-radius: 5px;
        }}
        QPushButton {{
            background-color: {btn_color};
            border: 1px solid #444;
            padding: 5px;
            border-radius: 10px;
            color: white;
        }}
        QPushButton:hover {{
            background-color: #666;
        }}
        QPushButton:pressed {{
            background-color: #777;
        }}
        """
        self.setStyleSheet(dark_palette)

    def showDiccionarioDialog(self):
        self.diccionarioDialog = DiccionarioDialog(self)
        self.diccionarioDialog.exec_()

    def escanearTexto(self):
        # Cargar el diccionario
        diccionario = {}
        categorias = {}
        try:
            with open("Diccionario.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    categoria, nombreToken, signoToken = line.strip().split()
                    diccionario[signoToken] = nombreToken
                    categorias[signoToken] = categoria
        except Exception as e:
            print(f"Error al cargar el archivo Diccionario.txt: {e}")

        # Escanear el texto
        texto = self.textEdit1.toPlainText()
        lineas = texto.split("\n")
        resultados = []

        for num_linea, linea in enumerate(lineas, 1):
            pos = 1
            i = 0
            while i < len(linea):
                token_encontrado = False
                for signoToken, nombreToken in sorted(
                    diccionario.items(), key=lambda x: len(x[0]), reverse=True
                ):
                    end_index = i + len(signoToken)
                    if (
                        linea[i:end_index] == signoToken
                        and (end_index == len(linea) or not linea[end_index].isalpha())
                        and (i == 0 or not linea[i - 1].isalpha())
                    ):
                        resultados.append((num_linea, pos, nombreToken, signoToken))
                        i += len(signoToken) - 1
                        pos += len(signoToken)
                        token_encontrado = True
                        break
                if not token_encontrado and linea[i] != " ":
                    pos += 1
                i += 1

        # Mostrar resultados en la tabla
        self.tablaResultados.setRowCount(len(resultados))
        for row, (num_linea, pos, nombreToken, signoToken) in enumerate(resultados):
            self.tablaResultados.setItem(row, 0, QTableWidgetItem(str(num_linea)))
            self.tablaResultados.setItem(row, 1, QTableWidgetItem(str(pos)))
            self.tablaResultados.setItem(
                row, 2, QTableWidgetItem(categorias[signoToken])
            )
            self.tablaResultados.setItem(row, 3, QTableWidgetItem(nombreToken))
            self.tablaResultados.setItem(row, 4, QTableWidgetItem(signoToken))

    def limpiarTabla(self):
        self.tablaResultados.setRowCount(0)

    def guardarResultados(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Resultados",
            "",
            "Archivo de Texto (*.txt);;Todos los archivos (*)",
            options=options,
        )
        if filepath:
            with open(filepath, "w") as file:
                for row in range(self.tablaResultados.rowCount()):
                    line_data = []
                    for col in range(self.tablaResultados.columnCount()):
                        item = self.tablaResultados.item(row, col)
                        if item and item.text():
                            line_data.append(item.text())
                    file.write("\t".join(line_data) + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AnalizadorLexico()
    window.show()
    sys.exit(app.exec_())
