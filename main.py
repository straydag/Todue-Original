import classes
import logger
import sys
import os
from datetime import datetime
from datetime import timedelta
from PyQt5.QtWidgets import (QTabWidget, QMessageBox, QComboBox, QGraphicsScene, QGraphicsView, QDateEdit, QTimeEdit, QDialog, QLineEdit, QFrame, QLabel, QSlider, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QGroupBox, QScrollArea, QSizePolicy)
from PyQt5.QtCore import (QTimer, Qt, QDate, QDateTime, QTime)
import uuid

logger.start()
user_tasks = classes.User_tasks()

print("Le task scheduling software has arrived")  # awesome ---> # YES :) ------>  #is this so ppl who view this understand its a meme? ----->      #meme
print("Oh boy i worked really hard on this, i can't wait to see it run without any bugs! :D")  # !!!!VERY IMPORTANT!!!!: I added a doge meme          <------    XDDDDDDDDDDDDDDDDDDDDDDD
print("UwU, i'm a pwogwammewr, pwease give me sheckles to suppowt my famiwy of 14 childwen :3")

class App(QWidget):

    #initialize all of the variables and call gui functions
    def __init__(self):
        super(App, self).__init__()

        self.setWindowTitle('to due')
        self.setGeometry(300, 200, 600, 600)
        self.create_task_area()
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.addLayout(self.create_header())
        self.vertical_layout.addWidget(self.tasks_area)
        self.show()

        self.refresh_tasks()

        timer = QTimer(self)
        timer.timeout.connect(self.countdown_update)
        timer.start(100)

    #create the header for the gui (i dont think it needs to be it's own function tbh, might change later)
    def create_header(self):

        header_layout = QHBoxLayout()
        btn_add_task = QPushButton('+')
        btn_add_task.setFixedSize(40, 40)
        btn_add_task.clicked.connect(lambda: TaskAddEditor('Add a task', 'Add', None))
        task_label = QLabel('Add Task')
        header_layout.addWidget(btn_add_task)
        header_layout.addWidget(task_label)

        sort_by_label = QLabel('Sort By')

        sort_by = QComboBox()
        sort_by.addItems(["Alphabetic", "Date Created", "Furthest Due Date", "Time Left"])
        sort_by.currentIndexChanged.connect(self.sort_by_func)
        header_layout.addStretch()
        header_layout.addWidget(sort_by_label)
        header_layout.addWidget(sort_by)

        return header_layout

    #calls backend sort functions
    def sort_by_func(self, choice):
        if choice == 0:
            print('sorting alphabetically')
            user_tasks.sort_alphabet()
        elif choice == 1:
            print('sorting by date created')
            user_tasks.sort_date_added()
        elif choice == 2:
            print('sorting by furthest due date')
            user_tasks.sort_time()
        elif choice == 3:
            print('sorting by amount of time left')
            user_tasks.sort_time_reverse()
        self.refresh_tasks()

    #create the task area for the gui, this will hold all of the tasks (probably doesn't need to be it's own function and can be made in the init_gui class)
    def create_task_area(self):

        #create a scroll area to hold tasks
        self.tasks_area = QScrollArea(self)
        self.tasks_area.setWidgetResizable(True)
        widget = QWidget()
        self.tasks_area.setWidget(widget)
        self.tasks_layout = QVBoxLayout(widget)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        logger.log("Draw GUI")

    #goes through the entire user_tasks list and creates gui tasks based of those
    def refresh_tasks(self):
    
        for task_num in range(self.tasks_layout.count()):
            self.tasks_layout.itemAt(task_num).widget().deleteLater()

        for task in user_tasks.tasks_list:
            self.tasks_layout.addWidget(Task(task.task_name, task.time_due, task.time_made, task.id_number))

    #updates all of the tasks timers at the same time
    def countdown_update(self):

        user_tasks.notify_task
        for task in range(self.tasks_layout.count()):
            try:
                self.tasks_layout.itemAt(task).widget().update_time()
            except:
                pass

