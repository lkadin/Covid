from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, states=None, counties=None):
        self.states = states
        self.counties = counties
        rowstart = 10
        MainWindow.setObjectName(_fromUtf8("Covid Analysis"))
        MainWindow.resize(669, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.rb1 = QtWidgets.QRadioButton(self.centralwidget)
        self.rb1.setGeometry(QtCore.QRect(10, rowstart + 30, 250, 20))
        self.rb1.toggled.connect(self.county_selected)
        self.rb2 = QtWidgets.QRadioButton(self.centralwidget)
        self.rb2.setGeometry(QtCore.QRect(150, rowstart + 30, 250, 20))
        self.rb2.toggled.connect(self.state_selected)
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(10, rowstart, 65, 16))
        self.label1.setObjectName(_fromUtf8("label1"))

        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(140, rowstart, 85, 16))
        self.label2.setObjectName(_fromUtf8("label2"))

        self.cb1 = QtWidgets.QComboBox(self.centralwidget)
        self.cb1.setGeometry(QtCore.QRect(200, rowstart, 175, 16))

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(9, 321, 158, 25))
        self.widget.setObjectName(_fromUtf8("widget"))

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(10, 100, 50, 25)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.results = QtWidgets.QTableWidget(10, 6, self.centralwidget)
        self.results.setGeometry(10, 200, 700, 500)
        self.results.hide()

        self.retranslateUi(MainWindow, states, counties)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, states=None, counties=None):
        MainWindow.setWindowTitle(_translate("MainWindow", "Covid Analysis", None))
        self.label1.setText(_translate("MainWindow", "County", None))
        self.label2.setText(_translate("MainWindow", "State", None))
        self.pushButton.setText(_translate("MainWindow", "Go", None))

    def state_selected(self):
        self.cb1.clear()
        for state in self.states:
            self.cb1.addItem(state)

    def county_selected(self):
        self.cb1.clear()
        for county in self.counties:
            self.cb1.addItem(county)

    def display_results(self, results, header_labels=None):
        self.results.setHorizontalHeaderLabels(header_labels
                                               )
        for row, line in enumerate(results):
            for col, data in enumerate(line):
                self.results.setItem(row, col, QtWidgets.QTableWidgetItem(data))
                self.results.show()
