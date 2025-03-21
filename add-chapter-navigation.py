import os
from dotenv import load_dotenv

load_dotenv()

bible_books = [
    ("Genesis", 50, "GEN", "OT", 1, 50),
    ("Exodus", 40, "EXO", "OT", 1, 40),
    ("Leviticus", 27, "LEV", "OT", 1, 27),
    ("Numbers", 36, "NUM", "OT", 1, 36),
    ("Deuteronomy", 34, "DEU", "OT", 1, 34),
    ("Joshua", 24, "JOS", "OT", 1, 24),
    ("Judges", 21, "JDG", "OT", 1, 21),
    ("Ruth", 4, "RUT", "OT", 1, 4),
    ("1 Samuel", 31, "1SA", "OT", 1, 31),
    ("2 Samuel", 24, "2SA", "OT", 1, 24),
    ("1 Kings", 22, "1KI", "OT", 1, 22),
    ("2 Kings", 25, "2KI", "OT", 1, 25),
    ("1 Chronicles", 29, "1CH", "OT", 1, 29),
    ("2 Chronicles", 36, "2CH", "OT", 1, 36),
    ("Ezra", 10, "EZR", "OT", 1, 10),
    ("Nehemiah", 13, "NEH", "OT", 1, 13),
    ("Esther", 10, "EST", "OT", 1, 10),
    ("Job", 42, "JOB", "OT", 1, 42),
    ("Psalms", 150, "PSA", "OT", 1, 144),
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

PROD_DIRECTORY = "/Users/guppy57/GuppyBrain/References/Bible"
DEV_DIRECTORY = "./test_bible"

def fix_my_oopsie(directory):
    for idx, (book, chapters, book_id, testament, skip_start, skip_end) in enumerate(bible_books, start=1):
        print(f"Currently working on {book}, {chapters}, {book_id}, {testament}")

        folder = f"{idx:02d}. {book}"
        OT_GREEK = "Brenton Greek Septuagint"
        NT_GREEK = "1904 Patriarchal Greek New Testament"

        for chapter in range(1, chapters + 1):
            filename = f"{book} {chapter}.md"
            file_path = os.path.join(f"{directory}/{folder}", filename)
            existing_text = ""

            with open(file_path, "r") as file:
                existing_text = file.read()

            previous = f"[[{book} {chapter - 1}|<- {book} {chapter - 1}]] | "
            next = f" | [[{book} {chapter + 1}|{book} {chapter + 1} ->]]"
            navigation = ""

            has_previous = True if chapter > 1 else False
            has_next = True if chapter < chapters else False

            if has_previous:
                navigation += previous

            navigation += f"[[{idx:02d}. Misc - {book}|{book} Miscellanies]]"

            if has_next:
                navigation += next

            html_navigation = f'<div class="bible-nav">{navigation}</div>'

            replaced = existing_text

            replaced = replaced.replace(html_navigation, f"{navigation}")

            with open(file_path, "w") as file:
                file.write(replaced)

            print(f"Finished working on {book} {chapter}")


def add_chapter_nav_to_bible(directory):
    for idx, (book, chapters, book_id, testament, skip_start, skip_end) in enumerate(bible_books, start=1):
        print(f"Currently working on {book}, {chapters}, {book_id}, {testament}")

        folder = f"{idx:02d}. {book}"
        OT_GREEK = "Brenton Greek Septuagint"
        NT_GREEK = "1904 Patriarchal Greek New Testament"

        for chapter in range(1, chapters + 1):
            filename = f"{book} {chapter}.md"
            file_path = os.path.join(f"{directory}/{folder}", filename)
            existing_text = ""

            with open(file_path, "r") as file:
                existing_text = file.read()

            to_replace_top = "##### Berean Standard Bible"
            to_replace_bottom = f"##### {OT_GREEK if testament == "OT" else NT_GREEK}"
            previous = f"[[{book} {chapter - 1}|<- {book} {chapter - 1}]] | "
            next = f" | [[{book} {chapter + 1}|{book} {chapter + 1} ->]]"
            navigation = ""

            has_previous = True if chapter > 1 else False
            has_next = True if chapter < chapters else False

            if has_previous:
                navigation += previous

            navigation += f"[[{idx:02d}. Misc - {book}|{book} Miscellanies]]"

            if has_next:
                navigation += next

            html_navigation = f'<div class="bible-nav">{navigation}</div>'

            replaced = existing_text

            replaced = replaced.replace(to_replace_top, f"{html_navigation}\n\n---\n{to_replace_top}")
            replaced = replaced.replace(to_replace_bottom, f"---\n{html_navigation}\n\n{to_replace_bottom}")

            with open(file_path, "w") as file:
                file.write(replaced)

            print(f"Finished working on {book} {chapter}")


# add_chapter_nav_to_bible(PROD_DIRECTORY)
fix_my_oopsie(PROD_DIRECTORY)
