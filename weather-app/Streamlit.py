import streamlit as st
import requests
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Weather App", page_icon="🌦️")

st.title("Weather App")

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌦️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "❄️"
    elif 701 <= weather_id <= 741:
        return "🌫️"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪️"
    elif weather_id == 800:
        return "☀️"
    elif 801 <= weather_id <= 804:
        return "☁️"
    else:
        return "❓"

def display_error(message):
    st.error(message)
    st.warning("Please try again or check your input.")

city = st.text_input("Enter city name", placeholder="Enter a city like New York or Tokyo...")

load_dotenv()
api_key = os.getenv("API_KEY")

if st.button("Get Weather"):
    if city:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                temperature_k = data["main"]["temp"]
                temperature_f = (temperature_k * 9/5) - 459.67
                weather_id = data["weather"][0]["id"]
                weather_description = data["weather"][0]["description"]
                
                # Display weather data with current weather emoji
                st.success(f'**{city.title()}**: {temperature_f:.0f}°F')
                st.markdown(f'### {get_weather_emoji(weather_id)} {weather_description.title()}')
            
            else:
                display_error(f"City '{city}' not found. Please check your spelling.")

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    display_error("Bad request: Please check your input.")
                case 401:
                    display_error("Unauthorized: Invalid API key.")
                case 403:
                    display_error("Forbidden: Access is denied.")
                case 404:
                    display_error("Not found: City not found.")
                case 500:
                    display_error("Internal Server Error: Please try again later.")
                case 502:
                    display_error("Bad Gateway: Invalid response from the server.")
                case 503:
                    display_error("Service Unavailable: Server is down.")
                case 504:
                    display_error("Gateway Timeout: No response from the server.")
                case _:
                    display_error(f"HTTP error occurred: {http_error}")

        except requests.exceptions.ConnectionError:
            display_error("Connection Error: Check your internet connection.")

        except requests.exceptions.Timeout:
            display_error("Timeout Error: The request timed out.")

        except requests.exceptions.TooManyRedirects:
            display_error("Too many redirects: Check the URL.")

        except requests.exceptions.RequestException as req_error:
            display_error(f"Request Error: {req_error}")

        except Exception as e:
            display_error(f"An unexpected error occurred: {e}")