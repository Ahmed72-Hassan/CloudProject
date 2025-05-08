from flet import *
import requests
import pandas as pd
import random as rn
from datetime import datetime, timedelta
import google.generativeai as genai
import re
import time


class frontend():
      
    def gimini(condition:str,temperture:float):
        genai.configure(api_key="AIzaSyCiy1rNn24Vwx85ij2HseLOOHqR2tKDmpY",)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = f"write Caption as the develop to the user that Weather Condition is {condition} and temperature is {temperture}"
        generated_text = model.generate_content(prompt,generation_config=genai.types.GenerationConfig(
                max_output_tokens=100 ))
        
        generated_text= re.findall(pattern=r">\s[a-zA-Z0-9.°\s!]+",string = generated_text.text)

        return generated_text[0].removeprefix(">")
    
    def Get_cloud_data():
        try:
            data = requests.get(url="https://api.open-meteo.com/v1/forecast?latitude=30&longitude=31.22&hourly=cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high&forecast_days=1")
            return data.json()
        except:
            pass


    @staticmethod
    def day_information(Type:str,value:str):
        return Column(controls=[Text(Type,size=15,color="#dbd9e1"),Text(value,size=17,color="#dbd9e1")],spacing=0)
    
    def week_info(day:str,morning:str,night:str,morning_image:str,night_image:str):
        fourth_part_1 = Container(bgcolor="#253251",height=180,width=150,border_radius=10,
        content=Column(controls=[
            Row([Text(day, size=12, color="white")],alignment=MainAxisAlignment.CENTER),
            Row(controls=[Image(src=morning_image, width=50, height=50),Text(f"{morning}", size=18, color="white")],spacing=5,alignment=MainAxisAlignment.START),
            Row(controls=[Image(src=night_image, width=50, height=50),Text(f"{night}", size=18, color="white")],spacing=5,alignment=MainAxisAlignment.START),
        ],alignment=MainAxisAlignment.CENTER,spacing=15))

        return fourth_part_1
    

    def week_info(day:str,morning:str,night:str,morning_image:str,night_image:str):
        fourth_part_1 = Container(bgcolor="#253251",height=180,width=150,border_radius=10,
        content=Column(controls=[
            Row([Text(day, size=12, color="white")],alignment=MainAxisAlignment.CENTER),
            Row(controls=[Image(src=morning_image, width=50, height=50),Text(f"{morning}", size=18, color="white")],spacing=5,alignment=MainAxisAlignment.START),
            Row(controls=[Image(src=night_image, width=50, height=50),Text(f"{night}", size=18, color="white")],spacing=5,alignment=MainAxisAlignment.START),
        ],alignment=MainAxisAlignment.CENTER,spacing=15))

        return fourth_part_1
    

    class every_hour(Container):
        def __init__(self, page:Page,time:str,image_hour:str,temp:str,Rain:str,Wind:str,Humidity:str,Pressure:str,Dew_point:str,Visibility:str):
            super().__init__()
            self.page = page
            self.time = time
            self.image_hour = image_hour
            self.temp = temp
            self.Rain =Rain
            self.Wind =Wind
            self.Humidity =Humidity
            self.Pressure =Pressure
            self.Dew_point =Dew_point
            self.Visibility =Visibility
            self.bgcolor = "#253251"
            self.height = 550 
            self.width = 200 
            self.padding = 20 
            self.border_radius = 10
            self.margin = Margin(top=10, left=0, right=10, bottom=10)
            
            self.time_text = Row(controls=[Icon(Icons.ACCESS_TIME_FILLED,color=Colors.WHITE60),Text(time, size=20, color="white")],alignment=MainAxisAlignment.CENTER)

            self.temperature = Row(controls=[Image(src=self.image_hour, width=50, height=50),Text(f"{self.temp}°C", size=18, color="white")],spacing=5,alignment=MainAxisAlignment.START)
            
            self.rain_row = Column(controls=[Row([Icon(Icons.CLOUD,color=Colors.WHITE60),Text("Rain",size=15,color="#dbd9e1")]),Text(f"{self.Rain}mm",size=17,color="#dbd9e1")],spacing=0)
            self.wind_row = Column(controls=[Row([Icon(Icons.AIR,color=Colors.WHITE60),Text("Wind",size=15,color="#dbd9e1")]),Text(f"{self.Wind} km/h",size=17,color="#dbd9e1")],spacing=0)
            self.humidity_row = Column(controls=[Row([Icon(Icons.WATER_DROP ,color=Colors.WHITE60),Text("Humidity",size=15,color="#dbd9e1")]),Text(f"{self.Humidity}%",size=17,color="#dbd9e1")],spacing=0)
            self.pressure_row = Column(controls=[Row([Icon(Icons.SHOW_CHART,color=Colors.WHITE60),Text("Pressure",size=15,color="#dbd9e1")]),Text(f"{self.Pressure} mb",size=17,color="#dbd9e1")],spacing=0)
            self.Dew_point_row = Column(controls=[Row([Icon(Icons.FOGGY,color=Colors.WHITE60),Text("Dew point",size=15,color="#dbd9e1")]),Text(f"{self.Dew_point}°",size=17,color="#dbd9e1")],spacing=0)
            self.Visibility_row = Column(controls=[Row([Icon(Icons.TRAVEL_EXPLORE,color=Colors.WHITE60),Text("Visibility",size=15,color="#dbd9e1")]),Text(f"{self.Visibility} M",size=17,color="#dbd9e1")],spacing=0)
            self.second_column = Column(controls=[self.rain_row,self.wind_row,self.humidity_row,self.pressure_row,self.Dew_point_row,self.Visibility_row],alignment=MainAxisAlignment.CENTER,spacing=20)
            self.content=Column(controls=[self.time_text,self.temperature,self.second_column],alignment=MainAxisAlignment.CENTER,spacing=20)
        



    class Searchbar11(SearchBar):

        def __init__(self,page:Page,on_Choose, controls = None, value = None, bar_leading = None, bar_trailing = None, bar_hint_text = None, bar_bgcolor = None, bar_overlay_color = None, bar_shadow_color = None, bar_surface_tint_color = None, bar_elevation = None, bar_border_side = None, bar_shape = None, bar_text_style = None, bar_hint_text_style = None, bar_padding = None, bar_scroll_padding = None, view_leading = None, view_trailing = None, view_elevation = None, view_bgcolor = None, view_hint_text = None, view_side = None, view_shape = None, view_header_text_style = None, view_hint_text_style = None, view_size_constraints = None, view_header_height = None, divider_color = None, capitalization = None, full_screen = None, keyboard_type = None, view_surface_tint_color = None, autofocus = None, on_tap = None, on_tap_outside_bar = None, on_submit = None, on_change = None, on_focus = None, on_blur = None, ref = None, key = None, width = None, height = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None):
            super().__init__(controls, value, bar_leading, bar_trailing, bar_hint_text, bar_bgcolor, bar_overlay_color, bar_shadow_color, bar_surface_tint_color, bar_elevation, bar_border_side, bar_shape, bar_text_style, bar_hint_text_style, bar_padding, bar_scroll_padding, view_leading, view_trailing, view_elevation, view_bgcolor, view_hint_text, view_side, view_shape, view_header_text_style, view_hint_text_style, view_size_constraints, view_header_height, divider_color, capitalization, full_screen, keyboard_type, view_surface_tint_color, autofocus, on_tap, on_tap_outside_bar, on_submit, on_change, on_focus, on_blur, ref, key, width, height, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data)
            self.page = page
            self.on_choose = on_Choose
            self.data = pd.read_csv("assets/Datasets/Cities.csv")
            self.on_change = lambda e: self.__on_change()
            self.on_tap = lambda e: self.__on_tap_searchbae()
            self.bar_trailing = [Icon(Icons.SEARCH)]
            self.bar_leading = Icon(Icons.LOCATION_ON)
            self.bar_hint_text = "Search City ...."


        def __on_tap_searchbae(self):
            for city , country , lat,lng in rn.sample(list(zip(self.data["city"],self.data["country"],self.data["lat"],self.data["lng"])), k =10):
                v =Tooltip(message=f" latitude: {lat} \n Longitude: {lng}")
                listtile = ListTile(leading=Icon(Icons.SEARCH),title=Text(value=city,weight=FontWeight.W_700),subtitle=Text(value=country),trailing=IconButton(Icons.LOCATION_ON,tooltip=v,icon_color=Colors.BLUE),data={"lat":lat,"lng":lng},on_click=self.on_choose)
                self.controls.append(listtile)
            self.open_view()
            self.page.update()



        def __on_change(self):
            Value = self.value
            cities = [(city,country,lat,lng) for city , country , lat,lng in list(zip(self.data["city"],self.data["country"],self.data["lat"],self.data["lng"])) if Value.capitalize() in city ]
            self.open_view()
            for  count ,info in zip(list(range(10)),cities[:10]):
                v =Tooltip(message=f" latitude: {info[2]} \n Longitude: {info[3]}")
                listtile:ListTile = self.controls[count]
                listtile.leading =Icon(Icons.SEARCH)
                listtile.title = Text(value=info[0],weight=FontWeight.W_700)
                listtile.subtitle = Text(value=info[1])
                listtile.trailing = IconButton(Icons.LOCATION_ON,tooltip=v,icon_color=Colors.BLUE)
                listtile.data= {"lat":info[2],"lng":info[3]}
                count +=1
            self.page.update()
        


        def Choose_city(self,e:ControlEvent):
            print(e.control.data)
            self.page.update()
    



