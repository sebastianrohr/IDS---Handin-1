import npyscreen
from npyscreen.wgtitlefield import TitleText
import json 
import requests

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
        ##get_recipe("potato", "olive")
        get_recipe = self.get_widget("ingredientstextfield").value
        URL = "http://www.recipepuppy.com/api/?i=" + get_recipe
        ## url = url + get_widget.replace(' ', ',')
        getInformation = requests.get(url = URL)
        recipeInformation = getInformation.json()
        recipeStr = " "

        for recipe in recipeInformation['results']:
            recipeStr += "\n" + recipe['title']

        message = "You can make these different courses: " + recipeStr
        npyscreen.notify_confirm(message, title="Ingredients", wrap=True, wide=True, editw=1)

    def coursebtn_press(self):
        message = f'Course results: {self.get_widget("coursetextfield").value}' 
        npyscreen.notify_confirm(message, title="Courses", wrap=True, wide=True, editw=1)
        
    def on_ok(self):
        self.parentApp.switchForm(None)
      
app = App()
app.run()