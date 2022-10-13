import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from Ui_front_end import Ui_Dialog
from functions import calc_soiling_rate

file_name = ""

class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.openFile.clicked.connect(self.clicky)
        self.ui.SR.clicked.connect(self.SR_calc)
        self.ui.SR.clicked.connect(self.grapher)


    def clicky(self):
        fname = QFileDialog.getOpenFileName(self, "Open File","", "All Files (*)")
        if fname:
            if "eds_data" in str(fname):
                global file_name
                file_name = fname[0]
                print(file_name)
                self.ui.CSV_label.setText("Valid")
            else:
                self.ui.CSV_label.setText("Not Valid!!")

    def SR_calc(self):
        calc_soiling_rate(file_name,self.ui.CSV_label.text())
    def grapher(self):
        pass
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
