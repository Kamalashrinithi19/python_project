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
    with st.spinner("Getting weather data..."):
        geolocator = Nominatim(user_agent="weather-forecast-app")
        location = geolocator.geocode(location_input)

        if location:
            lat = location.latitude
            lon = location.longitude
            st.success(f"📌 Location found: {location.address}")

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
                
                # Create 7 columns with equal spacing
                cols = st.columns(7)
                
                # Loop through each day
                for i in range(7):
                    date_obj = datetime.strptime(days[i], "%Y-%m-%d")
                    day_name = date_obj.strftime("%a")
                    date_str = date_obj.strftime("%b %d")
                    max_temp = max_temps[i]
                    min_temp = min_temps[i]
                    code = codes[i]

                    # Determine weather emoji and description
                    if code in [61, 63, 65, 80, 81, 82]:
                        icon = "🌧️"
                        desc = "Rainy"
                        bg_color = "#4A90E2"
                    elif code in [71, 73, 75, 85, 86]:
                        icon = "❄️"
                        desc = "Snow"
                        bg_color = "#7ED4E8"
                    elif code in [95, 96, 99]:
                        icon = "⛈️"
                        desc = "Storm"
                        bg_color = "#8B5A96"
                    elif max_temp > 35:
                        icon = "🥵"
                        desc = "Very Hot"
                        bg_color = "#E74C3C"
                    elif max_temp < 10:
                        icon = "🧊"
                        desc = "Cold"
                        bg_color = "#5DADE2"
                    else:
                        icon = "🌤️"
                        desc = "Pleasant"
                        bg_color = "#F39C12"

                    # Display each day in its column
                    with cols[i]:
                        st.markdown(f"""
                        <div style="
                            background-color: {bg_color};
                            color: white;
                            padding: 15px;
                            border-radius: 10px;
                            text-align: center;
                            margin: 2px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                            height: 160px;
                            display: flex;
                            flex-direction: column;
                            justify-content: space-between;
                        ">
                            <div style="font-weight: bold; font-size: 12px;">{day_name}</div>
                            <div style="font-size: 10px;">{date_str}</div>
                            <div style="font-size: 36px; margin: 8px 0;">{icon}</div>
                            <div style="font-size: 11px; font-weight: 600;">{desc}</div>
                            <div style="font-size: 10px;">
                                <div>↑ {max_temp:.1f}°C</div>
                                <div>↓ {min_temp:.1f}°C</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Alternative simple display using native Streamlit components
                st.markdown("---")
                st.markdown("### Alternative Simple Display")
                
                # Create columns again for alternative layout
                cols2 = st.columns(7)
                
                for i in range(7):
                    date_obj = datetime.strptime(days[i], "%Y-%m-%d")
                    day_name = date_obj.strftime("%a")
                    date_str = date_obj.strftime("%m/%d")
                    max_temp = max_temps[i]
                    min_temp = min_temps[i]
                    code = codes[i]

                    # Weather mapping
                    if code in [61, 63, 65, 80, 81, 82]:
                        icon = "🌧️"
                        desc = "Rain"
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
                        desc = "Nice"

                    with cols2[i]:
                        # Using Streamlit's metric component
                        st.metric(
                            label=f"{icon} {day_name}",
                            value=f"{max_temp:.0f}°C", 
                            delta=f"{min_temp:.0f}°C"
                        )
                        st.caption(f"{date_str} • {desc}")

            else:
                st.error("❌ Failed to fetch weather data. Please try again later.")
        else:
            st.error("⚠️ Could not find that location. Please check spelling and try again.")
