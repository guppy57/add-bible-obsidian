import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROD_DIRECTORY = "/Users/guppy57/GuppyBrain/Bible Studies/Indexes"
DEV_DIRECTORY = "./test_topics"

BIBLE_ID = "bba9f40183526463-01" # BSB
BIBLE_CODE = "BSB"
BIBLE_API_URL = "https://api.scripture.api.bible/v1/bibles"

key = os.environ["BIBLE_API_KEY"]

bible_dictionary = {
    "Genesis": "GEN",
    "Exodus": "EXO",
    "Leviticus": "LEV",
    "Numbers": "NUM",
    "Deuteronomy": "DEU",
    "Joshua": "JOS",
    "Judges": "JDG",
    "Ruth": "RUT",
    "1 Samuel": "1SA",
    "2 Samuel": "2SA",
    "1 Kings": "1KI",
    "2 Kings": "2KI",
    "1 Chronicles": "1CH",
    "2 Chronicles": "2CH",
    "Ezra": "EZR",
    "Nehemiah": "NEH",
    "Esther": "EST",
    "Job": "JOB",
    "Psalms": "PSA",
    "Proverbs": "PRO",
    "Ecclesiastes": "ECC",
    "Song of Solomon": "SNG",
    "Isaiah": "ISA",
    "Jeremiah": "JER",
    "Lamentations": "LAM",
    "Ezekiel": "EZK",
    "Daniel": "DAN",
    "Hosea": "HOS",
    "Joel": "JOL",
    "Amos": "AMO",
    "Obadiah": "OBA",
    "Jonah": "JON",
    "Micah": "MIC",
    "Nahum": "NAM",
    "Habakkuk": "HAB",
    "Zephaniah": "ZEP",
    "Haggai": "HAG",
    "Zechariah": "ZEC",
    "Malachi": "MAL",
    "Matthew": "MAT",
    "Mark": "MRK",
    "Luke": "LUK",
    "John": "JHN",
    "Acts": "ACT",
    "Romans": "ROM",
    "1 Corinthians": "1CO",
    "2 Corinthians": "2CO",
    "Galatians": "GAL",
    "Ephesians": "EPH",
    "Philippians": "PHP",
    "Colossians": "COL",
    "1 Thessalonians": "1TH",
    "2 Thessalonians": "2TH",
    "1 Timothy": "1TI",
    "2 Timothy": "2TI",
    "Titus": "TIT",
    "Philemon": "PHM",
    "Hebrews": "HEB",
    "James": "JAS",
    "1 Peter": "1PE",
    "2 Peter": "2PE",
    "1 John": "1JN",
    "2 John": "2JN",
    "3 John": "3JN",
    "Jude": "JUD",
    "Revelation": "REV",
}

def make_request(path):
    url = BIBLE_API_URL + path

    try:
        with requests.get(url, headers={"api-key": key}) as response:
            if response.status == 200:
                print("Found verse")
                return response.json()
            elif response.status == 404:
                print("Verse missing")
                return None
    except Exception as e:
        print(f"KEY HIT EXCEPTION: {e}")

def get_formatted_verse(text):
    formatted = text.strip()
    formatted = formatted.replace("\n    \n    ", "")
    formatted = formatted.replace("[", "<sup> ")
    formatted = formatted.replace("]", " </sup>")

    return f"> {formatted}\n"

def get_verse_text(verse_id):
    params = "content-type=text&include-notes=false&include-chapter-numbers=false&include-verse-numbers=true&include-verse-spans=false"
    path = f"/{BIBLE_ID}/verses/{verse_id}?{params}"
    resp = make_request(path)

    if resp and "data" in resp:
        return get_formatted_verse(resp["data"]["content"])
    return ""

def get_book_id_and_chapter(book_chapter):
    components = book_chapter.split(" ")

    if len(components) == 2:
        return bible_dictionary.get(components[0]), components[1]
    elif len(components) == 3:
      return bible_dictionary.get(f"{components[0]} {components[1]}"), components[2]

def get_subfolders(directory):
    # Create a Path object
    path = Path(directory)

    # Use list comprehension to get all subfolder names
    subfolders = [folder.name for folder in path.iterdir() if folder.is_dir()]

    return subfolders

def convert_all_indexes(directory):
    subfolders = get_subfolders(directory=directory)

    for sf in subfolders:
        path = os.path.join(directory, sf)
        files = os.listdir(path)

        for index in files:
            with open(os.path.join(path, index), "r") as file:
                new_file_text = ""

                for line in file:
                    if line.startswith("#"):
                        cleaned_line = line.replace("###### ", "")
                        split_line = cleaned_line.split(":")
                        print(split_line)

                        book_chapter = split_line[0].strip()
                        verses = None

                        book_id, chapter = get_book_id_and_chapter(book_chapter)

                        try:
                          verses = split_line[1].strip()
                        except:
                          print(f"{book_chapter} has no verses, need full chapter")

                        if verses == None:
                          new_file_text = new_file_text + f"[[{book_chapter}]]"
                        else:
                          header = f"> [!bible]+ [[{book_chapter}]]{f":{verses}" if verses else ""} ({BIBLE_CODE})"
                          new_file_text = new_file_text + header

                          if "-" in verses:
                              verses_split = verses.split("-")
                              start = int(verses_split[0])
                              end = int(verses_split[1])

                              for i in range (start, end):
                                  verse_id = f"{book_id}.{chapter}.{i}" 
                                  text = get_verse_text(verse_id)
                                  new_file_text = new_file_text + text
                          else:
                              verse_id = f"{book_id}.{chapter}.{int(verses)}"
                              text = get_verse_text(verse_id)
                              new_file_text = new_file_text + text

                        new_file_text = new_file_text + "\n\n"
                
                new_file = open(os.path.join("./topics", sf, index), "w")
                new_file.write(new_file_text)
                new_file.close()

convert_all_indexes(DEV_DIRECTORY)