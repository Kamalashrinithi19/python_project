import streamlit as st
from geopy.geocoders import Nominatim
import requests
from datetime import datetime

# Streamlit setup
st.set_page_config(page_title="🌍 Weather Forecast", layout="wide")
st.title("🌦️ City-Based 7-Day Weather Forecast")
st.write("Enter your city, district, and country to get the upcoming week's weather!")

# User input
location_input = st.text_input("📍 Enter location (City, District, Country):", "Bangalore, Karnataka, India")

# Forecast on button press
if st.button("🔍 Get Forecast"):
    geolocator = Nominatim(user_agent="weather-forecast-app")
    location = geolocator.geocode(location_input)

    if location:
        lat = location.latitude
        lon = location.longitude
        st.success(f"📌 Location found: {location.address} (Lat: {lat:.4f}, Lon: {lon:.4f})")

        # Call Open-Meteo API
        api_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
            f"&timezone=auto"
        )
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            days = data["daily"]["time"]
            max_temps = data["daily"]["temperature_2m_max"]
            min_temps = data["daily"]["temperature_2m_min"]
            codes = data["daily"]["weathercode"]

            st.markdown("## 🔮 7-Day Weather Forecast")

            # Styling with flex layout for cards and bigger icons/text
            st.markdown("""
            <style>
            .weather-container {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 1.5rem;
                max-width: 1200px;
                margin: 2rem auto;
            }
            .weather-card {
                background-color: #f9f9f9;
                padding: 1.5rem 2rem;
                border-radius: 1.5rem;
                box-shadow: 0 4px 16px rgba(0,0,0,0.05);
                text-align: center;
                width: 150px;
                flex-shrink: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .weather-card h3 {
                font-size: 2.4rem;
                margin-bottom: 0.5rem;
            }
            .weather-card .desc {
                font-size: 1.6rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            .weather-card .temp {
                font-size: 1.4rem;
                color: #555;
            }
            </style>
            """, unsafe_allow_html=True)

            # Wrap cards inside a container div
            st.markdown('<div class="weather-container">', unsafe_allow_html=True)

            # Loop through each day
            for i in range(7):
                date = datetime.strptime(days[i], "%Y-%m-%d").strftime("%A, %b %d")
                max_temp = max_temps[i]
                min_temp = min_temps[i]
                code = codes[i]

                # Emoji & description
                if code in [61, 63, 65, 80, 81, 82]:
                    icon = "🌧️"
                    desc = "Rainy"
                elif code in [71, 73, 75, 85, 86]:
                    icon = "❄️"
                    desc = "Snow"
                elif code in [95, 96, 99]:
                    icon = "⛈️"
                    desc = "Thunderstorm"
                elif max_temp > 35:
                    icon = "🥵"
                    desc = "Very Hot"
                elif max_temp < 10:
                    icon = "🧊"
                    desc = "Cold"
                else:
                    icon = "🌤️"
                    desc = "Mild"

                # Display forecast card
                st.markdown(f"""
                <div class="weather-card">
                    <h3>{date} <br> <span style="font-size:3.5rem;">{icon}</span></h3>
                    <div class="desc">{desc}</div>
                    <div class="temp">🌡️ Max: {max_temp:.1f}°C<br>Min: {min_temp:.1f}°C</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error("❌ Failed to fetch weather data. Please try again later.")
    else:
        st.error("⚠️ Could not find that location. Please enter a valid city, district, or country.")
