import npyscreen

# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

class MyTestApp(npyscreen.NPSAppManaged):
    #Gloval variables
    allowedThrough, allowedOn, allowedOut = None, None, None
    def onStart(self):
        self.registerForm("MAIN", MainForm())
        self.registerForm("AllowedOn", AllowedOnForm())
        self.registerForm("AllowedOut", AllowedOutForm())
        self.registerForm("OtherOptions", OtherOptionsForm())


class MainForm(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("AllowedOn")

    def create(self):
        self.allowedThrough = self.add(npyscreen.TitleMultiSelect,max_height=4, name='Select which services are allowed to be accessed through the firewall (forwarded packets):', values=['HTTPS', 'SSH', 'RDP'],scroll_exit=True)

    def on_ok(self):
        self.parentApp.allowedThrough = self.allowedThrough.value
        self.parentApp.switchForm("AllowedOn")


class AllowedOnForm(npyscreen.Form):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("AllowedOut")
        
    def create(self):
        self.allowedOn = self.add(npyscreen.TitleMultiSelect,max_height=4, name='Select which services are allowed to be accessed on the firewall (incoming packets):', values=['HTTPS', 'SSH', 'RDP'],scroll_exit=True)

    def on_ok(self):
        self.parentApp.allowedOn = self.allowedOn.value
        self.parentApp.switchForm("AllowedOut")


class AllowedOutForm(npyscreen.Form):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("OtherOptions")
        
    def create(self):
        self.allowedOut = self.add(npyscreen.TitleMultiSelect,max_height=4, name='Select which services are allowed to be accessed from the firewall (outgoing packets):', values=['HTTPS', 'SSH', 'RDP'],scroll_exit=True)

    def on_ok(self):
        self.parentApp.allowedOut = self.allowedOut.value
        self.parentApp.switchForm("OtherOptions")


class OtherOptionsForm(npyscreen.Form):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm(None)
        
    def create(self):
        self.customSSHPort = self.add(npyscreen.TitleText, name='Testing!')

    def on_ok(self):
        config_data = [
            "Services allowed through:"]
        config_data.append(' '.join(map(str,self.allowedThrough.value)))
        config_data.append("Services allowed on:")
        config_data.append(' '.join(map(str,self.allowedOn.value)))
        config_data.append("Services allowed from:")
        config_data.append(' '.join(map(str,self.allowedFrom.value)))
        with open("TestConfig.txt", 'w') as file:
            for line in config_data:
                file.write(line + '\n')
        self.parentApp.switchForm(None)
    

if __name__ == '__main__':
    npyscreen.wrapper(MyTestApp().run())