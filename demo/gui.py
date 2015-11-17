import sys
from PyQt4 import QtCore, QtGui, uic
import getSVMscore
import getSVMscore2

qtCreatorFile = "test.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.upload.clicked.connect(self.selectFile)
        self.getperson.clicked.connect(self.getPersonality)


    def selectFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home')
        # self.ans_box.setText(QtGui.QFileDialog.getOpenFileName())


        f = open(fname, 'r')

        with f:
            data = f.read()

            self.ans_box.setText(data)

    def getPersonality(self):

        mytext = self.ans_box.toPlainText();

        # self.olabel.setText('4')
        # self.clabel.setText('6')
        ans= unicode(mytext)
        a,b,c,d,e = getSVMscore2.getscore(ans)
        if a[0] == 1.:
            self.elabel.setText('YES')
        else:
            self.elabel.setText('NO')

        if b[0] == 1.:
            self.nlabel.setText('YES')
        else:
            self.nlabel.setText('NO')

        if c[0] == 1.:
            self.alabel.setText('YES')
        else:
            self.alabel.setText('NO')

        if d[0] == 1.:
            self.clabel.setText('YES')
        else:
            self.clabel.setText('NO')

        if e[0] == 1.:
            self.olabel.setText('YES')
        else:
            self.olabel.setText('NO')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    

