import streamlit as st
import asyncio
import json
import pandas as pd
import joblib
from aiocoap import Context, Message, GET
model = joblib.load("air_quality_rf_model.pkl")
async def get_air_quality():
    protocol = await Context.create_client_context()
    request = Message(
        code=GET,
        uri="coap://127.0.0.1:5683/airquality"
    )
    response = await protocol.request(request).response
    return json.loads(
        response.payload.decode()
    )
def get_data():
    return asyncio.run(
        get_air_quality()
    )
def sub_index(value, bp):
    for low, high, ilow, ihigh in bp:
        if low <= value <= high:
            return round(
                ((ihigh - ilow) / (high - low))
                * (value - low)
                + ilow
            )
def calculate_aqi(pm25, pm10, no2, so2, o3):
    pm25_bp = [(0,30,0,50),(31,60,51,100),(61,90,101,200),
               (91,120,201,300),(121,250,301,400),(251,500,401,500)]
    pm10_bp = [(0,50,0,50),(51,100,51,100),(101,250,101,200),
               (251,350,201,300),(351,430,301,400),(431,500,401,500)]
    no2_bp = [(0,40,0,50),(41,80,51,100),(81,180,101,200),
              (181,280,201,300),(281,400,301,400),(401,800,401,500)]
    so2_bp = [(0,40,0,50),(41,80,51,100),(81,380,101,200),
              (381,800,201,300),(801,1600,301,400),(1601,2620,401,500)]
    o3_bp = [(0,50,0,50),(51,100,51,100),(101,168,101,200),
             (169,208,201,300),(209,748,301,400),(749,1000,401,500)]
    values = [
        sub_index(pm25, pm25_bp),
        sub_index(pm10, pm10_bp),
        sub_index(no2, no2_bp),
        sub_index(so2, so2_bp),
        sub_index(o3, o3_bp)
    ]
    return max(values)
def get_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    return "Severe"
st.title("IoT Air Quality Monitoring")
st.write(
    "Live air-quality data from CoAP server "
    "using Random Forest Classification"
)
if st.button("Get Live Air Quality"):

    data = get_data()
    if "error" in data:
        st.error(data["error"])
    else:
        st.subheader("Live Data")
        st.write("Location:", data["location"])
        st.write("Time:", data["time"])
        pollutants = ["PM2.5", "PM10", "NO2", "SO2", "O3"]
        for p in pollutants:
            st.write(f"{p}: {data[p]}")
        live_data = pd.DataFrame(
            [[
                data["PM2.5"],
                data["PM10"],
                data["NO2"],
                data["SO2"],
                data["O3"]
            ]],
            columns=pollutants
        )
        prediction = model.predict(
            live_data
        )[0]
        aqi = calculate_aqi(
            data["PM2.5"],
            data["PM10"],
            data["NO2"],
            data["SO2"],
            data["O3"]
        )
        category = get_category(aqi)
        st.subheader("AQI")
        st.write("Calculated AQI:", aqi)
        st.write("AQI Category:", category)
        st.subheader("Machine Learning Result")
        st.success(
            f"Random Forest Prediction: {prediction}"
        )
        comparison = pd.DataFrame({
            "Method": [
                "AQI Calculation",
                "Random Forest"
            ],
            "Result": [
                category,
                prediction
            ]
        })
        st.subheader("AQI vs ML")
        st.table(comparison)
        st.subheader("Model Input")
        st.dataframe(live_data)
