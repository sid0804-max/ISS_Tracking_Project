import streamlit as st
import pandas as pd
import pydeck as pdk
from skyfield.api import load, EarthSatellite

st.set_page_config(layout="wide")
st.title("Real-Time ISS Tracker Dashboard")

@st.cache_resource(ttl=3600)
def load_iss():
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    satellites = load.tle_file(url)
    return {sat.name: sat for sat in satellites}

satellites = load_iss()
iss = satellites["ISS (ZARYA)"]
ts = load.timescale()

def get_iss_position():
    t = ts.now()
    subpoint = iss.at(t).subpoint()
    return subpoint.latitude.degrees, subpoint.longitude.degrees, t.utc_strftime("%Y-%m-%d %H:%M:%S UTC")

lat, lon, utc_time = get_iss_position()

st.markdown(f"**Last updated:** `{utc_time}`")
st.markdown(f"**Latitude:** `{lat:.4f}°`, **Longitude:** `{lon:.4f}°`")

df = pd.DataFrame({'lat': [lat], 'lon': [lon]})

# Use open map style (no token needed)
deck = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=2, pitch=0),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[lon, lat]',
            get_color='[255, 0, 0]',
            get_radius=400000,
        )
    ]
)

st.pydeck_chart(deck)
