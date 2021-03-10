import npyscreen
from npyscreen.wgtitlefield import TitleText
import json 
import requests
<<<<<<< HEAD
import pyttsx3
=======

#Simon did it
#kl 15:55
>>>>>>> a799f3faacf4cb8b29879c9c19a424a5c4b48caf

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        #add forms to the application
        self.addForm('MAIN', FirstForm, name="main")
        
class FirstForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.add(npyscreen.TitleText, w_id="ingredientstextfield", name="Enter your ingredients:", rely= 1)
        self.add(npyscreen.ButtonPress, name="See course", when_pressed_function=self.ingredientsbtn_press, rely= 3) 
        self.add(npyscreen.TitleText, w_id="coursetextfield", name="Enter your course:", rely= 5)
        self.add(npyscreen.ButtonPress, name="See ingredients", when_pressed_function=self.coursebtn_press, rely= 7)
        self.add(npyscreen.TitleFixedText, w_id="speechtextfield", editable= False, name="Text to speech:", rely= 11)
        #self.add(npyscreen.Button, name="OFF", when_pressed_function=self.textToSpeechbtn_press, relx= 17, rely=11)
        self.add(npyscreen.CheckBox, name="ON/OFF", when_toggled=self.textToSpeechbtn_press, relx= 18, rely=11)

    def textToSpeechbtn_press(self):
        message = "You can make these different courses: "


    def ingredientsbtn_press(self):
        get_recipe = self.get_widget("ingredientstextfield").value
        URL = "http://www.recipepuppy.com/api/?i=" + get_recipe
        getInformation = requests.get(url = URL)
        recipeInformation = getInformation.json()
        recipeStr = ""

        for recipe in recipeInformation['results']:
            recipeStr += "\n" + recipe['title']
            
            if textToSpeechbtn_press == True:
                engine = pyttsx3.init()
                engine.say(recipeStr)
                engine.say(recipeStr)
                engine.runAndWait()
                
        message = "You can make these different courses: " + recipeStr
        npyscreen.notify_confirm(message, title="Ingredients", wrap=True, wide=True, editw=1)


    def coursebtn_press(self):
        get_ingredients = self.get_widget("coursetextfield").value
        URL = "http://www.recipepuppy.com/api/?q=" + get_ingredients
        getInformation = requests.get(url = URL)
        ingredientInformation = getInformation.json()
        
        ingredientStr = ""
        ingredientStr = "\n" + ingredientInformation['results'][0]['ingredients'] #tager altid det første element. Kan implementeres anderledes så den er bedere

        message = "You need these ingredients for the course '" + ingredientInformation['results'][0]['title'] + "':" + ingredientStr
        npyscreen.notify_confirm(message, title="Courses", wrap=True, wide=True, editw=1)
        


    def on_ok(self):
        self.parentApp.switchForm(None)
      
app = App()
app.run()