class Backend():
    backend_url = "http://backend:8000"
    
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{backend_url}/some-api-endpoint")
            print(response.json())
            break
        except requests.exceptions.ConnectionError:
            print(f"Backend not ready, retrying... ({i+1}/{max_retries})")
            time.sleep(2)# إجراء طلب GET على الـ backend
            
    class data():
        def __init__(self,lat:str,lng:str):
            self.lat = lat
            self.lng = lng
            self.url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lng}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum&current=rain,wind_speed_10m,relative_humidity_2m,surface_pressure,precipitation,temperature_2m&past_days=1"
            response = requests.get(self.url)
            self.data = response.json()

        def get_currnt_day_weather(self):
            return self.data["current"]
        
        def get_week_Weather(self):
            return self.data["daily"]
        


        def get_6_days(self):
            today = datetime.today()
            next_days = [today + timedelta(days=i) for i in range(-1, 5)]
            return [day.strftime("%A") for i, day in enumerate(next_days, 1) ]
        

        def Get_temperature_data_hourly(self):
            """this function return Hourly_Time , Hourly_Temperature """
            try:
                data = requests.get(url=f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lng}&hourly=temperature_2m,visibility,dew_point_2m,relative_humidity_2m,rain,wind_speed_10m,surface_pressure&forecast_days=1")

                data = data.json()
                list1 = [] 
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                list6 = []
                list7 = []
                list8 = []
                hourly_time = [x[-5:] for x in data["hourly"]["time"]]
                hourly_temp = [x for x in data["hourly"]["temperature_2m"]]
                hourly_temp = [x for x in data["hourly"]["temperature_2m"]]
                hourly_wind = [x for x in data["hourly"]["wind_speed_10m"]]

                hourly_rain = [x for x in data["hourly"]["rain"]]
                hourly_humidity = [x for x in data["hourly"]["relative_humidity_2m"]]
                hourly_dew_point = [x for x in data["hourly"]["dew_point_2m"]]
                hourly_surface_pressure = [x for x in data["hourly"]["surface_pressure"]]
                hourly_visibility = [x for x in data["hourly"]["visibility"]]

                for x in range(3,len(hourly_time),4):
                    list1.append(hourly_time[x])
                    list2.append(hourly_temp[x])
                    list3.append(hourly_rain[x])
                    list4.append(hourly_humidity[x])
                    list5.append(hourly_dew_point[x])
                    list6.append(hourly_surface_pressure[x])
                    list7.append(hourly_visibility[x])
                    list8.append(hourly_wind[x])


                return list1 , list2 , list3,list4 , list5 ,list6 ,list7 ,list8
            except:
                pass



# weather = Backend.data(lat='44',lng='44')
# time,temperature,rain,huimuidity,dew_point,pressure,visabality = weather.get_hourly_data()
       



   