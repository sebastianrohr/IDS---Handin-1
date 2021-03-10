import npyscreen
from npyscreen.wgtitlefield import TitleText
import json 
import requests

#Simon did it
#kl 15:55

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


    def ingredientsbtn_press(self):
        get_recipe = self.get_widget("ingredientstextfield").value
        URL = "http://www.recipepuppy.com/api/?i=" + get_recipe
        getInformation = requests.get(url = URL)
        recipeInformation = getInformation.json()
        recipeStr = ""

        for recipe in recipeInformation['results']:
            recipeStr += "\n" + recipe['title']

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