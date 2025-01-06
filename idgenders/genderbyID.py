# Import the Jikan class from the jikanpy library, which is used to interact with the MyAnimeList API
from jikanpy import Jikan
# Import the getIDAnime function from the mal_dbid module, which is presumably used to get the ID of an anime
from mal_dbid import getIDAnime
# Import the getIDManga function from the mal_dbid module, which is presumably used to get the ID of a manga
from mal_dbid import getIDManga
# Import the json module, which is used for working with JSON data
import json
# Import the os module, which provides a way of using operating system dependent functionality
import os
# Import the time module, which provides various time-related functions
import time
# Import the sys module to access command-line arguments
import sys 



# Define a class named gendersIDs
class gendersIDs:
    """ A class to handle and categorize gender data for Anime and Manga. 
        Attributes: 
            animeID (list): List of Anime IDs. 
            mangaID (list): List of Manga IDs. 
            optionRaw (str): Specifies whether 'Anime' or 'Manga' data is being handled. 
            get_genders (dict): Dictionary to store gender data. 
            gender (str): Attribute for individual gender. 
            contact (Jikan): Instance of the Jikan class for API interaction. 
            list_genders (list): List of predefined genre categories. 
            values_ids (list): List to store IDs of various genres. 
            dicm (dict): Dictionary for additional data. 
            Methods: commonList(listg, id_g): Updates genre lists with the given ID. 
            listDic(): Creates a dictionary where genres are mapped to their indices. 
            uploadDict(): Populates the dicm dictionary and creates the get_genders dictionary. 
            returnJsonDict(): Saves the get_genders dictionary to a JSON file based on the optionRaw attribute. 
            runList(): Processes the list of IDs, fetches details from the API, and categorizes them into genres. 
    """
    # Define the constructor method for the class
    def __init__(self, IDS,optionName) -> None:
        # Initialize the animeID attribute with the provided IDS parameter
        self.animeID = IDS
        # Initialize the mangaID attribute with the provided IDS parameter
        self.mangaID = IDS
        # Initialize the optionRaw attribute with the provieded optionName parameter
        self.optionRaw = optionName
        # Initialize an empty dictionary to store genders
        self.get_genders = {}
        # Initialize an empty string for gender
        self.gender = ''
        # Create an instance of the Jikan class with a specified base URL for the API
        self.contact = Jikan(selected_base='https://api.jikan.moe/v4/')
        # Initialize a list of anime genres
        self.list_genders = ['Action', 'Comedy', 'Horror', 'Sports', 'Adventure', 'Drama',
                             'Mystery', 'Supernatural', 'Avant Garde', 'Fantasy', 'Romance',
                             'Suspense', 'Award Winning', 'Girls Love', 'Sci-Fi', 'Boys Love',
                             'Gourmet', 'Slice of Life', 'Ecchi', 'Erotica', 'Hentai']
        # Initialize empty lists for each genre
        self.Action = []
        self.Comedy = []
        self.Horror = []
        self.Sports = []
        self.Adventure = []
        self.Drama = []
        self.Mystery = []
        self.Avant = []
        self.Fantasy = []
        self.Romance = []
        self.Supernatural = []
        self.Suspense = []
        self.Award = []
        self.Girls = []
        self.Sci = []
        self.Boys = []
        self.Gourmet = []
        self.Slice = []
        self.Erotica = []
        self.Ecchi = []
        self.Hentai = []
        # Initialize an empty list to store values of IDs
        self.values_ids = []
        # Initialize an empty dictionary for additional data
        self.dicm = {}

    # Define a method named commonList within the gendersIDs class
    def commonList(self, listg, id_g):
        # Create a dictionary that maps genre names to their corresponding lists
        genre_map = {
            'Action': self.Action,
            'Comedy': self.Comedy,
            'Horror': self.Horror,
            'Adventure': self.Adventure,
            'Sports': self.Sports,
            'Drama': self.Drama,
            'Mystery': self.Mystery,
            'Supernatural': self.Supernatural,
            'Avant Garde': self.Avant,
            'Fantasy': self.Fantasy,
            'Romance': self.Romance,
            'Suspense': self.Suspense,
            'Award Winning': self.Award,
            'Girls Love': self.Girls,
            'Sci-Fi': self.Sci,
            'Boys Love': self.Boys,
            'Gourmet': self.Gourmet,
            'Slice of Life': self.Slice,
            'Ecchi': self.Ecchi,
            'Erotica': self.Erotica,
            'Hentai': self.Hentai
        }
        # Iterate over each genre in the list of genres
        for g in self.list_genders:
            # If the genre is in the provided list and also in the genre_map dictionary
            if g in listg and g in genre_map:
                # Append the given ID to the corresponding genre list
                genre_map[g].append(id_g)
        # Extend the values_ids list with all values from the genre_map dictionary
        self.values_ids.extend(genre_map.values())
        # Return the updated values_ids list
        return self.values_ids
    # Define a method named listDic within the gendersIDs class
    def listDic(self):
        # Create a dictionary where each genre is mapped to its index in the list_genders
        self.dicm = {item: index for index, item, in enumerate(self.list_genders)}
        # Return the created dictionary
        return self.dicm
    
    # Define a method named uploadDict within the gendersIDs class
    def uploadDict(self):
        # Call the listDic method to populate the dicm dictionary
        self.listDic()
        # Create a dictionary mapping genres to their corresponding lists of IDs
        self.get_genders = {key: value for key, value in zip(self.dicm.keys(), self.values_ids)}
        # Return the created dictionary
        return self.get_genders
    
    # Define a method named returnJsonDict within the gendersIDs class
    def returnJsonDict(self):
        if self.optionRaw == 'Anime':
            # Define the path to the JSON file
            path = './idsgenAnime.json'
            # Check if the file already exists
            if os.path.isfile(path):
                # If the file exists, open it in write mode and dump the get_genders dictionary into it
                with open('idsgenAnime.json', 'w') as file:
                    json.dump(self.get_genders, file, indent=4)
            else:
                # If the file does not exist, create it and dump the get_genders dictionary into it
                with open('idsgenAnime.json', 'a') as file:
                    json.dump(self.get_genders, file, indent=4)
        elif self.optionRaw == 'Manga':
            # Define the path to the JSON file
            path = './idsgenManga.json'
            # Check if the file already exists
            if os.path.isfile(path):
                # If the file exists, open it in write mode and dump the get_genders dictionary into it
                with open('idsgenManga.json', 'w') as file:
                    json.dump(self.get_genders, file, indent=4)
            else:
                # If the file does not exist, create it and dump the get_genders dictionary into it
                with open('idsgenManga.json', 'a') as file:
                    json.dump(self.get_genders, file, indent=4)
    # Define a method named runList within the gendersIDs class
    def runList(self): 
        # Set the correct method for fetching data based on the option
        ids_method = self.contact.anime if self.optionRaw == "Anime" else self.contact.manga
        # Set the correct list of IDs based on the option
        id_list = self.animeID if self.optionRaw == "Anime" else self.mangaID
        # Initialize counter r to 0
        r = 0
        # Enumerate over the list of IDs
        for i, num in enumerate(id_list):
            try:
                # Fetch details using the selected method (anime or manga)
                ids = ids_method(num)
                # Extract the list of genre names from the fetched data
                genres = [genre['name'] for genre in ids['data']['genres']]
                # Call the commonList method to update genre lists with the current ID
                self.commonList(genres, num)
                # Print the current registration number
                print(f"Registo: {i+1}/{len(id_list)}", flush=True)
                # Increment the counter r
                r += 1
                # If r is equal to 3, sleep for 3 seconds and reset r
                if r == 3:
                    time.sleep(3)
                    # Reset the counter r to 0
                    r = 0
            except:
                # If an exception occurs, pass and continue
                pass
        # Call the uploadDict method to update the get_genders dictionary
        self.uploadDict()
        # Call the returnJsonDict method to save the dictionary to a JSON file
        self.returnJsonDict()


def updateData():
    """
    Update data based on the command-line argument.

    This function checks the first command-line argument and updates data
    for either 'Anime' or 'Manga'. It prints the chosen class and executes
    the update process.

    Args:
        None

    Raises:
        Exception: If any error occurs during the update process.

    Example:
        $ python genderbyID.py Anime
        Anime

        $ python genderbyID.py Manga
        Manga
    """
    try:
        # Check the first command-line argument; set classData to 'Anime' or 'Manga'
        classData = 'Anime' if sys.argv[1] == 'Anime' else 'Manga'
        # If classData is 'Anime', update JSON IDs using getIDAnime() function
        if classData == 'Anime':
            updateJsonIds = gendersIDs(getIDAnime(), classData)
            updateJsonIds.runList()
        else:
            # If classData is 'Manga', also update JSON IDs using getIDAnime() function
            updateJsonIds = gendersIDs(getIDAnime(), classData)
            updateJsonIds.runList()
    except Exception as e:
        # Print any error that occurs during the execution
        print(f"An Error occurred: {e}")

# Call the updateData function to execute the update process
updateData()

