import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim

# OpenWeatherMap API key
API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

# Function to fetch weather data
def get_weather(city, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] == 200:
            city_name = data['name']
            temp = data['main']['temp']
            weather_desc = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            icon = data['weather'][0]['icon']

            return {
                "city": city_name,
                "temp": temp,
                "description": weather_desc,
                "wind_speed": wind_speed,
                "icon": icon
            }
        else:
            messagebox.showerror("Error", "City not found!")
            return None
    except Exception as e:
        messagebox.showerror("Error", "Unable to retrieve data.")
        return None

# Function to display weather data on GUI
def display_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    units = "metric" if temp_var.get() == 1 else "imperial"
    weather_data = get_weather(city, units)

    if weather_data:
        city_label.config(text=f"City: {weather_data['city']}")
        temp_label.config(text=f"Temperature: {weather_data['temp']}°")
        desc_label.config(text=f"Weather: {weather_data['description']}")
        wind_label.config(text=f"Wind Speed: {weather_data['wind_speed']} km/h")

        # Load weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
        icon_img = Image.open(requests.get(icon_url, stream=True).raw)
        icon_img = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_img)
        icon_label.image = icon_img  # keep reference

# Initialize Tkinter Window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

# City Input
city_label_entry = tk.Label(root, text="Enter City:")
city_label_entry.pack(pady=10)

city_entry = tk.Entry(root)
city_entry.pack()

# Temperature Unit Selection
temp_var = tk.IntVar(value=1)  # Default to Celsius
celsius_rbtn = tk.Radiobutton(root, text="Celsius", variable=temp_var, value=1)
fahrenheit_rbtn = tk.Radiobutton(root, text="Fahrenheit", variable=temp_var, value=2)
celsius_rbtn.pack()
fahrenheit_rbtn.pack()

# Search Button
search_button = tk.Button(root, text="Search", command=display_weather)
search_button.pack(pady=20)

# Display Weather Information
city_label = tk.Label(root, text="City: ", font=("bold", 14))
city_label.pack()

temp_label = tk.Label(root, text="Temperature: ", font=("bold", 14))
temp_label.pack()

desc_label = tk.Label(root, text="Weather: ", font=("bold", 14))
desc_label.pack()

wind_label = tk.Label(root, text="Wind Speed: ", font=("bold", 14))
wind_label.pack()

# Weather Icon
icon_label = tk.Label(root)
icon_label.pack()

# Run the Tkinter main loop
root.mainloop()