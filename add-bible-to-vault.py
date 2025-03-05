import os
import json
import requests
import pythonbible as bible
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

load_dotenv()
driver = None

# Define login credentials
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

bible_books = [
    ("Genesis", 50, "GEN", "OT", 1, 16),
    ("Exodus", 40, "EXO", "OT", 0, 0),
    ("Leviticus", 27, "LEV", "OT", 0, 0),
    ("Numbers", 36, "NUM", "OT", 0, 0),
    ("Deuteronomy", 34, "DEU", "OT", 0, 0),
    ("Joshua", 24, "JOS", "OT", 0, 0),
    ("Judges", 21, "JDG", "OT", 0, 0),
    ("Ruth", 4, "RUT", "OT", 0, 0),
    ("1 Samuel", 31, "1SA", "OT", 0, 0),
    ("2 Samuel", 24, "2SA", "OT", 0, 0),
    ("1 Kings", 22, "1KI", "OT", 0, 0),
    ("2 Kings", 25, "2KI", "OT", 0, 0),
    ("1 Chronicles", 29, "1CH", "OT", 0, 0),
    ("2 Chronicles", 36, "2CH", "OT", 0, 0),
    ("Ezra", 10, "EZR", "OT", 0, 0),
    ("Nehemiah", 13, "NEH", "OT", 0, 0),
    ("Esther", 10, "EST", "OT", 0, 0),
    ("Job", 42, "JOB", "OT", 0, 0),
    ("Psalms", 150, "PSA", "OT", 0, 0),
    ("Proverbs", 31, "PRO", "OT", 0, 0),
    ("Ecclesiastes", 12, "ECC", "OT", 0, 0),
    ("Song of Solomon", 8, "SNG", "OT", 0, 0),
    ("Isaiah", 66, "ISA", "OT", 0, 0),
    ("Jeremiah", 52, "JER", "OT", 0, 0),
    ("Lamentations", 5, "LAM", "OT", 0, 0),
    ("Ezekiel", 48, "EZK", "OT", 0, 0),
    ("Daniel", 12, "DAN", "OT", 0, 0),
    ("Hosea", 14, "HOS", "OT", 0, 0),
    ("Joel", 3, "JOL", "OT", 0, 0),
    ("Amos", 9, "AMO", "OT", 0, 0),
    ("Obadiah", 1, "OBA", "OT", 0, 0),
    ("Jonah", 4, "JON", "OT", 0, 0),
    ("Micah", 7, "MIC", "OT", 0, 0),
    ("Nahum", 3, "NAM", "OT", 0, 0),
    ("Habakkuk", 3, "HAB", "OT", 0, 0),
    ("Zephaniah", 3, "ZEP", "OT", 0, 0),
    ("Haggai", 2, "HAG", "OT", 0, 0),
    ("Zechariah", 14, "ZEC", "OT", 0, 0),
    ("Malachi", 4, "MAL", "OT", 0, 0),
    ("Matthew", 28, "MAT", "NT", 0, 0),
    ("Mark", 16, "MRK", "NT", 0, 0),
    ("Luke", 24, "LUK", "NT", 0, 0),
    ("John", 21, "JHN", "NT", 0, 0),
    ("Acts", 28, "ACT", "NT", 0, 0),
    ("Romans", 16, "ROM", "NT", 0, 0),
    ("1 Corinthians", 16, "1CO", "NT", 0, 0),
    ("2 Corinthians", 13, "2CO", "NT", 0, 0),
    ("Galatians", 6, "GAL", "NT", 0, 0),
    ("Ephesians", 6, "EPH", "NT", 0, 0),
    ("Philippians", 4, "PHP", "NT", 0, 0),
    ("Colossians", 4, "COL", "NT", 0, 0),
    ("1 Thessalonians", 5, "1TH", "NT", 0, 0),
    ("2 Thessalonians", 3, "2TH", "NT", 0, 0),
    ("1 Timothy", 6, "1TI", "NT", 0, 0),
    ("2 Timothy", 4, "2TI", "NT", 0, 0),
    ("Titus", 3, "TIT", "NT", 0, 0),
    ("Philemon", 1, "PHM", "NT", 0, 0),
    ("Hebrews", 13, "HEB", "NT", 0, 0),
    ("James", 5, "JAS", "NT", 0, 0),
    ("1 Peter", 5, "1PE", "NT", 0, 0),
    ("2 Peter", 3, "2PE", "NT", 0, 0),
    ("1 John", 5, "1JN", "NT", 0, 0),
    ("2 John", 1, "2JN", "NT", 0, 0),
    ("3 John", 1, "3JN", "NT", 0, 0),
    ("Jude", 1, "JUD", "NT", 0, 0),
    ("Revelation", 22, "REV", "NT", 0, 0),
]

