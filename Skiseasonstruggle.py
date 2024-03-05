import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import Sendamail
from email.message import EmailMessage
from googleapiclient.discovery import build
import WeerberichtClasses



SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

# Coordinates for different places
coordinates = {
    "solden": {"lat": 46.9655, "lon": 11.0076},
    "Chamonix-Mont Blanc": {"lat": 45.9237, "lon": 6.869},
    "Val di Fassa": {"lat": 46.4424081, "lon": 11.6968477},
    "falera": {"lat": 46.8012, "lon": 9.2305},
    "kaprun": {"lat": 47.8095, "lon": 13.0550},
    "aalberg": {"lat": 47.1948, "lon": 10.1602},
    "killy": {"lat": 45.4692, "lon": 6.9068},
    "Spindleruv Mlyn": {"lat": 50.7261, "lon": 15.6094}
}

# authenticates the mail
def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def main():
    addresses = input("Enter your email addresses separated by commas: ").split(',')

    # Iterate over all locations
    for chosen_place, coordinates in coordinates.items():
        latitude = coordinates["lat"]
        longitude = coordinates["lon"]

        # Get weather data for the chosen place or custom coordinates
        result = WeerberichtClasses.getdata(latitude, longitude)

        if "error" in result:
            print(result["error"])
        else:
            # Extract relevant information from the result
            resultList = list(result.values())
            descriptionList = list(resultList[0].get('description').keys())

            # Scoring based on temperature
            average_temp = (resultList[0].get('min-temp') + resultList[0].get('max-temp')) / 2
            snow_prediction = resultList[0].get('snow')

            score = 0

            if average_temp < 0:
                score = 5
            elif 0 <= average_temp < 5:
                score = 4
            elif 5 <= average_temp < 10:
                score = 3
            elif average_temp >= 10:
                score = 1

            # Additional +1 if more than 5 cm of snow is predicted
            if snow_prediction > 5:
                score += 1

            mail_content = f'''
            Today's Weather Report in {chosen_place} on {resultList[0].get('date')}: \n
            Temperatures range between {resultList[0].get('min-temp')}°C and {resultList[0].get('max-temp')} °C.\n
            Wind speeds up to {resultList[0].get('wind')} km/h are expected.\n
            We expect {descriptionList[0]}.\n
            Score: {score}/5
            '''

            for address in addresses:
                send_gmail("Weather Report", address.strip(), mail_content, authenticate_gmail())

    print("Mails sent with the weather report and score for all locations")

if __name__ == "__main__":
    main()
