
import sys
import tkinter, sys, json
from tkinter import messagebox
from random import randint
from pathlib import Path
import pickle
import os
import subprocess
import string
import re

def contruct_user_code(user_name, user_lastname):
    print("Contructor de codigo para usuarios")

    var_name = str(user_name)
    var_lastname = str(user_lastname)
    var_code = ""
    if not var_name or not var_lastname:
        print ('Debes introducir Nombre y Apellido')
    else:
        random = randint(10000,99999)
        #code = self.api.genCode(nombre,apellido)
        var_code = str(var_name[0] + var_lastname[0] + str(random))
        print("Your code is: " + var_code)
    path = str(Path().absolute())
    filename = "Users.txt"
    my_file = Path(path + filename)

    if not var_name or not var_lastname or not var_code:
        print ('Debes introducir Nombre y Apellido')
    else:
        try:
            my_abs_path = my_file.resolve(strict=True)
        except FileNotFoundError:  # doesn't exist
            file = open("Users.txt", "a") 
            file.write(var_name + " " + var_lastname + " " + var_code + "\n") 
            file.close() 
        else:  # exists
            file = open("Users.txt", "w") 
            file.write(var_name + " " + var_lastname + " " + var_code + "\n") 
            file.close() 

def view_all_users():
    parent = tkinter.Tk() # Create the object
    parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
    parent.withdraw() # Hide the window as we do not want to see this one
    file = open("Users.txt", "r")
    #messagetext = [line.rstrip() for line in open('Users.txt')]
    print("Total Users: ")
    print([line.rstrip() for line in open('Users.txt')])
    #messagetext = file.readlines()
    #message =  messagetext
    file.close() 
    #messagebox.showinfo(message=message, title="Usuarios")