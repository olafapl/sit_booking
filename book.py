from requests_html import HTMLSession
from urllib.parse import parse_qs, urlparse
from time import sleep
from datetime import datetime, timedelta
from dateparser import parse as parse_datetime
import argparse
import sys

# iBooking studio IDs
STUDIOS = {
    "gløshaugen": 306,
    "dragvoll": 307,
    "portalen": 308,
    "dmmh": 402,
    "moholt": 540,
}

# iBooking activity IDs
ACTIVITIES = {"egentrening": 419380}


def log_in(session: HTMLSession, username: str, password: str) -> None:
    session.post(
        "https://www.sit.no/trening",
        data={"name": username, "pass": password, "form_id": "user_login"},
    ).raise_for_status()


def get_token(session: HTMLSession) -> str:
    response = session.get("https://www.sit.no/trening/treneselv")
    response.raise_for_status()
    ibooking_src = response.html.find("#ibooking-iframe", first=True).attrs["src"]
    return parse_qs(urlparse(ibooking_src).query)["token"][0]


def get_schedule(session: HTMLSession, studio: int, token: str) -> dict:
    params = {"studios": studio, "token": token}
    response = session.get(
        "https://ibooking.sit.no/webapp/api/Schedule/getSchedule", params=params
    )
    response.raise_for_status()
    return response.json()


def add_booking(session: HTMLSession, token: str, class_id: int) -> None:
    data = {"classId": class_id, "token": token}
    session.post(
        "https://ibooking.sit.no/webapp/api/Schedule/addBooking", data=data
    ).raise_for_status()


def book(session: HTMLSession, start: str, days: int, studio: str) -> bool:
    training_start = (datetime.now() + timedelta(days=days)).replace(
        hour=int(start[:2]), minute=int(start[2:]), second=0, microsecond=0
    )

    token = get_token(session)
    schedule = get_schedule(session, STUDIOS[studio], token)
    current_date = datetime.now().date()
    for day in schedule["days"]:
        if (current_date + timedelta(days=days)) == parse_datetime(day["date"]).date():
            for training_class in day["classes"]:
                if (
                    training_class["activityId"] == ACTIVITIES["egentrening"]
                    and parse_datetime(training_class["from"]) == training_start
                ):
                    booking_start = parse_datetime(training_class["bookingOpensAt"])
                    if datetime.now() < booking_start:
                        opens_in = booking_start - datetime.now()
                        print(
                            f"Booking opens in {str(opens_in).split('.')[0]}. Going to sleep ..."
                        )
                        sleep(opens_in.total_seconds())
                    add_booking(session, token, training_class["id"])
                    return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Book training slots (egentrening) at Sit.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("username", type=str, help="Sit username (email)")
    parser.add_argument("password", type=str, help="Sit password")
    parser.add_argument(
        "--time",
        type=str,
        metavar="hhmm",
        help="start time (example: 0730)",
        required=True,
    )
    parser.add_argument(
        "--days",
        type=int,
        default=2,
        help="number of days until training slot (0 is today)",
    )
    parser.add_argument(
        "--studio",
        type=str,
        default="gløshaugen",
        choices=STUDIOS.keys(),
        help="studio",
    )
    parser.add_argument("--max-tries", type=int, default=2, help="max number of tries")
    args = parser.parse_args()

    success = False
    current_try = 1
    while current_try <= args.max_tries:
        session = HTMLSession()
        try:
            log_in(session, args.username, args.password)
            success = book(session, args.time, args.days, args.studio)
            print(
                "Slot booked!"
                if success
                else "Could not find a training slot matching the provided parameters."
            )
            break
        except Exception:
            if current_try == args.max_tries:
                print("An error occurred.")
        finally:
            session.close()
            current_try += 1

    sys.exit(0 if success else 1)
