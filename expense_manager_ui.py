from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, Ui_MainWindow):
        Ui_MainWindow.setObjectName("Ui_MainWindow")
        Ui_MainWindow.resize(400, 500)
        Ui_MainWindow.setMinimumSize(QtCore.QSize(400, 500))
        Ui_MainWindow.setMaximumSize(QtCore.QSize(400, 500))
        self.centralwidget = QtWidgets.QWidget(parent=Ui_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        

        self.expense_list = QtWidgets.QListWidget(parent=self.centralwidget)
        self.expense_list.setGeometry(QtCore.QRect(10, 10, 221, 481))
        self.expense_list.setObjectName("expense_list")
        

        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(240, 10, 151, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        

        self.add_category_btn = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.add_category_btn.setObjectName("add_category_btn")
        self.verticalLayout.addWidget(self.add_category_btn)
        

        self.add_expense_btn = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.add_expense_btn.setObjectName("add_expense_btn")
        self.verticalLayout.addWidget(self.add_expense_btn)
        

        self.delete_selected = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.delete_selected.setObjectName("delete_selected")
        self.verticalLayout.addWidget(self.delete_selected)
        

        self.export_to_csv = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.export_to_csv.setObjectName("export_to_csv")
        self.verticalLayout.addWidget(self.export_to_csv)
        
        Ui_MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(Ui_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Ui_MainWindow)

    def retranslateUi(self, Ui_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Ui_MainWindow.setWindowTitle(_translate("Ui_MainWindow", "Expense Manager"))
        self.add_category_btn.setText(_translate("Ui_MainWindow", "Добавить категорию"))
        self.add_expense_btn.setText(_translate("Ui_MainWindow", "Добавить трату"))
        self.delete_selected.setText(_translate("Ui_MainWindow", "Удалить элемент"))
        self.export_to_csv.setText(_translate("Ui_MainWindow", "Экспорт в CSV"))
