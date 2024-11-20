import sys
import json
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QListWidget, QPushButton, QInputDialog, QMessageBox, QListWidgetItem,
    QFileDialog
)
from PyQt6.QtCore import Qt
from expense_manager_ui import setup_ui



class ExpenseManager(QMainWindow):
    def __init__(self):
        super().__init__()

        setup_ui(self)

        self.expense_limit = 0
        self.current_spent = 0
        self.data = {}
        self.selection_mode = False
        self.load_data()


        self.search_input.textChanged.connect(self.perform_search)
        self.add_category_button.clicked.connect(self.add_category)
        self.add_expense_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_selected)
        self.edit_item_button.clicked.connect(self.edit_item)
        self.analyze_button.clicked.connect(self.set_limit)
        self.calculate_totals_button.clicked.connect(self.calculate_total_per_category)
        self.import_csv_button.clicked.connect(self.import_from_csv)
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.toggle_selection_mode_button.clicked.connect(self.toggle_selection_mode)
        self.list_widget.itemClicked.connect(self.show_expense_details)
        self.sort_button.clicked.connect(self.sort_expenses)
        self.reset_button.clicked.connect(self.reset_data)

        self.toggle_selection_mode()
        self.toggle_selection_mode()
        self.update_list()

        self.selection_mode = False
        self.toggle_selection_mode_button.setText("Режим выделения: ВЫКЛ")
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.NoSelection)




    def set_limit(self):
        """
        Установить лимит трат и сбросить текущую сумму.
        """
        current_limit = getattr(self, "expense_limit", 0)
        current_spent = getattr(self, "current_spent", 0)

        dialog = QInputDialog(self)
        dialog.setGeometry(650, 250, 300, 400)
        dialog.setWindowTitle("Лимит трат")
        dialog.setLabelText(
            f"Текущий лимит: {current_limit:.2f} ₽\n"
            f"Сумма трат с момента сброса: {current_spent:.2f} ₽\n\n"
            "Введите новый лимит:"
        )
        dialog.setTextValue(f"{current_limit:.2f}")
        dialog.setInputMode(QInputDialog.InputMode.DoubleInput)
        dialog.setDoubleMaximum(1e9)


        reset_button = QPushButton("Сбросить траты", dialog)
        reset_button.setGeometry(200, 50, 100, 25)
        reset_button.clicked.connect(lambda: self.reset_expenses(dialog))

        if dialog.exec() == QInputDialog.DialogCode.Accepted:
            new_limit = dialog.doubleValue()
            if new_limit > 0:
                self.expense_limit = new_limit
                QMessageBox.information(self, "Успех", f"Лимит установлен: {new_limit:.2f} ₽")
            else:
                self.expense_limit = new_limit
                QMessageBox.information(self, "Успех", "Лимит сброшен.")

    def reset_expenses(self, dialog):
        """
        Сбрасывает текущую сумму трат, не изменяя список трат.
        """
        self.current_spent = 0
        QMessageBox.information(self, "Успех", "Текущая сумма трат сброшена.")
        dialog.close()


    def count_expences(self, summ):
        """
        Подсчитывает траты на данный момент
        """
        self.current_spent += summ
        if self.expense_limit != 0 and self.current_spent > self.expense_limit:
            QMessageBox.warning(self, "Превышен лимит трат", "Вы превысили установленный лимит трат.")



    def add_category(self):
        """
        Добавление категории
        """
        category, ok = QInputDialog.getText(self, "Добавить категорию", "Введите название категории:")
        if ok and category.strip():
            if category in self.data:
                QMessageBox.warning(self, "Ошибка", "Такая категория уже существует.")
            else:
                self.data[category] = []
                self.update_list()

    def add_expense(self):
        """
        Добавление траты
        """
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
            self.update_list()
            self.count_expences(expense)

    def update_list(self):
        """
        Обновление списка
        """
        self.list_widget.clear()
        for category, expenses in self.data.items():
            category_item = QListWidgetItem(category)
            category_item.setFlags(category_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.list_widget.addItem(category_item)
            for expense, name in expenses:
                expense_item = QListWidgetItem(f"    {expense:.2f} ₽")
                expense_item.setFlags(expense_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                expense_item.setToolTip(name)
                self.list_widget.addItem(expense_item)

    def delete_selected(self):
        """
        Удаление элементов
        """
        selected_items = self.list_widget.selectedItems()
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
        self.update_list()

    def show_expense_details(self, item):
        if self.selection_mode or "₽" not in item.text():
            return
        QMessageBox.information(self, "Детали траты", item.toolTip())

    def toggle_selection_mode(self):
        """
        Режим выделения
        """
        self.selection_mode = not self.selection_mode
        self.toggle_selection_mode_button.setText("Режим выделения: ВКЛ" if self.selection_mode else "Режим выделения: ВЫКЛ")
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection if self.selection_mode else QListWidget.SelectionMode.NoSelection)

    def calculate_total_per_category(self):
        totals = {category: sum(expense[0] for expense in expenses) for category, expenses in self.data.items()}
        message = "\n".join([f"{category}: {total:.2f} ₽" for category, total in totals.items()])
        QMessageBox.information(self, "Суммы по категориям", message)

    def export_to_csv(self):
        """
        Экспорт в csv файл
        """
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

    def edit_item(self):
        """
        Редактирование объектов
        """
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) != 1:
            QMessageBox.warning(self, "Ошибка", "Выберите ровно один элемент для редактирования.")
            return
        item = selected_items[0]
        text = item.text().strip()
        if text in self.data:
            new_name, ok = QInputDialog.getText(self, "Редактировать категорию", "Новое название:", text=text)
            if ok and new_name.strip():
                self.data[new_name] = self.data.pop(text)
                self.update_list()
        else:
            for category, expenses in self.data.items():
                for i, (expense, name) in enumerate(expenses):
                    if f"{expense:.2f} ₽" in text:
                        new_expense, ok = QInputDialog.getDouble(self, "Редактировать трату", "Новая сумма:", value=expense)
                        if not ok:
                            return
                        new_name, ok = QInputDialog.getText(self, "Редактировать трату", "Новое описание:", text=name)
                        if ok:
                            self.data[category][i] = (new_expense, new_name.strip())
                            self.update_list()
                            return

    def perform_search(self, query):
        """
        Поиск по тратам и категориям
        """
        query = query.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(query not in item.text().lower() and query not in item.toolTip().lower())

    def save_data(self):
        """
        Сохранить данные в файл.
        """
        save_object = {
            "data": self.data,
            "expense_limit": getattr(self, "expense_limit", 0),
            "current_spent": getattr(self, "current_spent", 0),
        }
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(save_object, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """
        Загрузить данные из файла.
        """
        try:
            with open("expenses.json", "r", encoding="utf-8") as f:
                loaded_object = json.load(f)
                self.data = loaded_object.get("data", {})
                self.expense_limit = loaded_object.get("expense_limit", 0)
                self.current_spent = loaded_object.get("current_spent", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}
            self.expense_limit = 0
            self.current_spent = 0


    def closeEvent(self, event):
        self.save_data()
        super().closeEvent(event)


    def import_from_csv(self):
        """
        Импорт данных из CSV.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Импорт из CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) < 3:
                        continue
                    category, expense, name = row[0], float(row[1]), row[2]
                    if category not in self.data:
                        self.data[category] = []
                    self.data[category].append((expense, name))
            QMessageBox.information(self, "Успех", "Данные успешно импортированы!")
            self.update_list()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось импортировать данные: {e}")

    def delete_all_data(self):
        """
        Удалить все данные.
        """
        confirm = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить все данные?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.data.clear()
            self.update_list()
            QMessageBox.information(self, "Успех", "Все данные удалены!")

    def calculate_average_expense(self):
        """
        Подсчёт среднего расхода на трату.
        """
        total_expenses = sum(expense[0] for expenses in self.data.values() for expense in expenses)
        num_expenses = sum(len(expenses) for expenses in self.data.values())
        average = total_expenses / num_expenses if num_expenses > 0 else 0
        QMessageBox.information(self, "Средний расход", f"Средний расход: {average:.2f} ₽")


    def sort_expenses(self):
        """
        Сортировать траты по сумме.
        """
        for category in self.data.keys():
            self.data[category].sort(reverse=True, key=lambda x: x[0])
        QMessageBox.information(self, "Успех", "Траты отсортированы по убыванию суммы!")
        self.update_list()

    def total_expense(self):
        """
        Рассчитать общую сумму расходов.
        """
        total = sum(expense[0] for expenses in self.data.values() for expense in expenses)
        QMessageBox.information(self, "Общая сумма", f"Общая сумма расходов: {total:.2f} ₽")

    def reset_data(self):
        """
        Сбросить данные к изначальному состоянию.
        """
        confirm = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите сбросить данные?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.data = {}
            self.expense_limit = 0
            self.current_spent = 0
            self.update_list()
            QMessageBox.information(self, "Сброс данных", "Данные сброшены к изначальному состоянию.")


if __name__ == "__main__":
    ap = QApplication(sys.argv)
    wd = ExpenseManager()
    wd.show()
    sys.exit(ap.exec())
