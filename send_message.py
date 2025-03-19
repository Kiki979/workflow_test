import http.client
import urllib
import os
# from dotenv import load_dotenv

# load_dotenv()

def send_push_notification(message):
   
    token = os.getenv('TOKEN')
    user = os.getenv('USER')

    conn = http.client.HTTPSConnection("api.pushover.net", 443)
    data = urllib.parse.urlencode({
        "token": token,
        "user": user,
        "title": "Message Test",
        "message": message,
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
