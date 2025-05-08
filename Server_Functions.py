import requests 
from flet import *

class Server:

    @staticmethod
    def get_user_activiate_state(page:Page):
            try:
                url = f"http://backend:8000/is_active/{page.client_storage.get('email')}"
                params = {"e_mail": f"{page.client_storage.get('email')}"}
                response = requests.get(url, params=params)
                return response.json()[0]
            except:
                return 0
            
    @staticmethod
    def Delete_account(page:Page):
        try:
           
            requests.delete(f"http://backend:8000/items/{page.client_storage.get('email')}",params={"e_mail":f"{page.client_storage.get('email')}"})
            return True
        except:
            return False
        
    @staticmethod
    def get_user_data(email:str):
        response = requests.get(f"http://backend:8000/items/{email}")
        if response.status_code == 200:
            data = response.json()  
            return data
        else:
            print("Error:", response.status_code, response.text)


    @staticmethod 
    def get_user_country(page:Page):
        try:
            res = requests.get(f"http://backend:8000/country/{page.client_storage.get('email')}",params={"e_mail":f"{page.client_storage.get('email')}"})
            return res.json()[0]
        except:
            return " Hello"
        

