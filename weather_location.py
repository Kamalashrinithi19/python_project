import streamlit as st
from geopy.geocoders import Nominatim
import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="🌍 Weather Forecast", layout="wide")
st.title("🌦 Weather Forecast App")

# Initialize geocoder
geolocator = Nominatim(user_agent="weather-app-2024")

# Location input
st.markdown("### Enter your location:")
location_input = st.text_input(
    "Enter location:",
    placeholder="e.g., Coimbatore, Tamil Nadu, India",
    key="location_search"
)

lat, lon, location_name = None, None, None

if st.button("🔍 Find Location", key="search_btn"):
    if location_input.strip():
        with st.spinner("Searching for location..."):
            try:
                # Try to geocode the location
                location = geolocator.geocode(location_input.strip())
                
                if location:
                    lat = location.latitude
                    lon = location.longitude
                    location_name = location.address
                    
                    st.success(f"✅ Found: {location_name}")
                    st.info(f"📍 Coordinates: {lat:.4f}, {lon:.4f}")
                    
                    # Store in session state
                    st.session_state['current_lat'] = lat
                    st.session_state['current_lon'] = lon
                    st.session_state['current_location'] = location_name
                    
                else:
                    st.error("❌ Location not found. Try a different format like 'City, State, Country'")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter a location first!")

# Check if we have location data (from session state or current detection)
if 'current_lat' in st.session_state and 'current_lon' in st.session_state:
    lat = st.session_state['current_lat']
    lon = st.session_state['current_lon']
    location_name = st.session_state['current_location']

# Weather forecast section
if lat is not None and lon is not None:
    st.markdown("---")
    st.markdown(f"### 📍 Current Location: {location_name}")
    
    # Clear location button
    if st.button("🗑 Clear Location", key="clear_btn"):
        if 'current_lat' in st.session_state:
            del st.session_state['current_lat']
        if 'current_lon' in st.session_state:
            del st.session_state['current_lon']
        if 'current_location' in st.session_state:
            del st.session_state['current_location']
        st.rerun()
    
    # Get weather forecast
    if st.button("🌤 Get Weather Forecast", type="primary", key="weather_btn"):
        with st.spinner("Getting weather forecast..."):
            try:
                # Calculate date range (past 3 days + next 7 days)
                start_date = datetime.now().date() - timedelta(days=3)
                end_date = datetime.now().date() + timedelta(days=7)
                
                # Weather API URL
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode&start_date={start_date}&end_date={end_date}&timezone=auto"
                
                # Get weather data
                weather_response = requests.get(weather_url, timeout=10)
                
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    
                    # Extract data
                    dates = weather_data['daily']['time']
                    max_temps = weather_data['daily']['temperature_2m_max']
                    min_temps = weather_data['daily']['temperature_2m_min']
                    weather_codes = weather_data['daily']['weathercode']
                    rain_probs = weather_data['daily']['precipitation_probability_max']
                    
                    # Display 7-day forecast (skip past days, show from today)
                    st.markdown("## 🔮 7-Day Weather Forecast")
                    
                    # Find today's index
                    today = datetime.now().date()
                    today_idx = None
                    for i, date_str in enumerate(dates):
                        if datetime.strptime(date_str, '%Y-%m-%d').date() == today:
                            today_idx = i
                            break
                    
                    if today_idx is not None:
                        # Show 7 days starting from today
                        cols = st.columns(7)
                        
                        for i in range(7):
                            if today_idx + i < len(dates):
                                idx = today_idx + i
                                date_obj = datetime.strptime(dates[idx], '%Y-%m-%d')
                                
                                day_name = "Today" if i == 0 else date_obj.strftime('%a')
                                date_str = date_obj.strftime('%b %d')
                                max_temp = max_temps[idx]
                                min_temp = min_temps[idx]
                                weather_code = weather_codes[idx]
                                rain_prob = rain_probs[idx] if rain_probs[idx] else 0
                                
                                # Weather icon and description
                                if weather_code == 0:
                                    icon, desc, bg_color = "☀", "Clear", "#F39C12"
                                elif weather_code in [1, 2, 3]:
                                    icon, desc, bg_color = "⛅", "Cloudy", "#95A5A6"
                                elif weather_code in [61, 63, 65, 80, 81, 82]:
                                    icon, desc, bg_color = "🌧", f"Rain {rain_prob}%", "#3498DB"
                                elif weather_code in [71, 73, 75]:
                                    icon, desc, bg_color = "❄", "Snow", "#85C1E9"
                                elif weather_code in [95, 96, 99]:
                                    icon, desc, bg_color = "⛈", "Storm", "#8E44AD"
                                else:
                                    icon, desc, bg_color = "🌤", "Partly Cloudy", "#F1C40F"
                                
                                with cols[i]:
                                    st.markdown(f"""
                                    <div style="background-color: {bg_color}; color: white; padding: 10px; border-radius: 10px; text-align: center; margin: 5px 0;">
                                        <strong>{day_name}</strong><br>
                                        <small>{date_str}</small><br>
                                        <div style="font-size: 30px; margin: 5px 0;">{icon}</div>
                                        <small>{desc}</small><br>
                                        <strong>↑ {max_temp:.1f}°C</strong><br>
                                        <strong>↓ {min_temp:.1f}°C</strong>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Temperature chart
                        st.markdown("## 📊 Temperature Chart")
                        
                        # Create DataFrame for chart
                        chart_data = pd.DataFrame({
                            'Date': [datetime.strptime(d, '%Y-%m-%d') for d in dates],
                            'Max Temp': max_temps,
                            'Min Temp': min_temps
                        })
                        
                        # Create matplotlib chart
                        fig, ax = plt.subplots(figsize=(12, 6))
                        
                        ax.plot(chart_data['Date'], chart_data['Max Temp'], 
                               label='Max Temperature', color='red', marker='o', linewidth=2)
                        ax.plot(chart_data['Date'], chart_data['Min Temp'], 
                               label='Min Temperature', color='blue', marker='o', linewidth=2)
                        
                        ax.fill_between(chart_data['Date'], chart_data['Min Temp'], chart_data['Max Temp'], 
                                       alpha=0.3, color='lightblue')
                        
                        # Add today line
                        ax.axvline(x=today, color='green', linestyle='--', alpha=0.7, label='Today')
                        
                        ax.set_title('Temperature Forecast', fontsize=16)
                        ax.set_xlabel('Date')
                        ax.set_ylabel('Temperature (°C)')
                        ax.legend()
                        ax.grid(True, alpha=0.3)
                        
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        
                        st.pyplot(fig)
                        
                    else:
                        st.error("❌ Could not find today's date in weather data")
                        
                else:
                    st.error(f"❌ Weather API Error: {weather_response.status_code}")
                    
            except Exception as e:
                st.error(f"❌ Weather Error: {str(e)}")

else:
    st.info("👆 Please enter a location above to get started!")

# Footer
st.markdown("---")
st.markdown("Weather data from Open-Meteo API | Location services by Nominatim")