DIRECTORY = "/Users/guppy57/GuppyBrain/References/Bible"
# DIRECTORY = "/Users/guppy57/Downloads/Bible copy"

BSB_BIBLE_ID = "bba9f40183526463-01"
OT_HEBREW_BIBLE_ID = (
    "0b262f1ed7f084a6-01",
    "The Hebrew Bible, Westminister Leningrad Codex",
)
NT_HEBREW_BIBLE_ID = (
    "a8a97eebae3c98e4-01",
    "Biblica® Open Hebrew Living New Testament 2009",
)
OT_GREEK_BIBLE_ID = ("c114c33098c4fef1-01", "Brenton Greek Septuagint")
NT_GREEK_BIBLE_ID = ("901dcd9744e1bf69-01", "1904 Patriarchal Greek New Testament")

BIBLE_API_URL = "https://api.scripture.api.bible/v1/bibles"

key1 = os.environ["BIBLE_API_KEY_1"]
key2 = os.environ["BIBLE_API_KEY_2"]
key3 = os.environ["BIBLE_API_KEY_3"]
key4 = os.environ["BIBLE_API_KEY_4"]
key5 = os.environ["BIBLE_API_KEY_5"]
key6 = os.environ["BIBLE_API_KEY_6"]
api_keys = [key1, key2, key3, key4, key5, key6]
current_api_key_num = 0


def retrieve_new_api_key():
    global driver, current_api_key_num
    print(f"Current AKN {current_api_key_num}")
    current_api_key_num = current_api_key_num + 1
    print(f"New AKN: {current_api_key_num}")

    if current_api_key_num > len(api_keys) - 1:
        print("Getting login page")

        if driver is not None:
            driver.quit()

        driver = webdriver.Chrome()

        driver.get("https://scripture.api.bible/login")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        print("Hitting submit button")
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.url_changes("https://scripture.api.bible"))

        print("Opening new app page")
        driver.get("https://scripture.api.bible/admin/applications/new")

        application_name = f"bible-to-markdown-{current_api_key_num}"
        description = "Placing bible in markdown on my desktop"
        commercial = "Non-commercial"

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "application[name]"))
        ).send_keys(application_name)
        driver.find_element(By.NAME, "application[description]").send_keys(description)

        dropdown = Select(driver.find_element(By.ID, "application_commercial_id"))
        dropdown.select_by_value(commercial)

        print("Submitting form")
        driver.find_element(By.NAME, "commit").click()

        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.ID, "user-key"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        api_key_element = soup.find("code", {"id": "user-key"})
        new_api_key = None

        if api_key_element:
            new_api_key = api_key_element.text.strip()
            print("Extracted API Key:", new_api_key)
        else:
            print("API Key not found")

        driver.quit()
        driver = None
        api_keys.append(new_api_key)

    return None


