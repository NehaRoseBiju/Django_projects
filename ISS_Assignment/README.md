\# Real-Time ISS Location Data Analysis Using Python



\## Project Title



\*\*Real-Time ISS Location Data Analysis Using Python\*\*



\## Objective



The objective of this project is to retrieve the real-time location of the International Space Station (ISS) using a public API, collect location data at regular intervals, analyze the collected data, and visualize the movement of the ISS using Python.



\## Technologies Used



\* Python 3

\* Requests

\* Pandas

\* Matplotlib



\## Python Libraries



Install the required libraries using:



```bash

pip install requests pandas matplotlib

```



\## Project Files



\* `iss\_location.py` – Main Python program

\* `iss\_data.csv` – Collected ISS location data

\* `Latitude\_Graph.png` – Latitude vs Time graph

\* `Longitude\_Graph.png` – Longitude vs Time graph

\* `README.md` – Project documentation



\## API Used



This project uses the following public API to retrieve the real-time location of the ISS:



`https://api.wheretheiss.at/v1/satellites/25544`



> \*\*Note:\*\* The original assignment specified the Open Notify API. Since it was unavailable during implementation, an alternative public ISS API was used to obtain the same latitude and longitude information.



\## Features



\* Retrieves the current ISS location every 5 seconds.

\* Collects 100 consecutive location records.

\* Stores the data in a CSV file.

\* Calculates:



&#x20; \* Maximum Latitude

&#x20; \* Minimum Latitude

&#x20; \* Average Latitude

&#x20; \* Maximum Longitude

&#x20; \* Minimum Longitude

&#x20; \* Average Longitude

\* Plots:



&#x20; \* Latitude vs Time

&#x20; \* Longitude vs Time

\* Saves graphs as image files.



\## How to Run



1\. Open the project folder in VS Code.

2\. Activate the Python virtual environment (optional).

3\. Install the required libraries.

4\. Run the program:



```bash

python iss\_location.py

```



5\. Wait approximately \*\*8 minutes and 20 seconds\*\* while 100 records are collected.

6\. After completion, the CSV file and graph images will be generated automatically.



\## Output



The program generates:



\* `iss\_data.csv`

\* `Latitude\_Graph.png`

\* `Longitude\_Graph.png`



It also displays the following statistics in the terminal:



\* Maximum Latitude

\* Minimum Latitude

\* Average Latitude

\* Maximum Longitude

\* Minimum Longitude

\* Average Longitude



\## Conclusion



The project successfully demonstrates how Python can be used to retrieve, store, analyze, and visualize real-time IoT-style data. The collected ISS location data shows the continuous movement of the International Space Station around the Earth, while the generated graphs provide a clear visualization of changes in latitude and longitude over time.



