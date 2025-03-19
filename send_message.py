import http.client
import urllib
import os
from datetime import datetime
# from dotenv import load_dotenv

# load_dotenv()

def send_push_notification(message):
    """Sendet eine Push-Nachricht mit der aktuellen Zeit."""
   
    token = os.getenv('TOKEN')
    user = os.getenv('USER')

    if not token or not user:
        print("⚠️ TOKEN oder USER nicht gesetzt. Bitte überprüfe deine Umgebungsvariablen.")
        return

    # Aktuelle Zeit formatieren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{message}\n🕒 {current_time}"

    conn = http.client.HTTPSConnection("api.pushover.net", 443)
    data = urllib.parse.urlencode({
        "token": token,
        "user": user,
        "title": "Message Test",
        "message": full_message,
        "priority": '1',
        "sound": "magic"
    })
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    try:
        conn.request("POST", "/1/messages.json", data, headers)
        response = conn.getresponse()

        if response.status == 200:
            print("✅ Push-Nachricht erfolgreich gesendet!")
        else:
            print(f"❌ Fehler beim Senden der Push-Nachricht: {response.status}")
            print("Antwort:", response.read().decode())

    except Exception as e:
        print(f"⚠️ Ausnahmefehler beim Senden der Push-Nachricht: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    send_push_notification("Send message erfolgreich!")
