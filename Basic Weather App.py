import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

API_KEY = 'your_api_key' 
BASE_URL = 'https://www.accuweather.com/en/pk/national/satellite'

def get_weather(city):
    """Fetch weather data for the specified city."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_weather():
    """Update the weather information on the GUI."""
    city = city_entry.get()
    weather_data = get_weather(city)
    
    if weather_data:
        main = weather_data['main']
        weather = weather_data['weather'][0]
        
        temperature = main['temp']
        humidity = main['humidity']
        description = weather['description'].capitalize()
        icon_id = weather['icon']
        
        temperature_label.config(text=f"Temperature: {temperature}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        description_label.config(text=f"Condition: {description}")
        
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
        icon_image = Image.open(requests.get(icon_url, stream=True).raw)
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
    else:
        messagebox.showerror("Error", "City not found or network error.")

app = tk.Tk()
app.title("Weather App")

city_label = tk.Label(app, text="Enter city name:")
city_label.grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(app)
city_entry.grid(row=0, column=1, padx=10, pady=10)

temperature_label = tk.Label(app, text="Temperature: N/A")
temperature_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

humidity_label = tk.Label(app, text="Humidity: N/A")
humidity_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

description_label = tk.Label(app, text="Condition: N/A")
description_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

icon_label = tk.Label(app)
icon_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

update_button = tk.Button(app, text="Get Weather", command=update_weather)
update_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

app.mainloop()
