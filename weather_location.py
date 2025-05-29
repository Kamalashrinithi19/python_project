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

            # Enhanced CSS with better alignment and responsiveness
            st.markdown("""
            <style>
            .weather-container {
                display: flex;
                justify-content: center;
                align-items: stretch;
                flex-wrap: wrap;
                gap: 1rem;
                padding: 1rem;
                margin: 1rem 0;
            }
            
            .weather-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 1rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                text-align: center;
                min-width: 140px;
                max-width: 180px;
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                transition: transform 0.3s ease;
            }
            
            .weather-card:hover {
                transform: translateY(-5px);
            }
            
            .weather-card .date {
                font-size: 0.9rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                opacity: 0.9;
            }
            
            .weather-card .icon {
                font-size: 3rem;
                margin: 0.5rem 0;
            }
            
            .weather-card .desc {
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            
            .weather-card .temp {
                font-size: 0.9rem;
                opacity: 0.9;
                line-height: 1.4;
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .weather-container {
                    justify-content: space-around;
                }
                .weather-card {
                    min-width: 120px;
                    max-width: 140px;
                }
            }
            </style>
            """, unsafe_allow_html=True)

            # Create weather cards HTML
            cards_html = '<div class="weather-container">'
            
            # Loop through each day
            for i in range(7):
                date = datetime.strptime(days[i], "%Y-%m-%d").strftime("%a, %b %d")
                max_temp = max_temps[i]
                min_temp = min_temps[i]
                code = codes[i]

                # Emoji & description mapping
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

                # Add each card to the HTML string
                cards_html += f"""
                <div class="weather-card">
                    <div class="date">{date}</div>
                    <div class="icon">{icon}</div>
                    <div class="desc">{desc}</div>
                    <div class="temp">Max: {max_temp:.1f}°C<br>Min: {min_temp:.1f}°C</div>
                </div>
                """
            
            cards_html += '</div>'
            
            # Display all cards at once
            st.markdown(cards_html, unsafe_allow_html=True)

        else:
            st.error("❌ Failed to fetch weather data. Please try again later.")
    else:
        st.error("⚠️ Could not find that location. Please enter a valid city, district, or country.")

# Alternative approach using Streamlit columns (more reliable)
st.markdown("---")
st.markdown("### Alternative Layout Using Streamlit Columns")

if st.button("🔍 Get Forecast (Column Layout)"):
    geolocator = Nominatim(user_agent="weather-forecast-app-v2")
    location = geolocator.geocode(location_input)

    if location:
        lat = location.latitude
        lon = location.longitude
        
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

            # Using Streamlit columns for better alignment
            cols = st.columns(7)
            
            for i in range(7):
                date = datetime.strptime(days[i], "%Y-%m-%d").strftime("%a\n%b %d")
                max_temp = max_temps[i]
                min_temp = min_temps[i]
                code = codes[i]

                # Weather mapping
                if code in [61, 63, 65, 80, 81, 82]:
                    icon = "🌧️"
                    desc = "Rainy"
                elif code in [71, 73, 75, 85, 86]:
                    icon = "❄️"
                    desc = "Snow"
                elif code in [95, 96, 99]:
                    icon = "⛈️"
                    desc = "Storm"
                elif max_temp > 35:
                    icon = "🥵"
                    desc = "Hot"
                elif max_temp < 10:
                    icon = "🧊"
                    desc = "Cold"
                else:
                    icon = "🌤️"
                    desc = "Mild"

                with cols[i]:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #74b9ff, #0984e3);
                        color: white;
                        padding: 1rem;
                        border-radius: 10px;
                        text-align: center;
                        margin-bottom: 1rem;
                        min-height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    ">
                        <div style="font-size: 0.8rem; font-weight: bold;">{date}</div>
                        <div style="font-size: 2.5rem; margin: 0.5rem 0;">{icon}</div>
                        <div style="font-size: 0.9rem; font-weight: 600;">{desc}</div>
                        <div style="font-size: 0.8rem;">
                            Max: {max_temp:.1f}°C<br>
                            Min: {min_temp:.1f}°C
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
