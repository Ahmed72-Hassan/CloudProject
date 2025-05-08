from flet import * 
from __Cities__ import cities
import re 
import requests


class Signup(Column):
    def __init__(self,page:Page,on_login,on_success):
        super().__init__()
        self.page = page
        self.on_login = on_login
        self.on_success =on_success
        self.page.window.full_screen = False
        self.page.padding = 0
        self.page.title = "Login"
        self.page.window.resizable = True
        self.page.fonts={"pac":r"font/Pacifico-Regular.ttf"}
        self.null = Text("")
        self.city = cities()
       
        
        #! ===================================================================== Signup =================================================
        self.Login_text =Text(value="Signup",font_family="pac",size=30,selectable=False)

        #! ===================================================================== Textfeilds =================================================
        self.Email_textfeild = TextField(label="",border=InputBorder.UNDERLINE,hint_text="Type Your E-mail",hint_style=TextStyle(color=Colors.BLACK38),on_change=lambda e:self.on_change_email())
        self.Email = ListTile(title=Text("Email",weight=FontWeight.W_700),subtitle=self.Email_textfeild)

        self.Password_textfeild = TextField(label="",border=InputBorder.UNDERLINE,hint_text="Crete Your Password",hint_style=TextStyle(color=Colors.BLACK38),can_reveal_password=True,password=True,on_change=lambda e:self.on_change_password())
        self.password = ListTile(title=Text("Password",weight=FontWeight.W_700),subtitle=self.Password_textfeild)

        #! ===================================================================== City and Country Choosing =================================================
        self.option = [DropdownOption(text=country,leading_icon=Icon(Icons.LOCATION_ON,color=Colors.BLUE_400)) for country in sorted(self.city.get_Countries())]
        self.country_Dropdown = Dropdown(hint_text="Country",options=self.option,width=150)
        self.country = ListTile(title=Text("Your Country",weight=FontWeight.W_700),subtitle=self.country_Dropdown,width=200)

        self.city_Dropdown = Dropdown(hint_text="City",width=150)
        self.cities = ListTile(title=Text("Your City",weight=FontWeight.W_700),subtitle=self.city_Dropdown,width=200)

        self.choosing_country_city = Row(controls=[self.country,self.cities],spacing=0)
        #! ===================================================================== Login Part =================================================

        self.sign_up = Text(value="or Login Using")
        self.sign_up_button = TextButton(text="   Login   ",on_click=self.on_login)
        sign_up_login = Column(controls=[self.sign_up,self.sign_up_button],alignment=MainAxisAlignment.CENTER)
        gradient = LinearGradient(colors=["#274981", "#16203e"],begin=alignment.top_right,end=alignment.bottom_left)
        self.login_button = Container(content=Row([Text("Signup",weight=FontWeight.BOLD,color=Colors.WHITE,text_align=TextAlign.CENTER)],alignment=MainAxisAlignment.CENTER),gradient=gradient,width=300,height=40,border_radius=45,on_click=lambda e:self.signup(self.on_success),ink=True)
        
        
        self.login_succedded = Text("Success! Your signup is complete.",color=Colors.GREEN,font_family="Alex",weight=FontWeight.W_500)
        self.login_succedded_row = Row([self.login_succedded],alignment=MainAxisAlignment.CENTER,visible=False)
        Controls_Column = Column(controls=[self.null,self.Login_text,self.null,self.Email,self.password,self.choosing_country_city,self.null,self.login_button,self.login_succedded_row,sign_up_login],alignment=MainAxisAlignment.START,horizontal_alignment=CrossAxisAlignment.CENTER)
        self.login_container = Container(content=Controls_Column,width=400,height=600,border_radius=30,bgcolor="White")
        self.main_container = Container(content=Row(controls=[self.login_container],alignment=MainAxisAlignment.CENTER),gradient=gradient,width=self.page.width,height=self.page.height,expand=True)
        
        #! ===================================================================== Functions ====================================================
        self.page.on_resized = lambda e:self.on_resize()
        self.country_Dropdown.on_change = lambda e: self.city.get_cities(self.page,self.country_Dropdown,self.city_Dropdown)
        self.city_Dropdown.on_change = lambda e: self.city.choosed_city(e,self.page,self.login_button)

        self.controls = [self.main_container]

        
    def on_resize(self):
        self.main_container.width = self.page.width
        self.main_container.height = self.page.height
        self.main_container.update()
    

    def on_change_email(self):
        text = self.Email_textfeild.value
        match = bool(re.search(pattern=r"[A-Za-z0-9]+@[A-Za-z]+.com",string=text))
        if match == False:
            self.Email_textfeild.error_text = "Check your email address and try again."
            self.Email_textfeild.error_style = TextStyle(font_family="Alex")
        else:
            self.Email_textfeild.error_text = ""
        self.page.update()


    def on_change_password(self):
        text = self.Password_textfeild.value
        if len(text) < 8:
            self.Password_textfeild.error_text = "Please enter a password with 8 or more characters."
            self.Password_textfeild.error_style = TextStyle(font_family="Alex")
        else:
            self.Password_textfeild.error_text = ""
        self.page.update()
    


    def signup(self,on_success):
        data_country = self.city_Dropdown.data
        try:
            self.page.client_storage.set("lat",data_country[0])
            self.page.client_storage.set("lng",data_country[1])
            self.page.client_storage.set("email",self.Email_textfeild.value)
            data = {"e_mail": self.Email_textfeild.value,"password": self.Password_textfeild.value,
            "country": self.country_Dropdown.value, "city": data_country[2],
            "lat":float( data_country[0]),"lng": float(data_country[1]),"is_active":True}
                       
            requests.post(url="http://backend:8000//New_user",json=data)
            self.login_succedded_row.visible = True
            self.page.go("/first")

        except requests.exceptions.ConnectionError:
            self.login_succedded.value = "Oops! It looks like you're offline. Connect to the internet to continue."
            self.login_succedded.color = Colors.RED_600
            self.login_succedded_row.visible = True  
        self.page.update()
        
        
      


        
# def main(page:Page):
#     interface = Signup(page,print,print)
#     page.add(interface)
#     page.update()
    
# app(target=main,assets_dir=r"D:\My Download\DULMS\Codes\Cloud\Assignment",view=AppView.FLET_APP)  # Here You Must Change path to Your actual Path