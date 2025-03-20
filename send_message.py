import http.client
import urllib
import os
from datetime import datetime


def send_push_notification(message, priority='1'):
    """Sendet eine Push-Nachricht mit der aktuellen Zeit."""
    token = os.getenv('TOKEN')
    user = os.getenv('USER')

    if not token or not user:
        error_message = "⚠️ TOKEN oder USER nicht gesetzt. Bitte überprüfe deine Umgebungsvariablen."
        print(error_message)
        send_error_notification(error_message)
        return

    # Aktuelle Zeit formatieren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{message}\n🕒 {current_time}"

    conn = http.client.HTTPSConnection("api.pushover.net", 443)
    data = urllib.parse.urlencode({
        "token": token,
        "user": user,
        "title": "Push Notification",
        "message": full_message,
        "priority": priority,
        "sound": "magic"
    })
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    try:
        conn.request("POST", "/1/messages.json", data, headers)
        response = conn.getresponse()
        
        if response.status == 200:
            print("✅ Push-Nachricht erfolgreich gesendet!")
        else:
            error_message = f"❌ Fehler beim Senden der Push-Nachricht: {response.status}\nAntwort: {response.read().decode()}"
            print(error_message)
            send_error_notification(error_message)
    
    except Exception as e:
        error_message = f"⚠️ Ausnahmefehler beim Senden der Push-Nachricht: {e}"
        print(error_message)
        send_error_notification(error_message)
    
    finally:
        conn.close()


def send_error_notification(error_message):
    """Sendet eine Push-Nachricht mit einer Fehlerbenachrichtigung."""
    send_push_notification(f"🚨 Fehler: {error_message}", priority='2')


if __name__ == "__main__":
    send_push_notification("Testnachricht gesendet!")