import datetime


#this is used for storing a list of tasks as well as adding them
class Tasks(object):

    def __init__(self):                                           #constructor
        self.tasks_list = []                                      #the tasks list which holds an array of tasks
    
    def add_task(self, task_name="Untitled", time_due="Jan 1, 2099"):  # adds a task with information passed into the parameters

        task_to_add = Task(task_name, time_due)
        self.tasks_list.append(task_to_add)

    def display_tasks(self):                                      #displays all of the tasks and their information

        for task in self.tasks_list:
            task.display_task()
    
    def edit_task(self):                         # calls the edit_name and edit_due_date functions with parameters passed in
        selected_name = input("Which task do you want to change?")
        edit = input("Do you want to rename or change the due date?")
        if edit.lower().strip() == "rename":
            rename = input("What is the new name?")
            selected_name.edit_name(rename)
        else:
            date = input("When is it due?")
            selected_name.edit_due_date(date)


#a task class which holds information about it's name as well as it's due date
class Task(object):

    def __init__(self, name="Untitled", due_date="Jan 1, 2099"):                                           #constructor

        self.name = name                                          #name of the task
        self.due_date = due_date                                  #datetime object of when it's due

    def edit_name(self, new_name):                                #edits the string name of the task and changes it to the name_add passed in
        self.name = new_name

    def edit_due_date(self, new_date):                            #edits the due date of the task which is a datetime object
        self.due_date = new_date
    
    def display_task(self):                                       #displays the task -- This will be eventually passed to the display class
        print(self.name)
        print(self.due_date)

