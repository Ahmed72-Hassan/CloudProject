from flet import *
from datetime import datetime
from __design_pattern__ import frontend, Backend
from Server_Functions import Server
import requests

class first(Column):
    city = ""
    country = ''
    def __init__(self,page:Page):
        super().__init__()
        self.page = page
        self.page.fonts = {"logo": r"font/AGENCYB.TTF", "home_title": r"font/BRLNSB.TTF"}
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = "transparent"
        self.page.window.maximized = True
        self.scroll = ScrollMode.AUTO
        self.spacing = 5
        self.page.scroll = ScrollMode.AUTO
        self.database = Server.get_user_data(self.page.client_storage.get("email"))
        self.waether = Backend.data(lat=self.page.client_storage.get("lat"), lng=self.page.client_storage.get("lng"))
        self.current = self.waether.get_currnt_day_weather()
        self.days = self.waether.get_6_days()
        self.week = self.waether.get_week_Weather()

        #!===================================================================== Navigation Drawer =====================================================================
        self.destinitions = [
            ResponsiveRow(controls=[
                Column(col=12, controls=[
                    Row(controls=[
                        Image("photos/logo.png", width=110, height=90),
                        Text("WeathAI", color="white", font_family="logo", size=25)
                    ], alignment=MainAxisAlignment.CENTER)
                ])
            ]),
            Divider(height=30),
            NavigationDrawerDestination(label="Home", icon=Icons.HOME_OUTLINED, selected_icon=Icon(Icons.HOME)),
            NavigationDrawerDestination(label="Hourly", icon=Icons.WATCH_LATER_OUTLINED, selected_icon=Icon(Icons.WATCH_LATER)),
            Divider(height=30),
            ListTile(
                title=Text("Delete Account", color=Colors.WHITE),
                leading=Icon(Icons.DELETE, color=Colors.RED),
                trailing=Icon(Icons.ARROW_RIGHT, color=Colors.WHITE),
                on_click=lambda e: self.delete_account()
            ),
            ListTile(
                title=Text("Logout", color=Colors.WHITE),
                leading=Icon(Icons.LOGOUT, color=Colors.RED_600),
                trailing=Icon(Icons.ARROW_RIGHT, color=Colors.WHITE),
                on_click=lambda e: self.Log_out()
            )
        ]

        self.drawer = NavigationDrawer(controls=self.destinitions,bgcolor="#242424",indicator_shape=StadiumBorder(),indicator_color=Colors.WHITE,selected_index=0,on_change=lambda e: self.change_pages())

        ##!===================================================================== Top Bar #!=====================================================================
        Account_button = IconButton(icon=Icons.ACCOUNT_CIRCLE,icon_color=Colors.WHITE,on_click=lambda e: self.page.open(self.drawer))
        
        self.acount = ResponsiveRow(controls=[
                Column(col={"xs": 12}, controls=[
                    Row(controls=[Account_button,Text(f"{self.page.client_storage.get('email')}", font_family="logo", color=Colors.WHITE)], alignment=MainAxisAlignment.START)])])
        
        top_bar = Container(bgcolor="#242424",height=180,
            content=Column(controls=[self.acount,
                ResponsiveRow(controls=[Column(col=12, controls=[
                        Row(controls=[Image("photos/logo.png", width=130, height=110),Text("WeathAI", color="white", font_family="logo", size=40)], alignment=MainAxisAlignment.CENTER)])])], alignment=MainAxisAlignment.CENTER))

        #!===================================================================== Search Bar #!=====================================================================
        self.search_bar = frontend.Searchbar11(self.page, lambda e: self.on_change_city(e))
        scound_bar = Container(bgcolor="#1a3156",height=80,
            content=ResponsiveRow(controls=[Column(col={"xs": 10, "sm": 8, "md": 6}, controls=[self.search_bar])], alignment=MainAxisAlignment.CENTER))

        ##!===================================================================== Location Display #!=====================================================================
        self.city = Text(f"{self.database['country']}, {self.database['city']}", color="white", size=18)
        first.city = self.database["city"]
        first.country = self.database["country"]
        body_content = Container(content=ResponsiveRow(controls=[Column(col=12, controls=[Row(controls=[Icon(name=Icons.LOCATION_ON, color="white", size=20),self.city], alignment=MainAxisAlignment.CENTER)])]))

        ##!===================================================================== Current Weather #!=====================================================================
        self.current_weather_text = Text(f"Current Weather\n{datetime.now().strftime('%d/%m/%Y').center(16)}",size=20, color="white", font_family="logo")
        self.current_temperature = Text(f"{self.current['temperature_2m']}°C", size=45, color="white")
        self.current_condition = Text(f"{0}", size=14, color="white")
        self.caption_text = Text("The skies will be mostly cloudy. The high will be 24°.", size=16, color="white")

        weather_info = ResponsiveRow(controls=[
            Column(col={"xs": 12, "sm": 4}, controls=[
                Image(src="photos/Mostly cloudy.png", width=90, height=90)
            ]),
            Column(col={"xs": 12, "sm": 4}, controls=[
                self.current_temperature,
                self.current_condition
            ]),
            Column(col={"xs": 12, "sm": 4}, controls=[
                self.caption_text
            ])
        ], alignment=MainAxisAlignment.CENTER, spacing=20)

        #!===================================================================== Weather Metrics #!=====================================================================
        metrics = ResponsiveRow(
            controls=[
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Rain", f"{self.current['rain']}mm")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Wind", f"{self.current['wind_speed_10m']}km/h")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Humidity", f"{self.current['relative_humidity_2m']}%")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Pressure", f"{self.current['surface_pressure']} mb")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Precipitation", f"{self.current['precipitation']}°")
                ])
            ],
            spacing=10,
            alignment=MainAxisAlignment.CENTER
        )

        self.third_part = Container(bgcolor="#253251",height=350,border_radius=10,
        content=Column(controls=[ResponsiveRow(controls=[Column(col=12, controls=[self.current_weather_text])]),weather_info,metrics], spacing=30, alignment=MainAxisAlignment.CENTER))

        ##!===================================================================== Weekly Forecast #!=====================================================================
        temperature = [frontend.week_info(day, f"{day_temp} °C", f"{night_temp} °C", r"photos/day.png", r"photos/night.png")for day_temp, night_temp, day in zip(self.week["temperature_2m_max"], self.week["temperature_2m_min"], self.days)]
        windspeed = [frontend.week_info(day, f"{day_temp}Km/h", f"{night_temp} mm", r"photos/wind day.png", r"photos/Humidity day.png")for day_temp, night_temp, day in zip(self.week["wind_speed_10m_max"], self.week["precipitation_sum"], self.days)]

        #!===================================================================== Arcticture #!=====================================================================
        self.row0 = ResponsiveRow(controls=[Column(col={"xs": 12, "md": 10, "lg": 8}, controls=[self.third_part])], alignment=MainAxisAlignment.CENTER)
        self.row1 = ResponsiveRow(controls=[Column(col={"xs": 6, "sm": 4, "md": 2}, controls=[item]) for item in temperature],spacing=10,alignment=MainAxisAlignment.CENTER)
        self.row2 = ResponsiveRow(controls=[Column(col={"xs": 6, "sm": 4, "md": 2}, controls=[item]) for item in windspeed],spacing=10,alignment=MainAxisAlignment.CENTER)

        self.second_part_column = Column(controls=[self.row0, self.row1, self.row2], spacing=20)
        self.column = Column(controls=[top_bar,scound_bar,Container(height=20),body_content,Container(height=20),self.second_part_column],spacing=0)
        
        #!===================================================================== controls #!=====================================================================
        gradient_overlay = Container(content=self.column,gradient=LinearGradient(begin=alignment.top_center,end=alignment.bottom_center,colors=["#274981", "#16203e"]))
        self.controls = [gradient_overlay]
        self.Weather_prediction()
        self.from_egypt_or_not()

    def on_change_city(self, e: ControlEvent):
        data = e.control.data
        lat = data["lat"]
        lng = data["lng"]
        self.waether = Backend.data(lat=lat, lng=lng)
        self.current = self.waether.get_currnt_day_weather()
        self.days = self.waether.get_6_days()
        self.week = self.waether.get_week_Weather()
        
        city = e.control.title.value
        country = e.control.subtitle.value
       
        first.city = city
        first.country = country
        self.city.value = f"{country}, {city}"
        self.current_temperature.value = f"{self.current['temperature_2m']}°C"
        
        metrics = ResponsiveRow(
            controls=[
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Rain", f"{self.current['rain']}mm")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Wind", f"{self.current['wind_speed_10m']}km/h")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Humidity", f"{self.current['relative_humidity_2m']}%")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Pressure", f"{self.current['surface_pressure']} mb")
                ]),
                Column(col={"xs": 4, "sm": 2, "md": 2}, controls=[
                    frontend.day_information("Precipitation", f"{self.current['precipitation']}°")
                ])
            ],
            spacing=10,
            alignment=MainAxisAlignment.CENTER
        )
        
        self.third_part.content.controls[2].controls = metrics.controls
        self.row1.controls = [
            Column(col={"xs": 6, "sm": 4, "md": 2}, controls=[item]) 
            for item in [
                frontend.week_info(day, f"{day_temp} °C", f"{night_temp} °C", r"photos/day.png", r"photos/night.png")
                for day_temp, night_temp, day in zip(self.week["temperature_2m_max"], self.week["temperature_2m_min"], self.days)
            ]
        ]
        
        self.row2.controls = [
            Column(col={"xs": 6, "sm": 4, "md": 2}, controls=[item]) 
            for item in [
                frontend.week_info(day, f"{day_temp}Km/h", f"{night_temp} mm", r"photos/wind day.png", r"photos/Humidity day.png")
                for day_temp, night_temp, day in zip(self.week["wind_speed_10m_max"], self.week["precipitation_sum"], self.days)
            ]
        ]
        
        self.search_bar.close_view(f"{city}")
        self.Weather_prediction()
        self.city.update()
        self.current_temperature.update()
        self.third_part.update()
        self.row1.update()
        self.row2.update()
        self.page.update()
        

    def change_pages(self):
        if self.drawer.selected_index == 1:
            self.page.go("/second")    
        else:
            self.page.go("/first")
        self.page.update()

    def delete_account(self):
        Server.Delete_account(self.page)
        self.page.go("/signup")
        self.page.update()

    def Log_out(self):
        requests.put(f"http://backend:8000/is_active/{self.page.client_storage.get('email')}",params={"is_active": 0})
        self.page.go("/signup")
        self.page.update()

    def from_egypt_or_not(self):
        if Server.get_user_country(self.page) != "Egypt":
            del self.destinitions[-2]
            self.drawer.controls = self.destinitions
            self.page.update()

    def Weather_prediction(self):
        data = {"month": f"{datetime.now().strftime('%m')}","precipitation": float(self.current["precipitation"]),
            "temp_max": float(self.current["temperature_2m"]),"temp_min": 25,
            "wind": float(self.current["wind_speed_10m"])}
        response = requests.post("http://backend:8000/predict", json=data)
        
        if response.status_code == 200:
            prediction = response.json()
            self.current_condition.value = prediction
            self.caption_text.value = frontend.gimini(prediction, float(self.current["temperature_2m"]))
        else:
            print("Error:", response.status_code, response.text)
        self.page.update()
        


# def main(page:Page):
#     first_interface = first(page)
#     page.add(first_interface)
    
# app(target=main,assets_dir=r"D:\My Download\DULMS\Codes\Cloud\Project\assets",view=AppView.FLET_APP)