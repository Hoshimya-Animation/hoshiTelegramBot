import re  # Importing the 're' module for regular expression operations
import random  # Importing the 'random' module for generating random numbers
import json  # Importing the 'json' module for working with JSON data
from jikanpy import Jikan  # Importing the 'Jikan' class from the 'jikanpy' module for interacting with the Jikan API (an unofficial MyAnimeList API)
from googletrans import Translator  # Importing the 'Translator' class from the 'googletrans' module for translating text using Google Translate
import os #Importing the 'os' module for working with Operating System
class MangaApp:
    """
    A class to represent an Manga application.

    Attributes
    ----------
    languague_app : str
        The language of the app.
    request_api : Jikan
        An instance of the Jikan API initialized with the specified base URL.
    option : str
        User options.
    mangaSource : str
        The source of the manga.
    translator : Translator
        An instance of the Google Translator.
    translated : str
        Translated text.
    __mangaTitle : str
        The title of the manga (private).
    __mangaTitle_Japanese : str
        The title of the manga in Japanese (private).
    __genderManga : str
        The genre of the manga (private).
    __aired : str
        The airing date of the manga (private).
    __episodes : str
        The number of episodes (private).
    __score : str
        The score of the manga (private).
    __ratingData : str
        The rating data (private).
    __mangaId : int
        The ID of the manga (private).
    __synopsis : str
        The synopsis of the manga (private).
    __status : str
        The status of the manga (private).
    __types : str
        The type of the manga (private).
    __urlPicture : str
        The URL of the manga picture (private).
    mangaData : list
        A list to store manga data.
    mangaSuggest : list
        A list to store suggested manga.
    idDBGender : int
        The ID of the gender in the database.

    Methods
    -------
    __init__():
        Initializes the MangaApp with default values.
    """

    def __init__(self):
        """
        Initializes the MangaApp with default values.
        """
        self.languague_app = str  # Variable to store the language of the app
        self.request_api = Jikan(selected_base='https://api.jikan.moe/v4/')  # Initialize Jikan API with the specified base URL
        self.option = str  # Variable to store user options
        self.mangaSource = ''  # Variable to store the source of the manga
        self.translator = Translator()  # Initialize the Google Translator
        self.translated = str  # Variable to store translated text
        self.__mangaId = int  # Private variable to store the manga ID
        self.__mangaTitle = str  # Private variable to store the manga title
        self.__mangaTitle_Japanese = str  # Private variable to store the manga title in Japanese
        self.__authors = str #Priveate variable to store the author(s)
        self.__themes = str  # Private variable to store the type of the manga
        self.__serialization = str
        self.__volumes = str  # Private variable to store the number of episodes
        self.__chapters = str  # Private variable to store the airing date of the manga
        self.__genderManga = str  # Private variable to store the genre of the manga
        self.__status = str  # Private variable to store the status of the manga
        self.__score = str  # Private variable to store the score of the manga
        self.__synopsis = str  # Private variable to store the synopsis of the manga
        self.__urlPicture = str  # Private variable to store the URL of the manga picture
        self.mangaData = []  # List to store manga data
        self.mangaSuggest = []  # List to store suggested manga
        self.idDBGender = int  # Variable to store the ID of the gender in the database

    def changeLanguage(self, language):
        """
        Change the language of the app.

        Parameters
        ----------
        language : str
            The new language to set for the app.

        Returns
        -------
        str
            The updated language of the app.
        """
        self.languague_app = language.lower()
        return self.languague_app

    def changemangaSource(self, mangaNameSource):
        """
        Change the source of the manga.

        Parameters
        ----------
        mangaNameSource : str
            The new source name for the manga.

        Returns
        -------
        str
            The updated manga source.
        """
        self.mangaSource = mangaNameSource
        return self.mangaSource

    def getOption(self, option):
        """
        Set an option for the app.

        Parameters
        ----------
        option : str
            The option to set for the app.

        Returns
        -------
        str
            The updated option.
        """
        self.option = option.lower()
        return self.option

    def __dataTranslated(self, sourceData, srcLanguage,defaultLang=False) -> str:
        """
        Translate the source data from the source language to the app's language.

        Parameters
        ----------
        sourceData : str
            The data to be translated.
        srcLanguage : str
            The source language of the data.
        defaultLang: bool
            Change language to English.
        Returns
        -------
        str
            The translated and cleaned data.
        """
        if defaultLang:
            sourceData = self.translator.translate(sourceData, src=srcLanguage, dest='en').text
        else:
            try:
                sourceData = self.translator.translate(sourceData, src=srcLanguage, dest=self.languague_app).text
            except Exception as e:
                sourceData = self.translator.translate(sourceData, src=srcLanguage, dest='en').text
        new_sourceData = sourceData.replace('\u200b', '').replace('\n\n', '')
        return str(new_sourceData)
    def __fillMangaData(self, rand) -> list:
        """
        Fills the manga data based on the source and random flag.
        
        Parameters:
        rand (bool): A flag to determine if the data should be fetched randomly or based on the source.
        
        Returns:
        list: A list containing the manga data.
        """
        if self.mangaSource != '' and rand == False:  # Check if the manga source is not empty and rand is False
            search = self.request_api.search('manga', self.mangaSource)  # Search for the manga using the Jikan API
            self.__mangaId = search['data'][0]['mal_id']  # Get the manga ID from the search results
            dataManga = self.request_api.manga(self.__mangaId)  # Fetch detailed manga data using the manga ID
            self.mangaTitle = self.__dataTranslated(dataManga['data']['title_japanese'], 'ja')  # Translate the manga title to Japanese
            self.mangaTitle = "{} ({})".format(self.__dataTranslated(dataManga['data']['title_japanese'], srcLanguage='ja',defaultLang=True),self.mangaTitle)
            self.__mangaTitle_Japanese = dataManga['data']['title_japanese']  # Store the original Japanese title
            listAuthors = [auth['name'] for auth in dataManga['data']['authors']]
            listAuthors = [name.replace(",","") for name in listAuthors]
            listSerialization = [ser['name'] for ser in dataManga['data']['serializations']]
            listGenders = [gen['name'] for gen in dataManga['data']['genres']]  # Extract the genres of the manga
            self.translated_gender = [self.__dataTranslated(g, 'en') for g in listGenders]  # Translate the genres to English
            listThemes = [thems['name'] for thems in dataManga['data']['themes']] # Extract the themes of the manga
            self.translatedTheme = [self.__dataTranslated(g,'en')for g in listThemes]
            self.__authors = ", ".join(map(str,listAuthors))
            self.__serialization = ", ".join(map(str,listSerialization))
            self.__themes = "#" + " #".join(map(str,self.translatedTheme))
            self.__genderManga = "#" + " #".join(map(str, self.translated_gender))  # Format the genres as a string
            self.__chapters = str(dataManga['data']['chapters'])
            self.__volumes = str(dataManga['data']['volumes'])  # Store the number of episodes
            self.__score = str(dataManga['data']['score'])  # Store the score of the manga
            self.__status = self.__dataTranslated(dataManga['data']['status'], 'en')  # Translate the status of the manga
            self.__synopsis = self.__dataTranslated(dataManga['data']['synopsis'], 'en')  # Translate the synopsis
            self.__urlPicture = str(dataManga['data']['images']['jpg']['large_image_url'])  # Store the URL of the manga picture
            self.mangaData.extend([
                self.mangaTitle, self.__mangaTitle_Japanese, self.__authors,self.__themes,
                self.__serialization,self.__volumes, self.__chapters, self.__genderManga,
                self.__status, self.__score, self.__synopsis,self.__urlPicture
            ])  # Add all the collected data to the MangaData list
            return self.mangaData  # Return the list containing the manga data
        elif (self.mangaSource == '' or self.mangaSource != '') and rand == True:  # Check if the manga source is empty and rand is True
            id_manga_rand = self.request_api.random('manga')  # Fetch a random manga using the Jikan API
            try:
                self.__mangaId = id_manga_rand['data']['mal_id']  # Get the manga ID from the random anime data
                dataManga = self.request_api.manga(self.__mangaId)  # Fetch detailed anime data using the manga ID
                self.mangaTitle = self.__dataTranslated(dataManga['data']['title_japanese'], 'ja')  # Translate the manga title to Japanese
                # Translate the manga title to Japanese to English and any languague
                self.mangaTitle = "{} ({})".format(self.__dataTranslated(dataManga['data']['title_japanese'], srcLanguage='ja',defaultLang=True),self.mangaTitle)
                self.__mangaTitle_Japanese = dataManga['data']['title_japanese']  # Store the original Japanese title
                listAuthors = [auth['name'] for auth in dataManga['data']['authors']]
                listAuthors = [name.replace(",","") for name in listAuthors]
                listSerialization = [ser['name'] for ser in dataManga['data']['serializations']]
                listGenders = [gen['name'] for gen in dataManga['data']['genres']]  # Extract the genres of the manga
                self.translated_gender = [self.__dataTranslated(g, 'en') for g in listGenders]  # Translate the genres to English
                listThemes = [thems['name'] for thems in dataManga['data']['themes']] # Extract the themes of the manga
                self.translatedTheme = [self.__dataTranslated(g,'en')for g in listThemes]
                self.__authors = ", ".join(map(str,listAuthors))
                self.__serialization = ", ".join(map(str,listSerialization))
                self.__themes = "#" + " #".join(map(str,self.translatedTheme))
                self.__genderManga = "#" + " #".join(map(str, self.translated_gender))  # Format the genres as a string
                self.__chapters = str(dataManga['data']['chapters'])
                self.__volumes = str(dataManga['data']['volumes'])  # Store the number of episodes
                self.__score = str(dataManga['data']['score'])  # Store the score of the manga
                self.__status = self.__dataTranslated(dataManga['data']['status'], 'en')  # Translate the status of the manga
                self.__synopsis = self.__dataTranslated(dataManga['data']['synopsis'], 'en')  # Translate the synopsis
                self.__urlPicture = str(dataManga['data']['images']['jpg']['large_image_url'])  # Store the URL of the manga picture
                self.mangaData.extend([
                    self.mangaTitle, self.__mangaTitle_Japanese, self.__authors,self.__themes,
                    self.__serialization,self.__volumes, self.__chapters, self.__genderManga,
                    self.__status, self.__score, self.__synopsis,self.__urlPicture
                ])  # Add all the collected data to the MangaData list
            except:
                pass  # Handle any exceptions that occur
            return self.mangaData  # Return the list containing the manga data

    def __getMangaByIDGender(self, gender) -> int:
        """
        Retrieves an manga ID based on the provided gender.

        Args:
            gender (str): The gender for which to retrieve an manga ID.

        Returns:
            int: The ID of the manga corresponding to the provided gender.
        """
        js_file = os.path.join(os.getcwd(),'idgenders/idsgenManga.json') # Change directory and find the file
        file = open(js_file)  # Open the JSON file containing gender IDs
        idsGen = json.load(file)  # Load the JSON data into a dictionary
        self.idDBGender = random.choice(idsGen[str(gender)])  # Select a random ID from the list corresponding to the provided gender
        return self.idDBGender  # Return the selected manga ID
    def __getSuggestions(self, gender) -> list:
        """
        Retrieves a list of suggested manga details based on the provided gender.

        Args:
            gender (str): The gender for which to retrieve manga suggestions.

        Returns:
            list: A list containing details of the suggested manga.
        """
        self.__getMangaByIDGender(gender=gender)  # Retrieve an manga ID based on the provided gender
        try:
            setAnimeID = self.request_api.manga(self.idDBGender)  # Fetch anime details using the retrieved manga ID
            self.__mangaId = setAnimeID['data']['mal_id']  # Extract the anime ID from the fetched data
            dataManga = self.request_api.manga(self.__mangaId)  # Fetch detailed manga data using the manga ID
            self.mangaTitle = self.__dataTranslated(dataManga['data']['title_japanese'], 'ja')  # Translate the manga title to Japanese
            self.mangaTitle = "{} ({})".format(self.__dataTranslated(dataManga['data']['title_japanese'], srcLanguage='ja',defaultLang=True),self.mangaTitle)
            self.__mangaTitle_Japanese = dataManga['data']['title_japanese']  # Store the original Japanese title
            listAuthors = [auth['name'] for auth in dataManga['data']['authors']]
            listAuthors = [name.replace(",","") for name in listAuthors]
            listSerialization = [ser['name'] for ser in dataManga['data']['serializations']]
            listGenders = [gen['name'] for gen in dataManga['data']['genres']]  # Extract the genres of the manga
            self.translated_gender = [self.__dataTranslated(g, 'en') for g in listGenders]  # Translate the genres to English
            listThemes = [thems['name'] for thems in dataManga['data']['themes']] # Extract the themes of the manga
            self.translatedTheme = [self.__dataTranslated(g, 'en') for g in listThemes]
            self.__authors = ", ".join(map(str,listAuthors))
            self.__serialization = ", ".join(map(str,listSerialization))
            self.__themes = "#" + " #".join(map(str,self.translatedTheme))
            self.__genderManga = "#" + " #".join(map(str, self.translated_gender))  # Format the genres as a string
            self.__chapters = str(dataManga['data']['chapters'])
            self.__volumes = str(dataManga['data']['volumes'])  # Store the number of episodes
            self.__score = str(dataManga['data']['score'])  # Store the score of the manga
            self.__status = self.__dataTranslated(dataManga['data']['status'], 'en')  # Translate the status of the manga
            self.__synopsis = self.__dataTranslated(dataManga['data']['synopsis'], 'en')  # Translate the synopsis
            self.__urlPicture = str(dataManga['data']['images']['jpg']['large_image_url'])  # Store the URL of the manga picture
            self.mangaSuggest.extend([
                self.mangaTitle, self.__mangaTitle_Japanese, self.__authors,self.__themes,
                self.__serialization,self.__volumes, self.__chapters, self.__genderManga,
                self.__status, self.__score, self.__synopsis,self.__urlPicture
            ])  # Add all the collected data to the MangaData list
        except:
            pass  # Handle any exceptions that occur during the process
        return self.mangaSuggest  # Return the list of suggested manga details
    def getSuggestbyGenre(self, genderChoose) -> list:
        """
        Get a list of manga suggestions based on the chosen genre.

        Parameters
        ----------
        genderChoose : str
            The genre chosen by the user.

        Returns
        -------
        list
            A list of suggested manga.
        """
        self.mangaSuggest = []
        while self.__getSuggestions(genderChoose) == []:
            continue  # Keep trying until suggestions are found
        return self.mangaSuggest

    def getMangaData(self) -> list:
        """
        Get manga data based on the source and user option.
    
        Returns
        -------
        list
            A list of manga data.
        """
        if self.mangaSource != '' and self.option == 'usermanga':  # Check if the manga source is specified and the option is 'usermanga'
            self.mangaData = []
            try:
                self.__fillMangaData(False)  # Fill manga data without random selection
                return self.mangaData  # Return the filled manga data
            except:
                return []  # Return an empty list if an exception occurs
        elif (self.mangaSource == '' or self.mangaSource !='') and self.option == 'randmanga':  # Check if the manga source is not specified and the option is 'randmanga'
            self.mangaData = []
            while self.__fillMangaData(True) == []:  # Keep trying to fill data with random selection until successful
                continue  # Continue the loop until data is filled
            return self.mangaData  # Return the filled manga data
    def getMangaID(self):
        return self.__mangaId
