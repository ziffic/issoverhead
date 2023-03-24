import requests
from datetime import datetime
import smtplib
import connect
import time

my_email = connect.ACCOUNT_EMAIL
password = connect.ACCOUNT_PASSWORD
MY_LAT = 33.787914
MY_LNG = -117.853104


def is_iss_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json", )
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    if (MY_LAT - 5) <= iss_latitude <= (MY_LAT - 5) and (MY_LNG + 5) <= iss_longitude <= (MY_LNG + 5):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="dave@dryweb.com",
                msg=f"Subject: Look Up!\n\nThe ISS space station is overhead."
            )
