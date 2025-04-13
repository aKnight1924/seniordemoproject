import npyscreen

# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())
        self.registerForm("TestDisplay", TestDisplayForm())

# This form class defines the display that will be presented to the user.

class MainForm(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("TestDisplay")

    def create(self):
        self.allowedThrough = self.add(npyscreen.TitleMultiSelect,max_height=4, name='Services Allowed to Be Access Through The Firewall:', values=['HTTPS', 'SSH', 'RDP'],scroll_exit=True)

    def on_ok(self):
        toTest = self.parentApp.getForm("TestDisplay")
        toTest.selected.value = []
        for x in self.allowedThrough.value:
            toTest.selected.value.append(self.allowedThrough.values[x])
        self.parentApp.switchForm("TestDisplay")

class TestDisplayForm(npyscreen.Form):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm(None)
        
    def create(self):
        self.selected = self.add(npyscreen.TitleFixedText,max_height=4,name="Service Selected: ")

if __name__ == '__main__':
    npyscreen.wrapper(MyTestApp().run())