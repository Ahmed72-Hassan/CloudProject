from flet import * 
from Database import Database
import requests


class Login(Column):
    def __init__(self,page:Page,on_signup,on_success):
        super().__init__()
        self.page = page
        self.on_signup = on_signup
        self.on_success = on_success
        self.page.window.full_screen = False
        self.page.padding = 0
        self.page.title = "Login"
        self.page.window.resizable = True
        self.page.fonts={"pac":r"font/Pacifico-Regular.ttf","Alex":r"font/3.ttf"}
        self.null = Text("")
       


        self.Login_text =Text(value="Login",font_family="pac",size=30,selectable=False)

        self.Email_textfeild = TextField(label="",border=InputBorder.UNDERLINE,hint_text="Type Your E-mail",hint_style=TextStyle(color=Colors.BLACK38))
        self.Email = ListTile(title=Text("Email",weight=FontWeight.W_700),subtitle=self.Email_textfeild)

        self.Remeber_me = Row([Checkbox(label="Remeber Me!",value=False,label_position=LabelPosition.RIGHT,label_style=TextStyle(weight=FontWeight.W_700,color=Colors.BLUE_700))],alignment=MainAxisAlignment.CENTER)
        self.Password_textfeild = TextField(label="",border=InputBorder.UNDERLINE,hint_text="Type Your Password",hint_style=TextStyle(color=Colors.BLACK38),can_reveal_password=True,password=True,counter=self.Remeber_me,on_change=lambda e:self.on_change_password())
        self.password = ListTile(title=Text("Password",weight=FontWeight.W_700),subtitle=self.Password_textfeild)

        self.sign_up = Text(value="or Signup Using")
        self.sign_up_button = TextButton(text="   Signup   ",on_click=self.on_signup)
        sign_up_login = Column(controls=[self.sign_up,self.sign_up_button],alignment=MainAxisAlignment.CENTER)
        gradient = LinearGradient(colors=["#274981", "#16203e"],begin=alignment.top_right,end=alignment.bottom_left)

        self.login_succedded = Text("Success! Your Login is complete.",color=Colors.GREEN,font_family="Alex",weight=FontWeight.W_500)
        self.login_succedded_row = Row([self.login_succedded],alignment=MainAxisAlignment.CENTER,visible=False)

        self.login_button = Container(content=Row([Text("LOGIN",weight=FontWeight.BOLD,color=Colors.WHITE,text_align=TextAlign.CENTER)],alignment=MainAxisAlignment.CENTER),gradient=gradient,width=300,height=40,border_radius=45,on_click=lambda e:self.login(),ink=True)
        Controls_Column = Column(controls=[self.null,self.Login_text,self.null,self.Email,self.password,self.null,self.login_button,self.null,self.login_succedded_row,sign_up_login,],alignment=MainAxisAlignment.START,horizontal_alignment=CrossAxisAlignment.CENTER)
        self.login_container = Container(content=Controls_Column,width=400,height=600,border_radius=30,bgcolor="White")
        self.main_container = Container(content=Row(controls=[self.login_container],alignment=MainAxisAlignment.CENTER),gradient=gradient,width=self.page.width,height=self.page.height,expand=True)
        self.controls = [self.main_container]
        self.page.on_resized = lambda e:self.on_resize()
        
        
    def on_resize(self):
        self.main_container.width = self.page.width
        self.main_container.height = self.page.height
        self.main_container.update()

    def login(self):
        try:
            response = requests.get(f"http://backend:8000/items/{self.Email_textfeild.value}")
            if response.status_code == 200:
                data = response.json()  

            if data["password"] == self.Password_textfeild.value:
                self.login_succedded_row.visible = True
                self.page.client_storage.set("lat",data["lat"])
                self.page.client_storage.set("lng",data["lng"])
                self.page.client_storage.set("email",self.Email_textfeild.value)
                # print(self.Remeber_me.controls[0].value)
                requests.put(f"http://backend:8000/is_active/{self.Email_textfeild.value}",
                             params={"is_active": self.Remeber_me.controls[0].value})

                self.on_success(None)
                
        except UnboundLocalError:
            self.Password_textfeild.error_text = "Password is incorrect.Please Try Again"
            self.Password_textfeild.error_style = TextStyle(font_family="Alex")
        except requests.exceptions.ConnectionError:
            self.login_succedded.value = "Oops! It looks like you're offline. Connect to the internet to continue."
            self.login_succedded.color = Colors.RED_600
            self.login_succedded_row.visible = True  
        self.page.update()
    

    def on_change_password(self):
        self.Password_textfeild.error_text = ""
        self.page.update()

            

# def main(page:Page):
#     interface = Login(page,print,print)
#     page.add(interface)
#     page.update()
    
# app(target=main,assets_dir=r"D:\My Download\DULMS\Codes\Cloud\Assignment",view=AppView.FLET_APP) 
        