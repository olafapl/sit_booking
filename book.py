from requests_html import HTMLSession
from urllib.parse import parse_qs, urlparse
from time import sleep
from datetime import datetime, timedelta
from dateparser import parse as parse_datetime
import argparse
import sys


# iBooking studio IDs
studios = {
    "gløshaugen": 306,
    "dragvoll": 307,
    "portalen": 308,
    "dmmh": 402,
    "moholt": 540
}


# iBooking activity IDs
activities = {
    "egentrening": 419380
}


def log_in(session: HTMLSession, username: str, password: str) -> bool:
    return session.post("https://www.sit.no/trening",
                        data={"name": username, "pass": password, "form_id": "user_login"}).ok


def get_token(session: HTMLSession) -> str:
    response = session.get("https://www.sit.no/trening/treneselv")
    ibooking_src = response.html.find("#ibooking-iframe", first=True).attrs["src"]
    return parse_qs(urlparse(ibooking_src).query)["token"][0]


def get_schedule(session: HTMLSession, studio: int, token: str) -> dict:
    params = {"studios": studio, "token": token}
    response = session.get("https://ibooking.sit.no/webapp/api/Schedule/getSchedule",
                           params=params)
    return response.json()


def add_booking(session: HTMLSession, token: str, class_id: int) -> bool:
    data = {"classId": class_id, "token": token}
    return session.post("https://ibooking.sit.no/webapp/api/Schedule/addBooking", data=data).ok


def book(session: HTMLSession, start: str, days: int, studio: str) -> bool:
    now = datetime.now()
    training_start = (now + timedelta(days=days)).replace(
        hour=int(start[:2]), minute=int(start[2:]), second=0, microsecond=0)

    try:
        token = get_token(session)
        schedule = get_schedule(session, studios[studio], token)
        current_date = datetime.now().date()
        for day in schedule["days"]:
            if (current_date + timedelta(days=days)) == parse_datetime(day["date"]).date():
                for training_class in day["classes"]:
                    if training_class["activityId"] == activities["egentrening"] and parse_datetime(
                            training_class["from"]) == \
                            training_start:
                        booking_start = parse_datetime(training_class["bookingOpensAt"])
                        if datetime.now() < booking_start:
                            opens_in = booking_start - datetime.now()
                            print(f"Booking opens in {str(opens_in).split('.')[0]}. Going to sleep ...")
                            sleep(opens_in.total_seconds())
                        return add_booking(session, token, training_class["id"])
                print("Could not find a training slot at the given time.")
                return False

    except Exception:
        print("An error has occurred. :-(")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Book training slots (egentrening) at Sit.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("username", type=str, help="Sit username (email)")
    parser.add_argument("password", type=str, help="Sit password")
    parser.add_argument("--time", type=str, metavar="hhmm", help="start time (example: 0730)", required=True)
    parser.add_argument("--days", type=int, default=2, help="number of days until training slot (0 is today)")
    parser.add_argument("--studio", type=str, default="gløshaugen", choices=studios.keys(), help="studio")
    args = parser.parse_args()

    session = HTMLSession()
    success = log_in(session, args.username, args.password)
    if success:
        success = book(session, args.time, args.days, args.studio)
    session.close()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
