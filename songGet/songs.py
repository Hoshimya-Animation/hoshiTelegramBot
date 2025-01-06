import re  # Import the regular expression module
import os  # Import the OS module to interact with the operating system
import sys  # Import the sys module to interact with the interpreter
import shutil  # Import the shutil module for file operations
import os.path  # Import os.path module for file path operations
import mutagen  # Import the mutagen module for handling audio metadata
from mutagen.mp4 import MP4  # Import the MP4 class from mutagen.mp4 for handling MP4 files
from jikanpy import Jikan  # Import the Jikan class from jikanpy for interacting with the Jikan API
from pytubefix import YouTube  # Import the YouTube class from pytubefix for downloading videos
from pytubefix.cli import on_progress  # Import the on_progress function for progress callbacks
from youtube_search import YoutubeSearch  # Import the YoutubeSearch class for searching YouTube

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Add the parent directory to the system path
sys.path.append(parent_dir)
# Import the AnimeApp class from the apiget.animeapi module
from apiget.animeapi import AnimeApp

# Define a class named songsAnime
class songsAnime:
    def __init__(self) -> None:
        """
        Initialize the attributes for the songsAnime class.
        """
        self.idAnime = int
        self.request_api = Jikan(selected_base='https://api.jikan.moe/v4/')
        self.urlId = str
        self.songsDirectory = "animeSongs"
        self.songsBool = False
        self.urlPattern = r'\?v=([^&]+)'
        self.generalRegex =  r"^(.*)\sby\s([^()]+(?:\([^()]+\))?)"
        self.secondRegex =  r'"(.+?)" by (.+?) \(eps.*\)'
        self.themesBool = False
        self.songName = str
        self.singerName = str
        self.themes = str
        self.goodTitle = str
        self.goodArtist = str
    def updateString(self,pathAudio):
        """
        Extract and update the title and artist metadata of an audio file.
    
        This function reads the metadata from the specified audio file and updates the attributes
        with the title and artist information extracted from the file.
    
        Parameters:
            pathAudio (str): The path to the audio file.
    
        Returns:
            tuple: A tuple containing the title and artist of the audio file.
    
        Example:
            title, artist = updateString('/path/to/audio/file.m4a')
            print(f"Title: {title}, Artist: {artist}")
    
        Raises:
            KeyError: If the metadata keys 'titl' or 'arti' are not found in the file.
            mutagen.MutagenError: If there is an error in processing the file with mutagen.
        """
    
        metaDataSong = mutagen.File(f'{pathAudio}')
        self.goodTitle =''.join(metaDataSong[f'titl'])
        self.goodArtist = ''.join(metaDataSong[f'arti'])
        return self.goodTitle,self.goodArtist
    
    def hasOpenings(self):
        """
        Check if the anime has openings and endings.
        
        Returns:
            bool: True if both openings and endings exist, False otherwise.
        """
        if not len(self.themes['data']['openings']) == 0 and (not len(self.themes['data']['endings']) == 0):
            self.songsBool = True
            return self.songsBool
        else:
            self.songsBool = False
            return self.songsBool
    
    def __updateArtist(self, artist):
        """
        Update the artist name.
        
        Parameters:
            artist (str): The artist's name.
        
        Returns:
            str: The updated artist's name.
        """
        self.singerName = artist
        return self.singerName
    
    def __updateNameSong(self, nameSong):
        """
        Update the song name.
        
        Parameters:
            nameSong (str): The song's name.
        
        Returns:
            str: The updated song's name.
        """
        self.songName = nameSong
        return self.songName
    
    def call_request(self):
        """
        Make a request to the Jikan API to get anime themes.
        
        Returns:
            dict: The API response containing anime themes.
        """
        self.themes = self.request_api.anime(self.idAnime, extension='themes')
        return self.themes
    
    def changeID(self, ID):
        """
        Change the anime ID.
        
        Parameters:
            ID (int): The new anime ID.
        
        Returns:
            int: The updated anime ID.
        """
        self.idAnime = ID
        return self.idAnime
    
    def moveFiles(self):
        """
        Move downloaded audio files to the specified directory.
        """
        try:
            current_path = os.getcwd()  # Get the current working directory
            new_dir_path = os.path.join(current_path, self.songsDirectory)  # Create a new directory path
            if not os.path.exists(self.songsDirectory):
                os.makedirs(self.songsDirectory)  # Create the directory if it doesn't exist
            for filename in os.listdir(current_path):
                if filename.endswith('.m4a'):
                    source_file = os.path.join(current_path, filename)  # Define the source file path
                    dest_file = os.path.join(new_dir_path, filename)  # Define the destination file path
                    shutil.move(source_file, dest_file)  # Move the file to the new directory
                    print(f'Moved: {filename}')
        except Exception as e:
            print(f'An error occurred: {e}')
    
    def dowloadYouTube(self, url):
        """
        Download audio from a YouTube video and update its metadata.
        
        Parameters:
            url (str): The URL of the YouTube video.
        """
        yt = YouTube(url, on_progress_callback=on_progress)  # Create a YouTube object with a progress callback
        ys = yt.streams.get_audio_only()  # Get the audio-only stream
        ys.download()  # Download the audio
        for root,dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.m4a'):
                    tagName = MP4(f"{os.path.join(root,file)}")  # Create an MP4 object with the downloaded file
                    tagName.delete()  # Delete existing metadata
                    tagName['title'] = u"{}".format(f'{yt.title}')  # Set the title metadata
                    tagName['artist'] = u"{}".format(f'{yt.author}')  # Set the artist metadata
                    tagName.save()  # Save the updated metadata
        self.moveFiles()  # Move the downloaded files to the specified directory
    
    def __createTarget(self):
        """
        Create the target directory for storing downloaded songs.
        """
        try:
            os.mkdir(self.songsDirectory)  # Create the directory
        except FileExistsError:
            pass  # Ignore if the directory already exists
        except PermissionError:
            print(f"Permission denied: Unable to create")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __cutSingerString(self, song):
        """
        Extract the song name and singer from a song string.
        
        Parameters:
            song (str): The song string.
        
        Returns:
            tuple: The extracted song name and singer name.
        """
        #General case pattern
        match_g = re.search(self.generalRegex,song)
        match_s = re.findall(self.secondRegex,song)
        if match_s:
            songN, artistN = re.findall(self.secondRegex,song)[0]
            return songN,artistN
        elif match_g:
            songN = match_g.group(1).strip()
            artistN = match_g.group(2).strip()
            return songN,artistN
    
    def __cutDataYouTube(self, data):
        """
        Extract the YouTube video ID from a URL.
        
        Parameters:
            data (str): The YouTube URL.
        
        Returns:
            str: The extracted YouTube video ID.
        """
        id_urlYB = re.search(self.urlPattern, data)
        id_urlYB = id_urlYB.group(1)
        return id_urlYB
    
    def __searchYB(self):
        """
        Search for a YouTube video URL based on the song name and singer.
        
        Returns:
            str: The YouTube video URL.
        """
        get_url = YoutubeSearch(f'{self.singerName} {self.songName}', max_results=1).to_dict()
        get_url = get_url[0]['url_suffix']
        uri = self.__cutDataYouTube(get_url)
        url = 'http://youtube.com/watch?v=' + uri
        return url
    
    def getSongs(self):
        """
        Download and process songs from the anime.
        """
        #try:
        self.openingsLenList = len(self.themes['data']['openings'])  # Get the number of openings
        for i in range(0, self.openingsLenList):
            song = self.themes['data']['openings'][i]  # Get the opening song
            songs, artist = self.__cutSingerString(song)  # Extract the song name and singer
            self.__updateNameSong(songs)  # Update the song name
            self.__updateArtist(artist)  # Update the artist name
            self.__createTarget()  # Create the target directory
            self.dowloadYouTube(self.__searchYB())  # Download the song from YouTube
        self.openingsLenList = len(self.themes['data']['endings'])  # Get the number of endings
        for i in range(0, self.openingsLenList):
            song = self.themes['data']['endings'][i]  # Get the ending song
            songs, artist = self.__cutSingerString(song)  # Extract the song name and singer
            self.__updateNameSong(songs)  # Update the song name
            self.__updateArtist(artist)  # Update the artist name
            self.__createTarget()  # Create the target directory
            self.dowloadYouTube(self.__searchYB())  # Download the song from YouTube
        #except:
            #pass
    
    def destroyDirectory(self, dir_path):
        """
        Delete the specified directory and its contents.
        
        Parameters:
            dir_path (str): The path of the directory to delete.
        """
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)  # Remove the directory and its contents
                print(f"Removed files")
            else:
                print("Path Wrong!")
        except Exception as e:
            print(f"An error occurred: {e}")

