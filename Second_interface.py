from flet import *
from __design_pattern__ import frontend, Backend
from first_interface import first

class Second(ResponsiveRow):  
    def __init__(self,page:Page,first_interface:first):
        super().__init__()
        self.page = page
        self.first_interface = first_interface
        self.page.fonts = {"logo": r"font/AGENCYB.TTF", "home_title": r"font/BRLNSB.TTF"}
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = "transparent"
        self.page.window.maximized = True
        self.spacing = 10  
        self.page.scroll = ScrollMode.AUTO
        lat = self.page.client_storage.get("lat")
        lng = self.page.client_storage.get("lng")
        self.weather = Backend.data(lat=lat, lng=lng)
        self.time, self.temperature, self.rain, self.huimuidity, self.dew_point, self.pressure, self.visabality, self.wind = self.weather.Get_temperature_data_hourly()

        #!===================================================================== Account Feilf =====================================================================
        Account_button = IconButton(icon=Icons.ACCOUNT_CIRCLE,icon_color=Colors.WHITE,on_click=lambda e: self.page.open(first_interface.drawer))
        self.acount = ResponsiveRow(controls=[Column(col={"xs": 12}, controls=[Row(controls=[Account_button,Text(f"{self.page.client_storage.get('email')}", font_family="logo",color=Colors.WHITE)], alignment=MainAxisAlignment.START)])])

        #!===================================================================== Title =====================================================================
        top_bar = Container(bgcolor="#242424",height=150,
            content=Column(controls=[self.acount,
                ResponsiveRow(controls=[
                    Column(col={"xs": 12}, controls=[
                        Row(controls=[
                            Image("photos/logo.png", width=130, height=110),
                            Text("WeathAI", color="white", font_family="logo", size=40)
                        ], alignment=MainAxisAlignment.CENTER)
                    ])
                ])
            ], alignment=MainAxisAlignment.CENTER)
        )

        #!===================================================================== Location info #!=====================================================================
        self.city = Text(f"{first.country}, {first.city}", color="white", size=18)
        body_content = Container(
            content=ResponsiveRow(controls=[
                Column(col={"xs": 12}, controls=[
                    Row(controls=[
                        Icon(name=Icons.LOCATION_ON, color="white", size=20),
                        self.city
                    ], alignment=MainAxisAlignment.CENTER)
                ])
            ])
        )
        #!===================================================================== photos and Weather Cards =====================================================================
        photos = ["photos/cloudy.png", "photos/Rainy.png", "photos/Rainy.png", "photos/Windy night.png", "photos/Night11.png", "photos/Night11.png"]
        weather_cards = [frontend.every_hour(self.page, self.time[x], photos[x], self.temperature[x],self.rain[x], self.wind[x], self.huimuidity[x],self.pressure[x], self.dew_point[x], self.visabality[x]) for x in range(6)]

        #!===================================================================== Weather Controls =====================================================================
        self.weather_row = ResponsiveRow(controls=[Column(col={"xs": 12, "sm": 6, "md": 4, "lg": 2}, controls=[card]) for card in weather_cards],
        spacing=10,alignment=MainAxisAlignment.CENTER,vertical_alignment=CrossAxisAlignment.CENTER,run_spacing=10)
        
        #!===================================================================== Controls =====================================================================
        main_content = Container(content=Column(controls=[top_bar,body_content,Container(height=20),self.weather_row,Container(height=20)],spacing=0,horizontal_alignment=CrossAxisAlignment.CENTER),gradient=LinearGradient(begin=alignment.top_center,end=alignment.bottom_center,colors=["#274981", "#16203e"]),expand=True)
        self.controls = [main_content]



# def main(page:Page):
#     first_interface = Second(page,print)
#     page.add(first_interface)
# app(target=main,assets_dir=r"D:\My Download\DULMS\Codes\Cloud\Project\assets")