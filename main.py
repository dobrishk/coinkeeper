import sys
import json
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
from PyQt6.QtWidgets import QInputDialog
from expense_manager_ui import Ui_MainWindow

class ExpenseManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Мои расходы")
        
        self.data = {} 

        self.add_category_btn.clicked.connect(self.add_category)
        self.add_expense_btn.clicked.connect(self.add_expense)
        self.delete_selected.clicked.connect(self.delete_selected_item)
        self.export_to_csv.clicked.connect(self.export_to_csv_item)

        self.load_data()

    def load_data(self):
        """Загрузка данных из файла."""
        try:
            with open("expenses.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

        self.refresh_list()

    def save_data(self):
        """Сохранение данных в файл."""
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def refresh_list(self):
        """Обновление списка на экране."""
        self.expense_list.clear()
        for category, expenses in self.data.items():
            summ = sum(x[0] for x in expenses)
            category += f'  |   {summ:.2f} ₽'
            category_item = QListWidgetItem(category)
            self.expense_list.addItem(category_item)
            for expense, name in expenses:
                expense_item = QListWidgetItem(f"    {expense:.2f} ₽")
                expense_item.setToolTip(name)
                self.expense_list.addItem(expense_item)

    def add_category(self):
        """Добавление новой категории."""
        category, ok = QInputDialog.getText(self, "Добавить категорию", "Введите название категории:")
        if ok and category.strip():
            if category in self.data:
                QMessageBox.warning(self, "Ошибка", "Такая категория уже существует.")
            else:
                self.data[category] = []
                self.save_data() 
                self.refresh_list()

    def add_expense(self):
        """Добавление новой траты."""
        if not self.data:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте хотя бы одну категорию.")
            return

        category, ok = QInputDialog.getItem(self, "Добавить трату", "Выберите категорию:", list(self.data.keys()), editable=False)
        if ok and category:
            expense, ok = QInputDialog.getDouble(self, "Добавить трату", "Введите сумму траты:", min=0)
            if not ok:
                return
            name, ok = QInputDialog.getText(self, "Добавить трату", "Введите название траты:")
            name = name.strip() if ok and name.strip() else "Без названия"
            self.data[category].append((expense, name))
            self.save_data() 
            self.refresh_list()

    def delete_selected_item(self):
        """Удаление выбранных элементов."""
        selected_items = self.expense_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите элементы для удаления.")
            return

        for item in selected_items:
            text = item.text().strip()
            if text in self.data:
                del self.data[text]
            else: 
                for category, expenses in self.data.items():
                    for expense in expenses:
                        if f"{expense[0]:.2f} ₽" in text:
                            self.data[category].remove(expense)
                            break
        self.save_data()  # Сохранить данные после удаления
        self.refresh_list()

    def export_to_csv_item(self):
        """Экспорт данных в CSV."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Экспорт в CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
        with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Категория", "Сумма", "Описание"])
            for category, expenses in self.data.items():
                for expense, name in expenses:
                    writer.writerow([category, expense, name])
        QMessageBox.information(self, "Успех", "Данные экспортированы в CSV!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wd = ExpenseManager()
    wd.show()
    sys.exit(app.exec())