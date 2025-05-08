import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Database import *
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

db = Database("weather")
app = FastAPI()

@app.get("/some-api-endpoint")
def some_endpoint():
    return {"message": "Hello from backend!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    e_mail: str
    password: str
    country:str
    city:str
    lat:float
    lng:float
    is_active:bool

class ML(BaseModel):
    month:str
    precipitation:float  
    temp_max:float       
    temp_min:float       
    wind:float  
               
def init_db():
    with sqlite3.connect("weather.db") as conn:
        conn.execute('''
    CREATE TABLE Weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    e_mail VARCHAR(255),
    password VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255),
    lat INT,
    lng INT,
    is_active BOOLEAN DEFAULT TRUE
                    );''')
try:
    init_db()
except:
    pass
model = joblib.load("assets/Models/model.joblib")



@app.get("/")
def read_root():
    return {"message": f"The Server is open now"}


@app.post("/New_user")
def create_item(item: Item):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Weather (e_mail,password,city,country,lat,lng,is_active) VALUES (?,?,?,?,?,?,?)", 
                           (item.e_mail,item.password,item.city,item.country,item.lat,item.lng,item.is_active))
        conn.commit()
        db.insert(email=item.e_mail,password=item.password,city=item.city,country=item.country,lat=item.lat,lng=item.lng)

        item_id = cursor.lastrowid
    return {"id": item_id, "e_mail": item.e_mail, "password": item.password,"city":item.city,"country":item.country,"lat":item.lat,"lng":item.lng}

@app.get("/items")
def read_items():
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Weather")
        rows = cursor.fetchall()
    return [{"id":row[0], "e_mail": row[1], "password": row[2],"city":row[3],"country":row[4],"lat":row[5],"lng":row[6]} for row in rows]

@app.get("/items/{e_mail}")
def read_item(e_mail: str):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Weather WHERE e_mail = ?", (e_mail,))

        data = cursor.fetchall()
    if data:
        return [{"id":row[0], "e_mail": row[1], "password": row[2],"city":row[3],"country":row[4],"lat":row[5],"lng":row[6]} for row in data][0]
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{e_mail}")
def update_item(item: Item):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Weather SET country = ?, city = ? WHERE e_mail = ?", (item.country, item.city, item.e_mail))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    return {"Status":True}


@app.delete("/items/{e_mail}")
def delete_item(e_mail:str):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Weather WHERE e_mail = ?", (e_mail,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}


@app.put("/is_active/{e_mail}")
def update_IsActive(e_mail:str,is_active:bool):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Weather SET is_active = ? WHERE e_mail = ?", (is_active, e_mail))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    return {"Status":True}



@app.get("/is_active/{e_mail}")
def get_IsActive(e_mail:str):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_active FROM Weather WHERE e_mail = ?",(e_mail,))
        conn.commit()
        data = cursor.fetchone()
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="Item not found")

@app.get("/country/{e_mail}")
def get_country(e_mail:str):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT country FROM Weather WHERE e_mail = ?",(e_mail,))
        conn.commit()
        data = cursor.fetchone()
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="Item not found")
        


@app.post("/predict")
def ML_predict_Wether(data:ML):
    input_data = np.array([[data.month, data.precipitation, data.temp_max, data.temp_min,data.wind]])
    prediction = model.predict(input_data)
    return prediction[0]