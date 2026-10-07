import asyncio
import json
import requests
import joblib
from aiocoap import resource, Context, Message
LATITUDE = 9.93
LONGITUDE = 76.27
API_URL = (
    f"https://air-quality-api.open-meteo.com/v1/air-quality"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current=pm10,pm2_5,nitrogen_dioxide,sulphur_dioxide,ozone"
)
model = joblib.load("air_quality_rf_model.pkl")
class AirQualityResource(resource.Resource):
    async def render_get(self, request):
        try:
            current = requests.get(
                API_URL,
                timeout=10
            ).json()["current"]
            pm25 = current["pm2_5"]
            pm10 = current["pm10"]
            no2 = current["nitrogen_dioxide"]
            so2 = current["sulphur_dioxide"]
            o3 = current["ozone"]
            prediction = model.predict(
                [[pm25, pm10, no2, so2, o3]]
            )[0]
            result = {
                "location": "Kochi",
                "time": current["time"],
                "PM2.5": pm25,
                "PM10": pm10,
                "NO2": no2,
                "SO2": so2,
                "O3": o3,
                "air_quality_status": prediction
            }
            print(json.dumps(result, indent=4))
            return Message(
                payload=json.dumps(result).encode(),
                content_format=50
            )
        except Exception as e:
            return Message(
                payload=json.dumps(
                    {"error": str(e)}
                ).encode(),
                content_format=50
            )
async def main():
    root = resource.Site()
    root.add_resource(
        ["airquality"],
        AirQualityResource()
    )
    await Context.create_server_context(
        root,
        bind=("127.0.0.1", 5683)
    )
    print("CoAP Server Running")
    print("coap://127.0.0.1:5683/airquality")
    await asyncio.get_running_loop().create_future()
if __name__ == "__main__":
    asyncio.run(main())