from flask import Flask, render_template
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px

load_dotenv()

app = Flask(__name__)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


@app.route("/")
def home():

    response = supabase.table("weather_readings").select("*").order("recorded_at").execute()

    df = pd.DataFrame(response.data)

    if len(df) == 0:
        return "No Data"

    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    current = df.iloc[-1]["temperature"]

    fig = px.line(
        df,
        x="recorded_at",
        y="temperature",
        title="Temperature Trend"
    )

    graph = fig.to_html(full_html=False)

    return render_template(
        "index.html",
        current=current,
        graph=graph,
        table=df.tail(20).to_html(classes="table")
    )


if __name__ == "__main__":
    app.run(debug=True)