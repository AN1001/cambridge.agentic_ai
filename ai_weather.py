import requests
import google.generativeai as genai
import os
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_user_location() -> str:
    "Gets the users current location and returns a string with the city name"
    return "Cambridge"

def get_cambridge_weather() -> str:
    """
    Fetches the current weather for Cambridge, UK using the OpenWeatherMap API.
    
    Returns:
        A formatted string with weather information, or an error message.
    """
    api_key = os.environ["OPEN_WEATHER_API_KEY"]  # Replace with your actual API key
    base_url = f"http://api.openweathermap.org/geo/1.0/direct?q=Cambridge&limit=5&appid={api_key}"
    city = "Cambridge,uk"
    
    #my api key is not yet activated - we'll imagine it is and returns the following
    return """       
        {
        "lat": 52.2297,
        "lon": 21.0122,
        "timezone": "Europe/Cambridge",
        "timezone_offset": 3600,
        "data": [
            {
            "dt": 1645888976,
            "sunrise": 1645853361,
            "sunset": 1645891727,
            "temp": 279.13,
            "feels_like": 276.44,
            "pressure": 1029,
            "humidity": 64,
            "dew_point": 272.88,
            "uvi": 0.06,
            "clouds": 0,
            "visibility": 10000,
            "wind_speed": 3.6,
            "wind_deg": 340,
            "weather": [
                {
                "id": 800,
                "main": "Clear",
                "description": "clear sky",
                "icon": "01d"
                }
            ]
            }
        ]
        }
                   
    """

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Check if the city was found
        if data["cod"] != 200:
            return f"Error: {data['message']}"

        main_data = data["main"]
        weather_desc = data["weather"][0]["description"]
        
        temperature = main_data["temp"]
        humidity = main_data["humidity"]
        
        return f"Current weather in {city}: {weather_desc}. Temperature: {temperature}°C, Humidity: {humidity}%."
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


model = genai.GenerativeModel('gemini-2.5-flash', tools=[get_cambridge_weather])
chat = model.start_chat(enable_automatic_function_calling=True)

prompt = input("Enter prompt or enter 'exit' > ")
while prompt!='exit':
    response = chat.send_message(prompt)
    print(response.text)
    prompt = input("Enter prompt or enter 'exit' > ")