def make_request(path):
    url = BIBLE_API_URL + path
    api_key = api_keys[current_api_key_num]

    try:
        response = requests.get(url, headers={"api-key": api_key})

        if response.status_code == 200:
            print("Found verse")
        elif response.status_code == 404:
            print("Verse missing")
        else:
            print(f"Some exception: {response.text}")
            retrieve_new_api_key()
            return make_request(path)

        return response
    except Exception as e:
        # assumption is that we hit a rate limit
        print(f"KEY_1 HIT EXCEPTION: {e}")
        retrieve_new_api_key()
        return make_request(path)


def get_verse_text(bible, verse_id):
    params = "content-type=text&include-notes=false&include-chapter-numbers=false&include-verse-numbers=true&include-verse-spans=false"
    path = f"/{bible}/verses/{verse_id}?{params}"
    resp = make_request(path)

    data = json.loads(resp.text)
    print(data)
    return data["data"]["content"]


def get_formatted_verse(text):
    formatted = text.strip()
    formatted = formatted.replace("\n    \n    ", "\n    ")
    formatted = formatted.replace("[", '<span class="bible-verse-number">')
    formatted = formatted.replace("]", "</span>")
    return formatted + "\n"


def import_bible_into_existing_bible_files(directory):
    for idx, (book, chapters, book_id, testament, skip_start, skip_end) in enumerate(bible_books, start=1):
        print(f"Currently working on {book}, {chapters}, {book_id}, {testament}")

        folder = f"{idx:02d}. {book}"
        book_val = bible.Book(idx)

        print(f"Found book value: {book_val}")

        hebrew_id, hebrew_name = (
            OT_HEBREW_BIBLE_ID if testament == "OT" else NT_HEBREW_BIBLE_ID
        )
        greek_id, greek_name = (
            OT_GREEK_BIBLE_ID if testament == "OT" else NT_GREEK_BIBLE_ID
        )

        print(f"Using: {hebrew_name} and {greek_name}")

        for chapter in range(1, chapters + 1):
            if skip_start <= chapter <= skip_end:
                print(f"{book} {chapter}")
                continue

            filename = f"{book} {chapter}.md"
            file_path = os.path.join(f"{directory}/{folder}", filename)

            print(f"Writing to: {filename}\nPath: {file_path}")

            open("filename", "w").close()  # deletes all existing content

            # get number of verses using api
            num_of_verses = bible.get_number_of_verses(book_val, chapter)
            print(f"Number of verses: {num_of_verses}")

            english_scripture = "##### Berean Standard Bible\n\n"
            greek_scripture = f"##### {greek_name}\n\n"
            hebrew_scripture = f"##### {hebrew_name}\n\n"

            for i in range(1, num_of_verses + 1):
                verse_id = f"{book_id}.{chapter}.{i}"
                print(verse_id)

                try:
                    english = get_verse_text(BSB_BIBLE_ID, verse_id)
                    print(f"English: {english}")
                    english_scripture += get_formatted_verse(english)
                except Exception as e:
                    print(e)

                try:
                    greek = get_verse_text(greek_id, verse_id)
                    print(f"Greek: {greek}")
                    greek_scripture += get_formatted_verse(greek)
                except Exception as e:
                    print(e)

                try:
                    hebrew = get_verse_text(hebrew_id, verse_id)
                    print(f"Hebrew: {hebrew}")
                    hebrew_scripture += get_formatted_verse(hebrew)
                except Exception as e:
                    print(e)

            with open(file_path, "w") as file:
                file.write(
                    f"---\ncssclasses:\n  - bible-chapter\n---\n{english_scripture}\n\n{greek_scripture}\n\n{hebrew_scripture}\n"
                )

            print(f"Finished working on {book} {chapter}")


import_bible_into_existing_bible_files(DIRECTORY)
# retrieve_new_api_key()

# verses_to_test = [1, 2, 3, 4, 5, 6]
# for i in verses_to_test:
#     verse_text = get_verse_text(BSB_BIBLE_ID, f"GEN.1.{i}")
#     print(verse_text)
