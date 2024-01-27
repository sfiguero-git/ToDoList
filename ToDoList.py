import sys
import json
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPalette, QColor


'''
  _______          _____          _      _     _   
 |__   __|        |  __ \        | |    (_)   | |  
    | | ___ ______| |  | | ___   | |     _ ___| |_ 
    | |/ _ \______| |  | |/ _ \  | |    | / __| __|
    | | (_) |     | |__| | (_) | | |____| \__ \ |_ 
    |_|\___/      |_____/ \___/  |______|_|___/\__|

    Saul Figueroa

    This is an app that displays a task list which can be updated by adding new tasks, deleting old ones, and clearing the list.
    The list is automatically saved as tasks are added or removed.                                                                                      
'''

# Creating a QWidget class for the To-Do List application
class ToDoList(QWidget):
    def __init__(self):
        super(ToDoList, self).__init__()

        # Setting the window palette to a light blue color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 180, 220, 200))
        self.setPalette(palette)

        # Setting the window title and initializing the task list
        self.setWindowTitle("My To-Do List")
        self.Tasks = []

        # Creating the main layout for the application
        self.Layout = QVBoxLayout(self)

        # Creating input field, buttons, and task list
        self.InputField = QLineEdit()
        self.AddButton = QPushButton("Add Task")
        self.DeleteButton = QPushButton("Delete Selected Task")
        self.ClearButton = QPushButton("Clear List")
        self.TaskList = QListWidget()
        self.TaskList.setSelectionMode(QListWidget.SingleSelection)

        # Adding widgets to the layout
        self.Layout.addWidget(self.InputField)
        self.Layout.addWidget(self.AddButton)
        self.Layout.addWidget(self.DeleteButton)
        self.Layout.addWidget(self.ClearButton)
        self.Layout.addWidget(self.TaskList)

        # Connecting button actions to corresponding methods
        self.AddButton.clicked.connect(self.AddTask)
        self.DeleteButton.clicked.connect(self.DeleteTask)
        self.ClearButton.clicked.connect(self.AskClearConfirmation)

        # Setting initial window dimensions, position, and transparency
        self.setGeometry(0, 0, 500, 800)
        screenGeometry = app.desktop().screenGeometry()
        self.move((screenGeometry.width() - self.width()) // 2, (screenGeometry.height() - self.height()) // 2)
        self.setWindowOpacity(0.95)

        # Loading tasks from file on application startup
        self.LoadTasks()

    # Method to add a task to the list
    def AddTask(self):
        taskText = self.InputField.text()
        if taskText:
            task = {"text": taskText, "completed": False}
            self.Tasks.append(task)
            item = QListWidgetItem(taskText)
            self.TaskList.addItem(item)
            self.InputField.clear()
            self.SaveTasks()

    # Method to delete selected task(s) from the list
    def DeleteTask(self):
        selectedItems = self.TaskList.selectedItems()
        for item in selectedItems:
            row = self.TaskList.row(item)
            self.Tasks.pop(row)
            self.TaskList.takeItem(row)
        self.SaveTasks()

    # Method to ask for confirmation before clearing all tasks
    def AskClearConfirmation(self):
        reply = QMessageBox.question(self, 'Please Confirm', 'Are you sure you want to clear all tasks?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ClearTasks()

    # Method to clear all tasks
    def ClearTasks(self):
        self.TaskList.clear()
        self.Tasks.clear()
        self.SaveTasks()

    # Method to save tasks to a JSON file
    def SaveTasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.Tasks, file)

    # Method to load tasks from a JSON file
    def LoadTasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.Tasks = json.load(file)
            for task in self.Tasks:
                item = QListWidgetItem(task["text"])
                self.TaskList.addItem(item)
        except FileNotFoundError:
            pass

# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoList()
    window.show()
    sys.exit(app.exec_())
