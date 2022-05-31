from PySide6.QtWidgets import QPushButton, QWidget, QLabel, QMessageBox, QApplication
from PySide6.QtGui import QCloseEvent

class Gra(QWidget):
    def __init__(self):
        super(Gra, self).__init__()
        self.setFixedSize(640, 420)
        self.setWindowTitle("Nowa gra")


class Interfejs(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(640, 420)
        self.setWindowTitle("Statki - NPG 2022")
        self.a = None
        self.run()
    def run(self):


        self.button_start = QPushButton(self)
        self.button_start.move(200, 180)
        self.button_start.resize(150, 30)
        self.button_start.setText("Rozpocznij grę")
        self.button_start.clicked.connect(self.Okno)

        self.button_quit = QPushButton(self)
        self.button_quit.move(200, 220)
        self.button_quit.resize(150, 30)
        self.button_quit.setText("Wyjście")
        self.button_quit.clicked.connect(QApplication.instance().quit)



        self.show()

    def Okno(self, checked):
        if self.a is None:
            self.a = Gra()
        self.a.show()


    def closeEvent(self, event: QCloseEvent):
        zamkniecie = QMessageBox.question(self, "Zamykanie aplikacji", "Czy chcesz zamknac aplikacje?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if zamkniecie == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()





app = QApplication([])
interfejs = Interfejs()
app.exec()