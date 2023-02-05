from langdetect import *
import json


def detect_language(text: str) -> str:
    """
    Detect the language of a text
    :param text: The text to detect
    :return: The language of the text
    """
    return detect(text)


def detect_languages(text: str) -> str:
    """
    Detect the languages of a text
    :param text: The text to detect
    :return: The languages of the text
    """
    return detect_langs(text)


class Bad_Words:
    """
    Class to manage bad words
    """
    LANGUAGE: str = ""
    COUNTRY: str = ""
    BAD_WORDS: list = []

    def __init__(self, Bad_Words_Database: {str: str, str: str, str: list}) -> None:
        """
        Constructor
        :param Bad_Words_Database: The bad words database
        """
        self.LANGUAGE = Bad_Words_Database["Language"]
        self.COUNTRY = Bad_Words_Database["Country"]
        self.BAD_WORDS = Bad_Words_Database["Bad_Words_List"]

    def check_bad_words(self, text: str) -> bool:
        """
        Check if a text has bad words
        :param text: The text to check
        :return: True if the text has bad words, False otherwise
        """
        for bad_word in self.BAD_WORDS:
            if bad_word in text:
                return True

        return False

    def toString(self) -> str:
        """
        Get the bad words in a string
        :return: The bad words in a string
        """
        return "Language: " + self.LANGUAGE + "\nCountry: " + self.COUNTRY + "\nBad Words: " + str(self.BAD_WORDS)


class List_Bad_Words:
    """
    Class to manage a list of bad words
    """
    JSON_FILE_LINKS_BAD_WORDS: str = ""
    BAD_WORDS_DATABASE: {str: Bad_Words} = {}

    def __init__(self, json_file_links_bad_words: str) -> None:
        """
        Constructor
        :param json_file_links_bad_words: The file to load the bad words from
        """
        self.JSON_FILE_LINKS_BAD_WORDS = json_file_links_bad_words
        try:
            self.add_bad_words_language_from_json()
        except FileNotFoundError:
            pass

    def add_bad_words(self, key_Langue: str, bad_words: Bad_Words) -> None:
        """
        Add bad words to the database
        :param key_Langue: The key of the bad words
        :param bad_words: The bad words to add
        """
        self.BAD_WORDS_DATABASE[key_Langue] = bad_words

    def add_bad_words_language(self, key_Langue: str, language: str, country: str, bad_words_list: list) -> None:
        """
        Add bad words to the database
        :param key_Langue: The key of the bad words
        :param language: The language of the bad words
        :param country: The country of the bad words
        :param bad_words_list: The bad words list
        """
        self.BAD_WORDS_DATABASE[key_Langue] = Bad_Words(
            {
                "Language": language,
                "Country": country,
                "Bad_Words_List": bad_words_list
            }
        )

    def add_bad_words_language_from_json(self) -> None:
        """
        Add bad words to the database from a json file
        :raise FileNotFoundError: If the json file doesn't exist
        :return: None
        """
        try:
            with open(self.JSON_FILE_LINKS_BAD_WORDS, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("The file " + self.JSON_FILE_LINKS_BAD_WORDS + " doesn't exist")

        key_list = list(json_data.keys())

        for key in key_list:
            self.add_bad_words(key, Bad_Words(json_data[key]))

    def add_bad_words_language_to_json(self, key_Langue: str, bad_words: Bad_Words) -> None:
        """
        Add bad words to the database and to the json file
        :param key_Langue: The key of the bad words
        :param bad_words: The bad words to add
        :raise FileNotFoundError: If the json file doesn't exist
        :return: None
        """
        self.add_bad_words(key_Langue, bad_words)

        try:
            with open(self.JSON_FILE_LINKS_BAD_WORDS, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("The file " + self.JSON_FILE_LINKS_BAD_WORDS + " doesn't exist")

        json_data[key_Langue] = {
            "Language": bad_words.LANGUAGE,
            "Country": bad_words.COUNTRY,
            "Bad_Words_List": bad_words.BAD_WORDS
        }

        with open(self.JSON_FILE_LINKS_BAD_WORDS, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False, sort_keys=True)

    def get_bad_words_language(self, language: str) -> Bad_Words:
        """
        Get the bad words of a language
        :param language: The language of the bad words
        :return: The bad words of the language
        """
        return self.BAD_WORDS_DATABASE[language]

    def get_key(self) -> list:
        """
        Get the key of a language
        :return: The key of the language
        """
        return list(self.BAD_WORDS_DATABASE.keys())

    def check_bad_words_language(self, text: str, language: str) -> bool:
        """
        Check if a text has bad words
        :param text: The text to check
        :param language: The language to check
        :return: True if the text has bad words, False otherwise
        """
        return self.BAD_WORDS_DATABASE[language].check_bad_words(text)

    def check_bad_words(self, text: str) -> bool:
        """
        Check if a text has bad words
        :param text: The text to check
        :return: True if the text has bad words, False otherwise
        """
        language = detect_language(text)
        return self.check_bad_words_language(text, language)

    def toString(self) -> str:
        """
        Get the bad words in a string
        :return: The bad words in a string
        """
        text: str = "{"
        for key in self.BAD_WORDS_DATABASE:
            text += key + ": " + self.BAD_WORDS_DATABASE[key].toString() + ", "
        text = text[:-2] + "}"
        return text


if "__main__" == __name__:
    list_Bad_Words: List_Bad_Words = List_Bad_Words(json_file_links_bad_words="../Data/JSON/Bad_Word.json")

    bad_Words: Bad_Words = Bad_Words(
        Bad_Words_Database={
            "Language": "français",
            "Country": "France",
            "Bad_Words_List": []
        }
    )
    list_Bad_Words.add_bad_words_language_to_json("fr", bad_Words)
