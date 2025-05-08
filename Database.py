import requests



class Database:
    SUPABASE_URL = "https://yfdzqfrjwzvrvyypvlmx.supabase.co"

    SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlmZHpxZnJqd3p2cnZ5eXB2bG14Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM5MzU2NDUsImV4cCI6MjA0OTUxMTY0NX0.kqUgfYpDl_RgOxs0UHsDKvw0c3G-3trgQMriwnEJaPo"
    headers = {"Authorization": f"{SUPABASE_API_KEY}","apikey": f"{SUPABASE_API_KEY}"}

    @staticmethod
    def get_user_data(email:str):
        response = requests.get(f"http://127.0.0.1:8000/items/{email}")
        if response.status_code == 200:
            data = response.json()  
            return data
        else:
            print("Error:", response.status_code, response.text)

    def __init__(self,Table_name:str):
        self.Table_name = Table_name

        
    def insert(self,email:str,password:str,city:str,country:str,lat:str,lng:str):
        url = f"{Database.SUPABASE_URL}/rest/v1/{self.Table_name}"
        data = {"e_mail": email,"password": password,"city": city,"country": country,"lat": float(lat),"lng": float(lng)}
        response = requests.post(url, json=data, headers=Database.headers)
        if response.status_code == 201 or response.status_code == 200:
            print("تمت إضافة البيانات بنجاح.")
        else:
            print("فشل في إدخال البيانات:", response.status_code, response.text)

    
    def Select_all(self,email:str):

        url = f"{Database.SUPABASE_URL}/rest/v1/{self.Table_name}?e_mail=eq.{email}"
        response = requests.get(url,  headers=Database.headers)
        if response.status_code == 201 or response.status_code == 200:
            return response.json()
        else:
            print("فشل في إدخال البيانات:", response.status_code, response.text)
    

    





# db = Database("weather")

# # db.insert("awadallayossef@gmail.com",password="123456",city="Cairo",country="Egypt",lat="30",lng="31")

# db.Select_all("awadallayossef@gmail.com")
