import time
from datetime import datetime
import timeit
import logger 
import utils  
import os                                          
import json
import random


#this is used for storing a list of tasks as well as adding them
class User_tasks(object):
# whole init needs redoing with main for the save functionality
    def __init__(self, task_list):                                           #constructor
        self.tasks_list = list(task_list)                                      #the tasks list which holds an array of tasks - for starting, this needs to be initialized if save file found
        logger.log("User_Tasks Created")

        if self.tasks_list: # checks if the task has anything to open from the save file
            self.deserialize()

    def add_task(self, task_name="Untitled", time_due="Jan 1, 2099", id_number=random.randint(0, 1000)):  # adds a task with information passed into the parameters

        task_to_add = Task(task_name, time_due, id_number)
        self.tasks_list.append({"task": task_to_add, "id": id_number})

        logger.log("Adding Task")

    def display_tasks(self):                                      #displays all of the tasks and their information

        for task in self.tasks_list:
            task.display_task()

        logger.log("Displaying Tasks")
    
    def edit_task(self, task_id, name_change, date_change):     # calls the edit_name and edit_due_date functions with parameters passed in

        for task in self.tasks_list:
            if task.id_number == task_id:

                if name_change:
                    task.edit_name(name_change)

                    logger.log("Changing Name")

                if date_change:
                    task.edit_due_date(date_change)

                    logger.log("Changing Date")
    
    def delete_task(self, task_id):
        if task_id  in self.tasks_list:
            del self.tasks_list[task_id]

    def serialize(self):

        serialized_task_list = []

        for task in self.tasks_list:
            serialized_task_list.append(task.serialize())
        self.json_dump = json.dumps(serialized_task_list)

        logger.log("Serialized")   
    
    def save(self):

        location = os.path.dirname(os.path.abspath(__file__))
        saver = os.path.join(location, "save_files.txt")
        with open(saver, "w+") as handle:
            print(self.json_dump, file=handle, end="")

        logger.log("User Data Saved")
    
    def deserialize(self):
        # write the json.loads(string) on the main.py under loading at the bottom
        logger.log("User Data Retrieved")
        task_temp = []

        for item in self.tasks_list:
            task = Task(item["task name"], item["due date"], item["id number"])
            task_temp.append(task)

        self.tasks_list = task_temp


#a task class which holds information about it's name as well as it's due date
class Task(object):

    def __init__(self, name="Untitled", due_date="Jan 1, 2099", id_number=random.randint(0, 1000)):  # constructor

        self.name = name                                          #name of the task
        self.due_date = Timer(due_date)  # datetime object of when it's due
        self.id_number  = id_number                         

    def edit_name(self, new_name):                                #edits the string name of the task and changes it to the name_add passed in
        self.name = new_name

    def edit_due_date(self, new_date):                            #edits the due date of the task which is a datetime object
        self.due_date = new_date
    
    def display_task(self):                                       #displays the task -- This will be eventually passed to the display class

        print("task name: " + str(self.name))
        print("due date: " + str(self.due_date.date))
        print("time left: " + str(self.due_date.date_diff))

    def serialize(self):
        return {"task name":self.name, 
                "due date":self.due_date.serialize(),
                "id number":self.id_number}


class Timer(object):

 
    def __init__(self, date):
        self.date = date
        self.convert()
    def convert(self):
        # converts the string to a datetime object
        format = "%Y-%m-%d %H:%M:%S"
        self.date = datetime.strptime(self.date, format)

    def serialize(self):
        return utils.datetime_to_string_for_save(self.date)

    def date_diff(self):
        now = datetime.now()
        time_since = self.date - now
        return time_since

    def timer_display(self):
        # use for the countodown display
        total_mins = int(self.date_diff().total_seconds() / 60)
        return total_mins


#   test      # 
# x = Timer("2019-07-12 9:00:00")
# print(x.timer_display())
