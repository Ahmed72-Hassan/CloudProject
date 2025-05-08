import pandas as pd 
from flet import *

class cities():
    def __init__(self):
        self.data = pd.read_csv("assets/Datasets/Cities.csv")


    def get_cities(self,page:Page,countries:Dropdown,cities:Dropdown):
        """cities appear based on country choose """
        Country = countries.value.capitalize()
        city = [DropdownOption(text=city,key=[float(lat),float(lng),city],leading_icon=Icon(Icons.LOCATION_CITY,color=Colors.BLUE_400),data={"lat":float(lat),"lng":float(lng),"city":city}) 
                for country,city ,lng,lat in zip(self.data["country"].values,self.data["city"].values,self.data["lng"].values,self.data["lat"].values) if country == Country]
        cities.options = city
        page.update()


    def choosed_city(self,e:ControlEvent,page:Page,sign_up:Container):
        """action that happen when user choose city"""
        e.control.data = [e.control.value.replace("'","").removeprefix('[').removesuffix(']').split(",")[x].strip() for x in range(3)]
        page.update()
        

    def get_Countries(self):
        return set(list(self.data["country"]))        