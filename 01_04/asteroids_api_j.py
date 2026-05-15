import requests

start_date = "2026-05-07"
end_date = "2026-05-14"
api_key = "DEMO_KEY"

response = requests.get(
    f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"
)

# print(response)

with open("./asteroids", "a") as f:
    f.write(response.text)
