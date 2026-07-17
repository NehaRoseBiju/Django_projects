import csv
import io
from flask import Flask, render_template, jsonify, request, Response
from supabase_config import supabase

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def fetch_filtered_data(start_time=None, end_time=None):
    query = supabase.table("temp_readings").select("*")
    if start_time:
        query = query.gte("Time Stamp", start_time)
    if end_time:
        query = query.lte("Time Stamp", end_time)
    
    # Order by Time Stamp descending to get latest first.
    response = query.order("Time Stamp", desc=True).execute()
    return response.data

@app.route("/temperature")
def temperature():
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    try:
        data = fetch_filtered_data(start_time, end_time)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/export-csv")
def export_csv():
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    try:
        data = fetch_filtered_data(start_time, end_time)
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(["ID", "Temperature (°C)", "Date", "Time Stamp"])
        
        # Write rows
        for row in data:
            writer.writerow([
                row.get("id"),
                row.get("temperature"),
                row.get("date"),
                row.get("Time Stamp")
            ])
            
        output.seek(0)
        
        # Return CSV response
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=temperature_records.csv"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)