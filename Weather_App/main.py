import requests
import tkinter as tk
from tkinter import messagebox, ttk
from urllib.parse import quote
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x550")
        self.root.iconbitmap('C:\\Users\\futbo\\Downloads\\overcastday_weather_sun_cloudy_4493.ico')
        
        # Set up style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # City selection
        self.city_label = ttk.Label(self.main_frame, text="City:")
        self.city_label.grid(row=0, column=0, sticky=tk.W)
        self.city_entry = ttk.Entry(self.main_frame)
        self.city_entry.grid(row=0, column=1, sticky=tk.EW)
        self.main_frame.columnconfigure(1, weight=1)

        # Date selection
        self.date_label = ttk.Label(self.main_frame, text="Select Date:")
        self.date_label.grid(row=1, column=0, sticky=tk.W)
        self.selected_date = tk.StringVar()
        self.date_entry = ttk.Entry(self.main_frame, textvariable=self.selected_date)
        self.date_entry.grid(row=1, column=1, sticky=tk.EW)
        self.date_entry.insert(tk.END, datetime.now().strftime("%Y-%m-%d"))

        # Fetch weather button
        self.fetch_button = ttk.Button(self.main_frame, text="Fetch Weather", command=self.fetch_weather)
        self.fetch_button.grid(row=2, columnspan=2, pady=10)

        # Weather information display
        self.weather_label = ttk.Label(self.main_frame, text="", wraplength=350)
        self.weather_label.grid(row=3, columnspan=2, pady=10)

        # Weather icon display
        self.icon_label = ttk.Label(self.main_frame)
        self.icon_label.grid(row=4, columnspan=2)

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        selected_date = self.selected_date.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        api_key = "16ef362a3d744663486d4fd899f19462"  # Replace with your actual API key
        city_encoded = quote(city)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&units=metric&APPID={api_key}"
        
        self.weather_label.config(text="Fetching weather data...")
        self.root.update_idletasks()

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("cod") != 200:
                messagebox.showerror("Error", data.get("message", "Unable to fetch weather data"))
                return

            temperature = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            sunrise = data["sys"]["sunrise"]
            sunset = data["sys"]["sunset"]
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

            weather_info = (f"Temperature: {temperature}°C\n"
                            f"Weather: {weather}\n"
                            f"Humidity: {humidity}%\n"
                            f"Wind Speed: {wind_speed} m/s\n"
                            f"Pressure: {pressure} hPa\n"
                            f"Sunrise: {sunrise}\n"
                            f"Sunset: {sunset}")

            # Fetch the weather icon
            icon_response = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_response.content))
            icon_photo = ImageTk.PhotoImage(icon_image)

            self.weather_label.config(text=weather_info)
            self.icon_label.config(image=icon_photo)
            self.icon_label.image = icon_photo
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                messagebox.showerror("Unauthorized", "Invalid API key or unauthorized access.")
            else:
                messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
