import time
import requests
import smtplib
from datetime import datetime

MY_LAT = 53.344101
MY_LONG = -6.267490
MY_EMAIL = "jcalinquanttesting@gmail.com"
PASSWORD = "sgcsgtyngdlilmod"
NB_RETRIES = 10
SLEEP_INTERVAL = 10


def is_iss_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(f"Current ISS latitude: {iss_latitude}")
    print(f"Current ISS longitude: {iss_longitude}")

    if MY_LAT-5 < iss_latitude < MY_LAT+5 and MY_LONG-5 < iss_longitude < MY_LONG+5:
        return True
    return False


def is_night_time():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now > sunset or time_now < sunrise:
        return True
    return False


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="jcalinquant@hotmail.com",
            msg=f"Subject:Look up ☝️\n\nISS is above your head")


retry = 0
while retry <= NB_RETRIES:
    retry += 1
    print(f"Attempt nb: {retry}")
    if is_iss_near() and is_night_time():
        print("ISS detected!!!")
        send_email()
        isNotificationSent = True
    time.sleep(SLEEP_INTERVAL)
