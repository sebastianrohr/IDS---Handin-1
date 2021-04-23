import npyscreen
from npyscreen.wgtitlefield import TitleText
import json 
import requests
import random
import pyttsx3
import logging as log

log.basicConfig(filename='Kopi.log', filemode= 'w' , encoding='utf-8', level=log.DEBUG, format='%(asctime)s %(message)s') 

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', first_form) 
        
class first_form(npyscreen.ActionForm):
    recipe_list = []

    def create(self):
        self.add(npyscreen.TitleText, w_id="ingredientstextfield", name="Enter your ingredients:", rely= 1)
        self.add(npyscreen.ButtonPress, name="See course", when_pressed_function=self.ingredientsbtn_press, rely= 3) 
        self.add(npyscreen.TitleText, w_id="coursetextfield", name="Enter your course:", rely= 5)
        self.add(npyscreen.ButtonPress, name="See ingredients", when_pressed_function=self.coursebtn_press, rely= 7)
        self.add(npyscreen.ButtonPress, name="Hear ingredients", when_pressed_function=self.readbtn_press, rely = 7, relx = 20)
        self.add(npyscreen.ButtonPress, name="Read & save log", when_pressed_function=self.logbtn_press, rely = 7, relx=39)    

        
    def ingredient_information_def(self):
        get_ingredients = self.get_widget("coursetextfield").value
        URL = "http://www.recipepuppy.com/api/?q=" + get_ingredients
        get_information = requests.get(url = URL)
        ingredient_information = get_information.json()
        return ingredient_information

    def format_input(self, text):
        new_text = ''
        for letter in text:
            if letter != ' ' and letter != '-' and letter != '/' and letter != '.':
                new_text += letter
            else:
                new_text += ','
        return new_text

    def ingredientsbtn_press(self): #Displays recipes based on given ingredients
        get_recipe = self.get_widget("ingredientstextfield").value
        URL = "http://www.recipepuppy.com/api/?i=" + get_recipe
        get_information = requests.get(url = URL)
        recipe_information = get_information.json()
        recipe_str = ""
        for recipe in recipe_information['results']:
           recipe_str += "\n" + recipe['title']
        recipe_str1 = self.format_input(recipe_str)
        npyscreen.notify_confirm(recipe_str1, title="You can make these different courses", wrap=True, wide=True, editw=1)

    def coursebtn_press(self): #Searches for recipes and displays ingredients
        overall_ingredients = self.ingredient_information_def()
        ingredient_str = "\n" + overall_ingredients['results'][0]['ingredients']
        npyscreen.notify_confirm(ingredient_str, title="You need these ingredients for the course '" + overall_ingredients['results'][0]['title'] + "':", wrap=True, wide=True, editw=1)
        if overall_ingredients['results'][0]['title'] not in first_form.recipe_list: #Avoids duplications og already saved recipes
            first_form.recipe_list.append(overall_ingredients['results'][0]['title'])
            
    def readbtn_press(self): #Reads ingredients out loud
        overall_ingredients = self.ingredient_information_def()
        ingredient_str = "\n" + overall_ingredients['results'][0]['ingredients']
        message = "You need these ingredients for the course '" + overall_ingredients['results'][0]['title'] + "':" + ingredient_str
        tts = pyttsx3.init()         #Initiation of speaker
        tts.say(message)             #Speaker message
        tts.runAndWait()            
        if overall_ingredients['results'][0]['title'] not in first_form.recipe_list:
            first_form.recipe_list.append(overall_ingredients['results'][0]['title'])

    def logbtn_press(self):             #A log where you can see which course you have looked at
        message = first_form.recipe_list           #Create a String from which we can print
        npyscreen.notify_confirm(message, title="History", wrap=True, wide=True, editw=1)       #Print the string
        log.warning (f'Log is saved! History:{message}')

    def on_ok(self):
        self.parentApp.setNextForm(None)

app = App()
app.run()
