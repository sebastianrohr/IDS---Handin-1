import npyscreen
from npyscreen.wgtitlefield import TitleText
import json 
import requests
import random
import pyttsx3

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', FirstForm) 
        
class FirstForm(npyscreen.ActionForm):
    opskriftListe = []
    def create(self):
        self.add(npyscreen.TitleText, w_id="ingredientstextfield", name="Enter your ingredients:", rely= 1)
        self.add(npyscreen.ButtonPress, name="See course", when_pressed_function=self.ingredientsbtn_press, rely= 3) 
        self.add(npyscreen.TitleText, w_id="coursetextfield", name="Enter your course:", rely= 5)
        self.add(npyscreen.ButtonPress, name="See ingredients", when_pressed_function=self.coursebtn_press, rely= 7)
        self.add(npyscreen.ButtonPress, name="Hear ingredients", when_pressed_function=self.readbtn_press, rely = 7, relx = 20)
        self.add(npyscreen.ButtonPress, name="Read log", when_pressed_function=self.logbtn_press, rely = 7, relx=39)

    def ingredientsbtn_press(self): #Displays recipes based on given ingredients
        get_recipe = self.get_widget("ingredientstextfield").value
        URL = "http://www.recipepuppy.com/api/?i=" + get_recipe
        getInformation = requests.get(url = URL)
        recipeInformation = getInformation.json()
        recipeStr = ""
        for recipe in recipeInformation['results']:
           recipeStr += "\n" + recipe['title']
        npyscreen.notify_confirm(recipeStr, title="You can make these different courses", wrap=True, wide=True, editw=1)

    def coursebtn_press(self): #Searches for recipes and displays ingredients
        get_ingredients = self.get_widget("coursetextfield").value
        URL = "http://www.recipepuppy.com/api/?q=" + get_ingredients
        getInformation = requests.get(url = URL)
        ingredientInformation = getInformation.json()
        ingredientStr = "\n" + ingredientInformation['results'][0]['ingredients']
        npyscreen.notify_confirm(ingredientStr, title="You need these ingredients for the course '" + ingredientInformation['results'][0]['title'] + "':", wrap=True, wide=True, editw=1)
        if ingredientInformation['results'][0]['title'] not in FirstForm.opskriftListe: #Avoids duplications og already saved recipes
            FirstForm.opskriftListe.append(ingredientInformation['results'][0]['title'])
            
    def readbtn_press(self): #Reads ingredients out loud
        get_ingredients = self.get_widget("coursetextfield").value
        URL = "http://www.recipepuppy.com/api/?q=" + get_ingredients
        getInformation = requests.get(url = URL)
        ingredientInformation = getInformation.json()
        ingredientStr = "\n" + ingredientInformation['results'][0]['ingredients']
        message = "You need these ingredients for the course '" + ingredientInformation['results'][0]['title'] + "':" + ingredientStr
        engine = pyttsx3.init()         #Initiation of speaker
        engine.say(message)             #Speaker message
        engine.runAndWait()            
        if ingredientInformation['results'][0]['title'] not in FirstForm.opskriftListe:
            FirstForm.opskriftListe.append(ingredientInformation['results'][0]['title'])

    def logbtn_press(self):             #A log where you can see which course you have looked at
        message = FirstForm.opskriftListe           #Create a String from which we can print
        npyscreen.notify_confirm(message, title="History", wrap=True, wide=True, editw=1)       #Print the string

    def on_ok(self):
        self.parentApp.setNextForm(None)

app = App()
app.run()