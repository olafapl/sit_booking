from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, timedelta
import argparse


def log_in(driver, username: str, password: str):
    print("Logger inn ...")
    driver.get("https://www.sit.no")
    sleep(2)
    login_link = driver.find_element_by_link_text("Logg inn")
    login_link.click()
    login_feide = driver.find_element_by_link_text("Logg inn med Feide")
    login_feide.click()

    choose_org = driver.find_element_by_id("org-chooser-selectized")
    choose_org.click()
    choose_org.send_keys("NTNU")
    choose_org.send_keys(Keys.RETURN)
    continue_button = driver.find_element_by_xpath("//*[@id=\"discoform_feide\"]/button")
    continue_button.click()

    username_input = driver.find_element_by_id("username")
    username_input.send_keys(username)
    password_input = driver.find_element_by_id("password")
    password_input.send_keys(password)
    login_button = driver.find_element_by_xpath("//*[@id=\"main\"]/div[1]/form/button")
    login_button.click()
    print("Innlogging vellykket!")


facility_checkboxes = {
    "gløshaugen": 1,
    "dragvoll": 2,
    "portalen": 3,
    "moholt": 5
}


def book_slot(driver, start: str, days: int, facility: str):
    print(f"Prøver å booke treningstime {start} om {days} dag(er) ...")
    now = datetime.now()
    training_start = (now + timedelta(days=days)).replace(
        hour=int(start[:2]), minute=int(start[2:]))
    delta = training_start - now

    if delta >= timedelta(days=2):
        opens_in = delta - timedelta(days=2)
        print(f"Booking åpner om {opens_in}. Går i dvale ...")
        sleep(opens_in.seconds)

    try:
        driver.get("https://www.sit.no/trening/treneselv")
        driver.switch_to.frame(driver.find_element_by_id("ibooking-iframe"))

        # Uncheck unwanted facilities.
        for i in range(1, 6):
            if i == facility_checkboxes[facility]:
                continue
            checkbox = driver.find_element_by_xpath(f"//*[@id=\"ScheduleApp\"]/div/div/div[2]/div/button["
                                                    f"{i}]/input")
            checkbox.click()

        # Click on the slot.
        slot = driver.find_element_by_xpath(f"//*[@id=\"ScheduleApp\"]/div/div/div[4]/div[{1 + days}]"
                                            f"/div[(.//*|.)[contains(., '{start[:2]}.{start[2:]}–')]]/div")
        slot.click()
        sleep(1)  # Wait for the modal to fade in.

        # Click on the "book" button in the modal.
        book_button = driver.find_element_by_xpath(
            "//*[@id=\"ScheduleApp\"]/div/div/div[5]/div/div/div[3]/div[8]/button[1]")
        book_button.click()
        sleep(1)  # Wait for the modal to fade in.

        # Click the "OK" button in the confirmation modal.
        ok_button = driver.find_element_by_xpath("//*[@id=\"ModalDiv\"]/div/div/div[2]/button")
        ok_button.click()
        print("Booking vellykket!")
    except:
        print("Det har skjedd en feil :-(")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Book treningstid hos Sit")
    parser.add_argument("brukernavn", type=str, help="Feide-brukernavn")
    parser.add_argument("passord", type=str, help="Feide-passord")
    parser.add_argument("--senter", type=str, default="gløshaugen", choices=facility_checkboxes.keys(),
                        help="treningssenter")
    parser.add_argument("--tid", type=str, metavar="hhmm", help="starttid",
                        required=True)
    parser.add_argument("--dager", type=int, default=0, help="antall dager frem i tid det skal bookes")
    args = parser.parse_args()

    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    log_in(driver, args.brukernavn, args.passord)
    sleep(10)
    book_slot(driver, args.tid, args.dager, args.senter)
    driver.quit()