class Task(QFrame):

    #initialze the Task class and all it's variables as well as create the gui
    def __init__(self, task_name, due_date, time_made, identifier):
        super(Task, self).__init__()
        self.setFrameStyle(1)

        self.due_date = due_date
        self.task_name = task_name
        self.identifier = identifier
        self.time_made = time_made

        self.creation_due_difference = (self.due_date - self.time_made).total_seconds()

        self.main_layout = QHBoxLayout()

        #create the left part of the task, this will be a horizontal layout with the name and the date
        self.name_and_date = QVBoxLayout()
        self.delete_and_edit = QHBoxLayout()
        self.delete = QPushButton('X')
        self.edit = QPushButton('/')
        self.delete.clicked.connect(self.button_click)
        self.delete.setFixedSize(25, 25)
        self.edit.clicked.connect(lambda: TaskAddEditor('Edit task', 'Edit', self.identifier))
        self.edit.setFixedSize(25, 25)
        self.delete_and_edit.addWidget(self.delete)
        self.delete_and_edit.addWidget(self.edit)
        self.delete_and_edit.addStretch()

        self.name = QLabel(self.task_name)
        self.date = QLabel(self.due_date.strftime("Due: %m/%d/%Y Time: %I:%M %p"))
        self.name_and_date.addWidget(self.name)
        self.name_and_date.addWidget(self.date)
        self.name_and_date.addLayout(self.delete_and_edit)
        self.main_layout.addLayout(self.name_and_date)
        self.main_layout.addStretch()

        #create all the countdowns
        countdowns = QGridLayout()
        countdowns.setColumnMinimumWidth(0, 60)
        countdowns.setColumnMinimumWidth(1, 60)
        self.time_til = (self.due_date - datetime.today())

        self.le_days = QLabel('D: 0')
        self.le_hours = QLabel('H: 0')
        self.le_minutes = QLabel('M: 0')
        self.le_seconds = QLabel('S: 0')

        countdowns.addWidget(self.le_days, 0, 0, Qt.AlignLeft)
        countdowns.addWidget(self.le_hours, 0, 1, Qt.AlignLeft)
        countdowns.addWidget(self.le_minutes, 1, 0, Qt.AlignLeft)
        countdowns.addWidget(self.le_seconds, 1, 1, Qt.AlignLeft)
        self.update_time()

        self.main_layout.addLayout(countdowns)
        self.setFixedHeight(100)

        self.setLayout(self.main_layout)
    
    #constantly updates the time until in days, hours, minutes ad seconds
    def update_time(self):

        time_til = (self.due_date - datetime.today())
        frame_width = self.frameSize().width()

        if time_til.days > -1:

            if(time_til.seconds == 1):
                user_tasks.notify_task(self.identifier, self.task_name + " is due")
            elif(time_til.total_seconds == 86400):
                user_tasks.notify_task(self.identifier, self.task_name + " is due in 1 day")
            elif(time_til.total_seconds == 600):
                user_tasks.notify_task(self.identifier, self.task_name + " is due in 10 minutes")
            elif(time_til.total_seconds == 3600):
                user_tasks.notify_task(self.identifier, self.task_name + " is due in 1 hour")

            user_tasks.notify_tasks()

            self.setStyleSheet(""" 
            QFrame.Task
            {
                background-color: rgba(70, 130, 180, 0.2);
                background-clip: padding;
                border-right-width: """ + str(frame_width - (time_til.total_seconds() * frame_width) // self.creation_due_difference) + """px;
            }
            """)
            self.le_days.setText("D: " + str(time_til.days))
            self.le_hours.setText("H: " + str((time_til.days * 24 + time_til.seconds) // 3600))
            self.le_minutes.setText("M: " + str((time_til.seconds % 3600) // 60))
            self.le_seconds.setText("S: " + str(time_til.seconds % 60))
        else:
            self.setStyleSheet('QFrame.Task {background-color: transparent;}')

    #delete button connect
    def button_click(self):

        sender = self.sender()
        if sender.text() == "X":
            user_tasks.delete_task(self.identifier)
            le_window.refresh_tasks()


class TaskAddEditor(QDialog):

    #initialize everything
    def __init__(self, dialog_name, button_name, identifier):
        super(TaskAddEditor, self).__init__()

        self.dialog_name = dialog_name
        self.button_name = button_name
        self.identifier = identifier

        self.setGeometry(50, 50, 300, 250)

        self.le_tabs = QTabWidget()
        self.le_tabs.tab_1 = QWidget()
        self.le_tabs.tab_2 = QWidget()
        
        self.le_tabs.addTab(self.le_tabs.tab_1, "basic info")
        self.le_tabs.addTab(self.le_tabs.tab_2, "notifications")

        self.tab_1()
        self.tab_2()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.le_tabs)

        buttons = QHBoxLayout()

        button_ok = QPushButton(self.button_name)
        button_close = QPushButton("Cancel")
        button_ok.clicked.connect(self.dialog_button_press)
        button_close.clicked.connect(self.dialog_cancel_press)
        buttons.addWidget(button_ok)
        buttons.addWidget(button_close)

        main_layout.addLayout(buttons)

        self.setLayout(main_layout)

        self.setWindowTitle(dialog_name)
        self.exec_()

    #tab 1
    def tab_1(self):

        #main layout
        layout = QVBoxLayout()

        task_name = QLabel('Task Name')
        due_date = QLabel('Due Date')
        due_time = QLabel('Due Time')

        if(self.button_name == "Add"):
            self.task_name_input = QLineEdit()
            self.due_date_input = QDateEdit()
            self.due_date_input.setMinimumDate(QDate.currentDate())
            self.due_time_input = QTimeEdit()
        else:
            for task in user_tasks.tasks_list:
                if task.id_number == self.identifier:
                    self.task_name_input = QLineEdit(task.task_name)
                    self.due_date_input = QDateEdit(task.time_due.date())
                    self.due_date_input.setMinimumDate(QDate.currentDate())
                    self.due_time_input = QTimeEdit(task.time_due.time())

        layout.addWidget(task_name)
        layout.addWidget(self.task_name_input)
        layout.addWidget(due_date)
        layout.addWidget(self.due_date_input)
        layout.addWidget(due_time)
        layout.addWidget(self.due_time_input)
        layout.addSpacing(20)

        self.le_tabs.tab_1.setLayout(layout)

    #tab 2
    def tab_2(self):

        layout = QVBoxLayout()

        page_name = QLabel('Notification Settings')
        layout.addWidget(page_name)

        add_notification_area = QHBoxLayout()

        description = QLabel('Remind me everyday at: ')
        self.time_input = QTimeEdit()
        add_notification = QPushButton('+')
        add_notification.setFixedSize(30, 30)
        add_notification.clicked.connect(self.add_notification)

        add_notification_area.addWidget(description)
        add_notification_area.addWidget(self.time_input)
        add_notification_area.addWidget(add_notification)
    
        layout.addLayout(add_notification_area)

        your_notifications = QLabel('Your Notifications:')

        layout.addWidget(your_notifications)

        #create a scroll area to hold notifications
        notifications_area = QScrollArea(self)
        notifications_area.setWidgetResizable(True)
        widget = QWidget()
        notifications_area.setWidget(widget)
        self.notifications_layout = QVBoxLayout(widget)
        notifications_area.setAlignment(Qt.AlignTop)
        self.notifications_layout.setAlignment(Qt.AlignTop)
        
        layout.addWidget(notifications_area)

        if self.identifier is not None:
            le_task = user_tasks.get_task(self.identifier)
            for notification_date in le_task.notifications:
                self.notifications_layout.addWidget(Notification(datetime.strptime(notification_date, "%I:%M:%S %p")))

        self.le_tabs.tab_2.setLayout(layout)

    #adds a notification to the layout of notifications
    def add_notification(self):

        for notification in range(self.notifications_layout.count()):
            if datetime.strptime(self.notifications_layout.itemAt(notification).widget().time_input, "%I:%M %p").time() > self.time_input.time().toPyTime():
                self.notifications_layout.insertWidget(notification, Notification(self.time_input.time().toPyTime()))
                return 
            elif (self.notifications_layout.itemAt(notification).widget().time_input) == self.time_input.time().toPyTime().strftime('%I:%M %p'):
                error = QMessageBox()
                error.setText("please enter a different time")
                error.exec_()
                return 
            
        self.notifications_layout.addWidget(Notification(self.time_input.time().toPyTime()))

    #when add is pressed
    def dialog_button_press(self):
        if(input_error_box(self.due_time_input, self.due_date_input, self.task_name_input)):

            notification_dates = []
            for notification in range(self.notifications_layout.count()):
                notification_dates.append(datetime.strptime(self.notifications_layout.itemAt(notification).widget().time_input, "%I:%M %p").strftime("%I:%M:%S %p"))

            if(self.button_name == 'Add'):
                user_tasks.add_task(self.task_name_input.text(), datetime.combine(self.due_date_input.date().toPyDate(), self.due_time_input.time().toPyTime()), datetime.today(), str(uuid.uuid4()), notification_dates)
            else:
                user_tasks.edit_task(self.identifier, self.task_name_input.text(), datetime.combine(self.due_date_input.date().toPyDate(), self.due_time_input.time().toPyTime()), notification_dates)

            self.reject()
            le_window.refresh_tasks()
    
    #used in the input window and closes it
    def dialog_cancel_press(self):
        self.reject()

class Notification(QFrame):

    #initialize everything
    def __init__(self, notification_time):
        super(Notification, self).__init__()
        self.setFrameStyle(1)
        main_layout = QHBoxLayout()
        self.time_input = notification_time.strftime("%I:%M %p")
        test2 = QLabel(self.time_input)
        test3 = QPushButton('-')
        test3.setFixedSize(32, 22)
        test3.clicked.connect(lambda: self.deleteLater())

        main_layout.addWidget(test2)
        main_layout.addWidget(test3)

        self.setFixedHeight(45)
        self.setLayout(main_layout)

#functions for an error box which pops up when the users input date/time is less that the current date/time or the name is empty
def input_error_box(due_time_input, due_date_input, task_name_input):

    if(due_time_input.time() < QTime.currentTime() and due_date_input.date() == QDate.currentDate() or task_name_input.text() == ''):
        error = QMessageBox()
        error.setText("Error")
        if(task_name_input.text() == ''):
            error.setInformativeText("Please enter a task name")
        else:
            error.setInformativeText("please enter a future date")
            error.setWindowTitle("Error")
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    else:
        return True


application = QApplication(sys.argv)
le_window = App()
sys.exit(application.exec_())

