import logging  # Import the logging module for handling logs
import time
import os
import mutagen
from botDatabase import (
    start_db,
    updateIDUser,
    updateAge,
    update_age_automatically,
    get_user_age,
    set_language,
    get_language
)
from difflib import SequenceMatcher  # Import SequenceMatcher for string similarity comparison
from googletrans import Translator  # Import Translator from googletrans for text translation
from apiget.animeapi import AnimeApp  # Import AnimeApp from apiget.animeapi for anime-related data
from songGet.songs import songsAnime
from apiget.mangapi import MangaApp
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup  # Import Telegram-related classes
from telegram.ext import (
    Application,  # Import Application for handling different types of interactions
    CommandHandler,  # Import CommandHandler for handling commands
    ContextTypes,  # Import ContextTypes for context management
    MessageHandler,
    CallbackQueryHandler,  # Import CallbackQueryHandler for handling callback queries
    CallbackContext,  # Import CallbackContext for context in callback queries
    filters
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)  # Set up logging configuration

logging.getLogger("httpx").setLevel(logging.WARNING)  # Set log level for httpx module

# Create a logger for this module
logger = logging.getLogger(__name__)  # Initialize logger for this script/module


class telegramBot:
    def __init__(self) -> None:
        # Initialize a dictionary to map language names to their corresponding codes
        self.dict_languages = {
                "Español":"es",
                "English":"en",
                "Français":"fr",
                "Deutsch":"de",
                "Português":"pt",
                "Italiano":"it",
                "Русский":"ru",
                "عرب":"ar",
                "हिंदू":"hi",
                "Română":"ro",
                "日本語":"ja",
                "简体中文":"zh-tw",
                "한국인":"ko"
            }
        # Define a dictionary of bot commands and their descriptions
        self.commands_dictionary = {
            "start":"The bot starts ₍^ >ヮ<^₎ .ᐟ.ᐟ",
            "language":f"Change language of the Bot 🇪🇸➡️🇬🇧",
            "request": f"+'name'. Request information about an anime from MyAnimeList 🗄🔎📺 (japanese or english)",
            "mangarequest": f"+'name'. Request information about a manga from MyAnimeList 🗄🔎📖 (japanese or english)",
            "random": f"Random information about an anime 🎲",
            "mangarand":f"Random information about a manga 🎲📖",
            "hoshiimanga":f"+ 'gender'. Manga suggestion by gender 🍱📖",
            "hoshii": f"+'gender'. Anime suggestion by gender 🌍🍱",
            "showgen":f"Show all available genders 🍘🎎",
            "help":f"Give you information about my functions 🆘❔"
        }
        #
        # List of anime genres
        self.__genders = ['Action', 'Comedy', 'Horror', 'Sports', 'Adventure', 'Drama',
                        'Mystery', 'Supernatural', 'Avant Garde', 'Fantasy', 'Romance',
                        'Suspense', 'Award Winning', 'Girls Love', 'Sci-Fi', 'Boys Love',
                        'Gourmet', 'Slice of Life', 'Ecchi', 'Erotica', 'Hentai']
        # Initialize language-related attributes
        self.language = str
        self.translator = Translator()
        self.sourceLanguage = "en"
        # Placeholder for data 
        self.data = str
        # Initialize an empty dictionary to store information about manga message
        self.info_manga = {
            f"🎥 {'Title'}": "",
            f"🎌 {'Japanese Title'}": "",
            f"✍️ {'Author(s)'}": "",
            f"🟥 {'Themes'}":"",
            f"📚 {'Volumes'}": "",
            f"📔 {'Serialization'}":"",
            f"#️⃣ {'Chapters'}": "",
            f"📝 {'Gender'}": "",
            f"📜 {'Status'}": "",
            f"⭐ {'Score'}": "",
            f"📝 {'Synopsis'}": ""
        }
        # Initialize an empty dictionary to store information messages
        self.info_message = {
            f"🎥 {'Title'}": "",
            f"🎌 {'Japanese Title'}": "",
            f"📺 {'Type'}": "",
            f"🏷️ {'Genre'}":"",
            f"🗓️ {'Aired'}": "",
            f"🖥️ {'Episodes'}": "",
            f"⭐ {'Score'}": "",
            f"🔞 {'Rating'}": "",
            f"📜 {'Status'}": "",
            f"📝 {'Synopsis'}": ""
        }
        # Initialize an empty dictionary to store information about genders
        self.gender_info = {
            f"🔫":"",
            f"😂":"",
            f"🏚":"",
            f"🤾‍♀️":"",
            f"🗺":"",
            f"🎭":"",
            f"🔮":"",
            f"👾":"",
            f"⚔️":"",
            f"🧙‍♂️":"",
            f"💝":"",
            f"🧩":"",
            f"🏆":"",
            f"👭":"",
            f"🧪":"",
            f"👬":"",
            f"🍽":"",
            f"🌅":"",
            f"🫣":"",
            f"❤️👯":"",
            f"🔞💋":""
        }
    def getAbbreviation(self,lang):
        """
        Returns the abbreviation for the specified language
        Args:
            lang (str): Language code (e.g., 'en' for English)
        Returns:
            str: Language abbreviation
        """
        self.language = lang
        return self.language
    def showHelp(self):
        """
        Displays a help message with available commands
        Returns:
            dict: Dictionary of commands and their descriptions
        """
        if self.language == str:
            return self.commands_dictionary
        else:
            # Translate command descriptions if language is not English
            self.commands_dictionary = {x: self.translatedData(y) for x,y in self.commands_dictionary}
            return self.commands_dictionary
    def showGender(self):
        help_gender = '\n'.join(f'{k}: {v}'for k,v in zip(self.gender_info.keys(),self.__genders))
        return help_gender
    def translatedData(self,data) -> str:
        """
        Translates data from the source language to the specified language
        Args:
            data (str): Text to be translated
        Returns:
            str: Translated text
        """
        self.data = self.translator.translate(data,src=self.sourceLanguage,dest=self.language).text
        self.data = self.data.replace('\u200b', '').replace('\n\n', '')
        return self.data
    def getSimilarity(self,gender):
        """
        Finds a gender match based on similarity
        Args:
            gender (str): Gender to compare
        Returns:
            str: Matching gender (if found)
        """
        gender_get  = next((i for i in self.__genders if SequenceMatcher(None, i.lower(), gender).ratio() > 0.5), '')
        return gender_get
# Instances
telebot = telegramBot() # Create an instance of the TelegramBot class
animeApp = AnimeApp() # Create an instance of the AnimeApp class
songAnime = songsAnime()
mangaApp = MangaApp()
start_db()
update_age_automatically()
#Functons for Anime commands
"""Start Command"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the start command for the bot
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    user = update.message.chat
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    age = get_user_age(user_id=user_id)
    updateIDUser(user_id,language=lang,age=age)
    if lang != None:
        telebot.getAbbreviation(str(lang))
        # Send a translated welcome message if the language is not English
        await update.message.reply_text(telebot.translatedData(f"Hi, {user.first_name}!!♡⸜(˃ ᵕ ˂ )⸝ I’m Hoshimya ✨, but you can call me ‘mya-chan’ if you prefer (ᵕ—ᴗ—). I’m at your service! 🌟\nWhat does this bot do? ❓ Well, when boredom strikes, I’ll whisk you away to the world of anime with a recommendation. Share your preferred genre, and I’ll conjure up a suggestion! I understand around 10 languages. 🌐\nWhile there are some things I can’t do, I’ll give my best shot.\nIf you’re a programmer itching to improve something new, go ahead! 👨‍💻👩‍💻 Check out the repository on GitHub. 🐈‍⬛ https://github.com/Hoshimya-Animation/hoshiTelegramBot \nAnd lastly, like the stars and constellations, I’ll be here for you until eternity. ( > 〰 < )♡✨🌃🌍"))
        if age==None:
            await update.message.reply_text(telebot.translatedData(f"How old are you?"))
            context.user_data['awaiting_age'] = True
        else:pass
    else:
        # Send the default welcome message in English
        await update.message.reply_text(f"Hi, {user.first_name}!!♡⸜(˃ ᵕ ˂ )⸝ I’m Hoshimya ✨, but you can call me ‘mya-chan’ if you prefer (ᵕ—ᴗ—). I’m at your service! 🌟\nWhat does this bot do? ❓ Well, when boredom strikes, I’ll whisk you away to the world of anime with a recommendation. Share your preferred genre, and I’ll conjure up a suggestion! I understand around 10 languages. 🌐\nWhile there are some things I can’t do, I’ll give my best shot.\nIf you’re a programmer itching to improve something new, go ahead! 👨‍💻👩‍💻 Check out the repository on GitHub. 🐈‍⬛ https://github.com/Hoshimya-Animation/hoshiTelegramBot \nAnd lastly, like the stars and constellations, I’ll be here for you until eternity. ( > 〰 < )♡✨🌃🌍")
        if age==None:
            await update.message.reply_text(f"How old are you?")
            context.user_data['awaiting_age'] = True
        else:pass
"""Change commands"""
async def changeCommands(application:Application) -> None:
    """
    Updates the bot's commands and chat menu button
    Args:
        application (Application): The application instance
    """
    command = [BotCommand((key),(value)) for key,value in telebot.commands_dictionary.items()]
    await application.bot.set_my_commands(command)
    await application.bot.set_chat_menu_button()

"""Start command menu"""
async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a message with three inline buttons attached for language selection.
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    keyboard = [
        [
            InlineKeyboardButton(f"Español 🇲🇽", callback_data="lang_Español"),
            InlineKeyboardButton(f"English 🇬🇧🇺🇸", callback_data="lang_English"),
            InlineKeyboardButton(f"Français 🇫🇷", callback_data="lang_Français"),
            
        ],
        [   InlineKeyboardButton(f"Deutsch 🇩🇪", callback_data="lang_Deutsch"),
            InlineKeyboardButton(f"Português 🇵🇹🇧🇷", callback_data="lang_Português"),
            InlineKeyboardButton(f"Italiano 🇮🇹", callback_data="lang_Italiano"),
        ],
        [
            InlineKeyboardButton(f"Русский 🇷🇺", callback_data="lang_Русский"),
            InlineKeyboardButton(f"عرب 🇸🇦", callback_data="lang_عرب"),
            InlineKeyboardButton(f"हिंदू 🇮🇳", callback_data="lang_हिंदू"),
        ],
        [
            InlineKeyboardButton(f"Română 🇷🇴", callback_data="lang_Română"),
            InlineKeyboardButton(f"日本語 🇯🇵", callback_data="lang_日本語"),
            InlineKeyboardButton(f"简体中文 🇨🇳", callback_data="lang_简体中文"),
            InlineKeyboardButton(f"한국인 🇰🇷", callback_data="lang_한국인"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    if lang == None:
        await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    else:
        telebot.getAbbreviation(str(lang))
        await update.message.reply_text(telebot.translatedData("Please choose:"), reply_markup=reply_markup)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Parses the CallbackQuery and updates the message text.
    
    Args:
        update (Update): The update received from Telegram.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    lang = get_language(user_id=user_id)
    if lang==None:
        if query.data.split('_')[1] in telebot.dict_languages and query.data.startswith('lang_'):
            # Get the language from the query data
            language = telebot.dict_languages[query.data.split('_')[1]]
            set_language(user_id=user_id,language=language)
            language = get_language(user_id=user_id)
            telebot.getAbbreviation(lang=language)
            # Get the abbreviation for the language
            animeApp.changeLanguage(language=language)
            # Change the language in the animeApp
            await query.edit_message_text(text=f"{telebot.translatedData('Selected option')}: {query.data.split('_')[1]}")
    elif lang!=None:
        if query.data.split('_')[1] in telebot.dict_languages and query.data.startswith('lang_'):
            # Get the language from the query data
            language = telebot.dict_languages[query.data.split('_')[1]]
            set_language(user_id=user_id,language=language)
            language = get_language(user_id=user_id)
            telebot.getAbbreviation(lang=language)
            # Get the abbreviation for the language
            animeApp.changeLanguage(language=language)
            # Change the language in the animeApp
            await query.edit_message_text(text=f"{telebot.translatedData('Selected option')}: {query.data.split('_')[1]}")
async def handle_songs_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the download and sending of anime songs.

    This function fetches songs associated with anime, updates the audio metadata,
    and sends the audio files via the Telegram bot. It also cleans up the directory
    after sending the files.

    Parameters:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the callback.

    Example:
        await handle_songs_download(update, context)

    Raises:
        Exception: If an error occurs during the processing or sending of audio files.
    """
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_language(user_id=user_id)
    try:
        telebot.getAbbreviation(str(lang))
        # Fetch and download songs using the songAnime object
        songAnime.getSongs()
        # Get the current working directory and the new directory path for songs
        current_path = os.getcwd()
        new_dir_path = os.path.join(current_path, songAnime.songsDirectory)
        # Walk through the new directory to find audio files
        for root, dirs, files in os.walk(new_dir_path):
            for file in files:
                audio_path = os.path.join(root, file)
                try:
                    # Split the file name and extension
                    file_root, file_ext = os.path.splitext(file)
                    # Update the audio metadata (title and artist)
                    titleName, artistName = songAnime.updateString(audio_path)
                    # Open the audio file and send it via Telegram bot
                    with open(audio_path, 'rb') as audio_file:
                        await update.callback_query.message.reply_audio(
                            audio=audio_file,
                            filename=file_root,
                            title=f'{titleName}',
                            performer=f'{artistName}'
                        )
                except Exception as e:
                    # Send a failure message if an exception occurs
                    failure_message = telebot.translatedData("Failed! (╥﹏╥)") if lang is not None else "Failed! (╥﹏╥)"
                    await update.callback_query.message.reply_text(failure_message)
        # Pause for 3 seconds before cleaning up the directory
        time.sleep(3)
        # Destroy the directory containing the downloaded songs
        songAnime.destroyDirectory(os.path.join(os.getcwd(), "animeSongs"))
    except Exception as e:
        # Send a failure message if an exception occurs in the main try block
        failure_message = telebot.translatedData("Failed! (╥﹏╥)") if lang is not None else "Failed! (╥﹏╥)"
        await update.callback_query.message.reply_text(failure_message)


async def buttonDownload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle button press events for downloading or canceling song downloads.

    This function processes user input from a callback query button press. If the user
    selects the 'yes_option', it triggers the song download and upload process. If the
    user selects the 'no_option', it cancels the operation. The user data is cleared 
    after processing.

    Parameters:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the callback.

    Example:
        await buttonDownload(update, context)

    Raises:
        None
    """
    query = update.callback_query
    user_id = query.from_user.id 
    lang = get_language(user_id=user_id)
    await query.answer()
    if query.data == 'yes_option':
        if lang == None:
            text = "Downloading and uploading"
            await query.edit_message_text(text=text)
            await handle_songs_download(update,context)
            context.user_data.clear()
        else:
            telebot.getAbbreviation(str(lang))
            text = telebot.translatedData("Downloading and uploading")
            await query.edit_message_text(text=text)
            await handle_songs_download(update, context)
            context.user_data.clear()
    elif query.data == 'no_option':
        text = "Cancelled"
        await query.edit_message_text(text=text)
        context.user_data.clear()
    context.user_data.clear()


"""
Request Random Anime Function

This function handles a user's request for a random anime recommendation.
It interacts with an external anime application to retrieve data and sends
the information back to the user via a Telegram bot.
"""
async def requestRandom(update: Update, context: CallbackContext) -> None:
    """
    Stores the info about the user and ends the conversation.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (CallbackContext): The context object that contains the bot's data and helper functions.
    """
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    age = get_user_age(user_id=user_id)
    
    # Check if the language setting in the telebot is set to a string (indicating English)
    if lang == None:
        try:
            # Change the language of the anime application to English
            animeApp.changeLanguage('en')
            # Request a random anime from the anime application
            animeApp.getOption('randanime')
            # Get the anime data from the anime application
            animedata = animeApp.getAnimeData()
            # Create a help_info string with the anime data formatted as "key: value"
            help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
            # If the help_info string is longer than 1000 characters, truncate it and add ellipses
            if len(help_info)>=1000:
                help_info = help_info[0:997]+"..."
             # Check if the anime is categorized as hentai or erotica 
            is_adult_content = ('#Hentai' in animedata[3] or '#hentai' in animedata[3] or '#Erotica' in animedata[3] or '#erotica' in animedata[3])
            # Check if the anime is categorized as hentai or erotica
            if is_adult_content and (age is None or age <18):
                await update.message.reply_text("Sorry, we cannot show you this content (◞‸◟；)")
            elif is_adult_content and (age>=18):
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
            else:
                if not is_adult_content:
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                        # Send the anime image and information as a photo without a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                        songAnime.changeID(animeApp.getAnimeID())
                        songAnime.call_request()
                        songAnime.hasOpenings()
                        if songAnime.songsBool:
                            keyboard = [
                                [InlineKeyboardButton(f"✅",callback_data='yes_option')],
                                [InlineKeyboardButton(f"❌",callback_data='no_option')]
                            ]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            await update.message.reply_text(f"You have openings and endings inthis    anime. Do you wanna to dowloaded?",reply_markup=reply_markup)
                        else:pass
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
        except:
            await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
    elif lang!= None:
        try:
            telebot.getAbbreviation(str(lang))
            # If the language setting in the telebot is not a string, use the set language
            animeApp.changeLanguage(lang)
            # Request a random anime from the anime application
            animeApp.getOption('randanime')
            # Get the anime data from the anime application
            animedata = animeApp.getAnimeData()
            # Create a help_info string with the anime data formatted as "translated key: value"
            help_info = '\n'.join(f'{telebot.translatedData(k)}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
            # If the help_info string is longer than 1000 characters, truncate it and add ellipses
            if len(help_info)>=1000:
                help_info = help_info[0:997]+"..."
            # Check if the anime is categorized as hentai or erotica
            is_adult_content = ('#Hentai' in animedata[3] or '#hentai' in animedata[3] or '#Erotica' in animedata[3] or '#erotica' in animedata[3])
            # Check if the anime is categorized as hentai or erotica
            if is_adult_content and (age is None or age <18):
                await update.message.reply_text(telebot.translatedData("Sorry, we cannot show you this content (◞‸◟；)"))
            elif is_adult_content and (age>=18):
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
            else:
                if not is_adult_content:
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                        # Send the anime image and information as a photo without a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                        songAnime.changeID(animeApp.getAnimeID())
                        songAnime.call_request()
                        songAnime.hasOpenings()
                        if songAnime.songsBool:
                            keyboard = [
                                [InlineKeyboardButton(f"✅",callback_data='yes_option')],
                                [InlineKeyboardButton(f"❌",callback_data='no_option')]
                            ]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            await update.message.reply_text(telebot.translatedData(f"You have openings and endings in this anime. Do you wanna to dowloaded?"),reply_markup=reply_markup)
                        else:pass
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
        except:
            await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))

"""
Request Anime by User Function

This function handles a user's request for a specific anime recommendation.
It interacts with an external anime application to retrieve data based on the user's input and sends
the information back to the user via a Telegram bot.
"""
async def requestAnime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the user's request for an anime by name.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (ContextTypes.DEFAULT_TYPE): The context object that contains the bot's data and helper functions.
    """
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    age = get_user_age(user_id=user_id)
    # Get the user's input text and split it into command and anime name
    user_input = update.message.text.split(maxsplit=1)
    # Check if the user provided an anime name
    if len(user_input) > 1:
        name = user_input[1]
        # Check if the language setting in the telebot is set to a string (indicating English)
        if lang == None:
            try:
                # Change the language of the anime application to English
                animeApp.changeLanguage('en')
                # Change the anime source in the anime application to the user's input
                animeApp.changeAnimeSource(str(name))
                # Request the user-specified anime from the anime application
                animeApp.getOption('useranime')
                # Get the anime data from the anime application
                animedata = animeApp.getAnimeData()
                # Create a help_info string with the anime data formatted as "key: value"
                help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
                # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                if len(help_info)>=1000:
                    help_info = help_info[0:997]+"..."
                # Check if the anime is categorized as hentai or erotica 
                is_adult_content = ('#Hentai' in animedata[3] or '#hentai' in animedata[3] or '#Erotica' in animedata[3] or '#erotica' in animedata[3])
                # Check if the anime is categorized as hentai or erotica
                if is_adult_content and (age is None or age <18):
                    await update.message.reply_text("Sorry, we cannot show you this content (◞‸◟；)")
                elif is_adult_content and (age>=18):
                    # Notify the user that an anime suggestion is being sent
                    await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                    await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                else:
                    if not is_adult_content:
                        try:
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                            # Send the anime image and information as a photo without a spoiler warning
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                            songAnime.changeID(animeApp.getAnimeID())
                            songAnime.call_request()
                            songAnime.hasOpenings()
                            if songAnime.songsBool:
                                keyboard = [
                                    [InlineKeyboardButton(f"✅",callback_data='yes_option')],
                                    [InlineKeyboardButton(f"❌",callback_data='no_option')]
                                ]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                await update.message.reply_text(f"You have openings and endings in this anime. Do you wanna to dowloaded?",reply_markup=reply_markup)
                            else:
                                pass
                        except:
                            # If an error occurs, notify the user
                            await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
            except:
                # If an error occurs, notify the user
                await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
        elif lang != None:
            try:
                telebot.getAbbreviation(str(lang))
                # If the language setting in the telebot is not a string, use the set language
                animeApp.changeLanguage(lang)
                # Change the anime source in the anime application to the user's input
                animeApp.getOption('useranime')
                # Request the user-specified anime from the anime application
                animeApp.changeAnimeSource(name)
                # Get the anime data from the anime application
                animedata = animeApp.getAnimeData()
                # Create a help_info string with the anime data formatted as "translated key: value"
                help_info = '\n'.join(f'{telebot.translatedData(k)}: {v}'for k,v in zip(telebot.info_message.keys(),animedata))
                # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                if len(help_info)>=1000:
                    help_info = help_info[0:997]+"..."
                # Check if the anime is categorized as hentai or erotica
                is_adult_content = (telebot.translatedData('#Hentai') in animedata[3] or telebot.translatedData('#hentai') in animedata[3] or telebot.translatedData('#Erotica') in animedata[3] or telebot.translatedData('#erotica') in animedata[3])
                # Check if the anime is categorized as hentai or erotica
                if is_adult_content and (age is None or age <18):
                    await update.message.reply_text(telebot.translatedData("Sorry, we cannot show you this content (◞‸◟；)"))
                elif is_adult_content and (age>=18):
                    # Notify the user that an anime suggestion is being sent
                    await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                    await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                else:
                    if not is_adult_content:
                        try:
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                            # Send the anime image and information as a photo without a spoiler warning
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                            animeID = animeApp.getAnimeID()
                            songAnime.changeID(animeApp.getAnimeID())
                            songAnime.call_request()
                            songAnime.hasOpenings()
                            if songAnime.songsBool:
                                keyboard = [
                                    [InlineKeyboardButton(f"✅",callback_data='yes_option')],
                                    [InlineKeyboardButton(f"❌",callback_data='no_option')]
                                ]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                await update.message.reply_text(telebot.translatedData(f"You have openings and endings in this anime. Do you wanna to dowloaded?"),reply_markup=reply_markup)
                            else:
                                pass
                        except:
                            # If an error occurs, notify the user
                            await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
            except:
                # If an error occurs, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
    else:
        # If the user did not provide an anime name, prompt them to type an anime name
        if lang == None:
            response = "Type your anime (ෆ˙ᵕ˙ෆ)♡"
            await update.message.reply_text(response)
        else:
            telebot.getAbbreviation(str(lang))
            response = telebot.translatedData("Type your anime (ෆ˙ᵕ˙ෆ)♡")
            await update.message.reply_text(response)

"""
Request Anime by Gender Function

This function handles a user's request for an anime recommendation by genre.
It interacts with an external anime application to retrieve data based on the user's input and sends
the information back to the user via a Telegram bot.
"""
async def requestgender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the user's request for an anime by genre.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (ContextTypes.DEFAULT_TYPE): The context object that contains the bot's data and helper functions.
    """
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    age = get_user_age(user_id=user_id)
    # Get the user's input text and split it into command and genre name
    user_input = update.message.text.split(maxsplit=1)
    # Check if the user provided a genre name
    if len(user_input) > 1:
        name = user_input[1]
        # Check if the language setting in the telebot is set to a string (indicating English)
        if lang == None:
            try:
                # Change the language of the anime application to English
                animeApp.changeLanguage('en')
                # Get the genre that closely matches the user's input
                gender_ = telebot.getSimilarity(name)
                # If a matching genre is found
                if gender_!='':
                    try:
                        # Request anime suggestions by genre from the anime application
                        animedata = animeApp.getSuggestbyGenre(str(gender_))
                        # Create a help_info string with the anime data formatted as "key: value"
                        help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),    animedata))
                        # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                        if len(help_info)>=1000:
                            help_info = help_info[0:997]+"..."
                        # Check if the anime is categorized as hentai or erotica
                        is_adult_content = ('#Hentai' in animedata[3] or '#hentai' in animedata[3] or   '#Erotica' in animedata[3] or '#erotica' in animedata[3])
                        # Check if the anime is categorized as hentai or erotica
                        if is_adult_content and (age is None or age <18):
                            await update.message.reply_text("Sorry, we cannot show you this content (◞‸◟；)")
                        elif is_adult_content and (age>=18):
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                        else:
                            if not is_adult_content:
                                try:
                                    # Notify the user that an anime suggestion is being sent
                                    await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                                    # Send the anime image and information as a photo without a spoiler warning
                                    await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                                    songAnime.changeID(animeApp.getAnimeID())
                                    songAnime.call_request()
                                    songAnime.hasOpenings()
                                    if songAnime.songsBool:
                                        keyboard = [
                                            [InlineKeyboardButton(f"✅",callback_data='yes_option')],
                                            [InlineKeyboardButton(f"❌",callback_data='no_option')]
                                        ]
                                        reply_markup = InlineKeyboardMarkup(keyboard)
                                        await update.message.reply_text(f"You have openings and endings in this anime. Do you wanna to dowloaded?",reply_markup=reply_markup)
                                    else:pass
                                except:
                                    # If an error occurs, notify the user
                                    await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
                    except:pass
                else:
                    # If no matching genre is found, notify the user
                    await update.message.reply_text("Error! Maybe your gender is not into the list. ( ˶°ㅁ°) !!\nPlease use the command /showgen to show the genders are available. (˶ᵔ ᵕ ᵔ˶)")
            except:
                await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
        elif lang != None:
            try:
                telebot.getAbbreviation(str(lang))
                # If the language setting in the telebot is not a string, use the set language
                animeApp.changeLanguage(lang)
                # Get the genre that closely matches the user's input
                gender_ = telebot.getSimilarity(name)
                # If a matching genre is found
                if gender_!='':
                    try:
                        # Request anime suggestions by genre from the anime application
                        animedata = animeApp.getSuggestbyGenre(str(gender_))
                        # Create a help_info string with the anime data formatted as "translated key: value"
                        help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_message.keys(),    animedata))
                        # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                        if len(help_info)>=1000:help_info = help_info[0:997]+"..."
                        # Check if the anime is categorized as hentai or erotica
                        is_adult_content = (telebot.translatedData('#Hentai') in animedata[3] or telebot.translatedData('#hentai') in animedata[3] or telebot.translatedData('#Erotica') in animedata[3] or telebot.translatedData('#erotica') in animedata[3])
                        # Check if the anime is categorized as hentai or erotica
                        if is_adult_content and (age is None or age <18):
                            await update.message.reply_text(telebot.translatedData("Sorry, we cannot show you this content (◞‸◟；)"))
                        elif is_adult_content and (age>=18):
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=True)
                        else:
                            if not is_adult_content:
                                try:
                                    # Notify the user that an anime suggestion is being sent
                                    await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                                    # Send the anime image and information as a photo without a spoiler warning
                                    await context.bot.send_photo(chat_id=update.message.chat_id,photo=animedata[10],caption=help_info,has_spoiler=False)
                                    songAnime.changeID(animeApp.getAnimeID())
                                    songAnime.call_request()
                                    songAnime.hasOpenings()
                                    if songAnime.songsBool:
                                        keyboard = [
                                            [InlineKeyboardButton(f"✅",callback_data='yes_option')],
                                            [InlineKeyboardButton(f"❌",callback_data='no_option')]
                                        ]
                                        reply_markup = InlineKeyboardMarkup(keyboard)
                                        await update.message.reply_text(telebot.translatedData(f"You have openings and endings in this anime. Do you wanna to dowloaded?"),reply_markup=reply_markup)
                                    else:pass
                                except:
                                    # If an error occurs, notify the user
                                    await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
                else:
                    # If no matching genre is found, notify the user
                    await update.message.reply_text(telebot.translatedData("Error! Maybe your gender is not into the list. ( ˶°ㅁ°) !!\nPlease use the command /showgen to show the genders are available. (˶ᵔ ᵕ ᵔ˶)"))
            except:
                # If an error occurs, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
    else:
        # If the user did not provide a genre name, prompt them to type a genre name
        if lang == None:
            response = "Type your anime (ෆ˙ᵕ˙ෆ)♡"
            await update.message.reply_text(response)
        else:
            telebot.getAbbreviation(str(lang))
            response = telebot.translatedData("Type the gender please (ෆ˙ᵕ˙ෆ)♡")
            await update.message.reply_text(response)
"""
Show Help Function

This function provides help information to the user, displaying the available commands and their descriptions.
"""
async def help(update: Update, context:CallbackContext)->None:
    """
    Provides help information to the user.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (CallbackContext): The context object that contains the bot's data and helper functions.
    """
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    # Check if the language setting in the telebot is not a string (indicating a specific language setting)
    if lang!=None:
        telebot.getAbbreviation(str(lang))
        # Create a help_info string with the translated commands and their descriptions
        help_info = '\n'.join(f'/{x}: {telebot.translatedData(y)}'for x,y in telebot.commands_dictionary.items())
        await update.message.reply_text(help_info)
    else:
        # Create a help_info string with the commands and their descriptions in English
        help_info = '\n'.join(f'/{x}: {y}'for x,y in telebot.commands_dictionary.items())
        await update.message.reply_text(help_info)

async def showGen(update:Update, context:CallbackContext) -> None:
    """
    Provides information about the genders
    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (CallbackContext): The context object that contains the bot's data and helper functions.
    """
    # Check if the language setting in the telebot is not a string (indicating a specific language setting)
    await update.message.reply_text(telebot.showGender())
"""
"""
async def handle_non_command_message(update:Update, context: CallbackContext) -> None:
    text = update.message.text
    user_data = update.message.from_user
    lang = get_language(user_id=user_data['id'])
    if 'awaiting_age' in context.user_data:
        try:
            updateAge(user_data['id'],text)
            await update.message.reply_text("Ok!")
            del context.user_data['awaiting_age']
        except:
            if lang == None:await update.message.reply_text("Error! ( • ᴖ • ｡")
            else:
                telebot.getAbbreviation(str(lang))
                await update.message.reply_text(telebot.translatedData("Error! ( • ᴖ • ｡"))
    else:
        if lang == None and  (not text.startswith("/")):
            await update.message.reply_text("Hey! I didn't receive a command ( • ᴖ • ｡)")
        elif lang != None and  (not text.startswith("/")):
            telebot.getAbbreviation(str(lang))
            await update.message.reply_text(telebot.translatedData("Hey! I didn't receive a command ( • ᴖ • ｡)"))

#Fucntions for Manga commands
async def requestRandomManga(update: Update, context: CallbackContext) -> None:
    """
    Stores the info about the user and ends the conversation.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (CallbackContext): The context object that contains the bot's data and helper functions.
    """
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    age = get_user_age(user_id=user_id)
    # Check if the language setting in the telebot is set to a string (indicating English)
    if lang == None:
        try:
            # Change the language of the anime application to English
            mangaApp.changeLanguage('en')
            # Request a random anime from the anime application
            mangaApp.getOption('randmanga')
            # Get the anime data from the anime application
            mangadata = mangaApp.getMangaData()
            # Create a help_info string with the anime data formatted as "key: value"
            help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_manga.keys(),mangadata))
            # If the help_info string is longer than 1000 characters, truncate it and add ellipses
            if len(help_info)>=1000:
                help_info = help_info[0:997]+"..."
            is_adult_content = ('#Hentai' in mangadata[7] or '#hentai' in mangadata[7] or '#Erotica' in mangadata[7] or '#erotica' in mangadata[7])
            # Check if the anime is categorized as hentai or erotica
            if is_adult_content and (age is None or age <18):
                await update.message.reply_text("Sorry, we cannot show you this content (◞‸◟；)")
            elif is_adult_content and (age>=18):
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=True)
            else:
                if not is_adult_content:
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                        # Send the anime image and information as a photo without a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=False)
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
        except:await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
    elif lang != None:
        try:
            telebot.getAbbreviation(str(lang))
            # If the language setting in the telebot is not a string, use the set language
            mangaApp.changeLanguage(lang)
            # Request a random anime from the anime application
            mangaApp.getOption('randmanga')
            # Get the anime data from the anime application
            mangadata = mangaApp.getMangaData()
            # Create a help_info string with the anime data formatted as "translated key: value"
            help_info = '\n'.join(f'{telebot.translatedData(k)}: {v}'for k,v in zip(telebot.info_manga.keys(),mangadata))
            # If the help_info string is longer than 1000 characters, truncate it and add ellipses
            if len(help_info)>=1000:
                help_info = help_info[0:997]+"..."
            # Check if the anime is categorized as hentai or erotica
            is_adult_content = (telebot.translatedData('#Hentai') in mangadata[7] or telebot.translatedData('#hentai') in mangadata[7] or telebot.translatedData('#Erotica') in mangadata[7] or telebot.translatedData('#erotica') in mangadata[7])
            # Check if the anime is categorized as hentai or erotica
            if is_adult_content and (age is None or age <18):
                await update.message.reply_text(telebot.translatedData("Sorry, we cannot show you this content (◞‸◟；)"))
            elif is_adult_content and (age>=18):
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=True)
            else:
                if not is_adult_content:
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                        # Send the anime image and information as a photo without a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=False)
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
        except:
            await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
async def requestManga(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the user's request for an anime by name.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (ContextTypes.DEFAULT_TYPE): The context object that contains the bot's data and helper functions.
    """
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    age = get_user_age(user_id=user_id)
    # Get the user's input text and split it into command and anime name
    user_input = update.message.text.split(maxsplit=1)
    # Check if the user provided an anime name
    if len(user_input) > 1:
        name = user_input[1]
        # Check if the language setting in the telebot is set to a string (indicating English)
        if lang == None:
            try:
                # Change the language of the anime application to English
                mangaApp.changeLanguage('en')
                # Change the anime source in the anime application to the user's input
                mangaApp.changemangaSource(str(name))
                # Request the user-specified anime from the anime application
                mangaApp.getOption('usermanga')
                # Get the anime data from the anime application
                mangadata = mangaApp.getMangaData()
                # Create a help_info string with the anime data formatted as "key: value"
                help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_manga.keys(),mangadata))
                # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                if len(help_info)>=1000:
                    help_info = help_info[0:997]+"..."
                # Check if the anime is categorized as hentai or erotica
                is_adult_content = ('#Hentai' in mangadata[7] or '#hentai' in mangadata[7] or '#Erotica'in mangadata[7] or '#erotica' in mangadata[7])
                # Check if the anime is categorized as hentai or erotica
                if is_adult_content and (age is None or age <18):
                    await update.message.reply_text("Sorry, we cannot show you this content (◞‸◟；)")
                elif is_adult_content and (age>=18):
                    # Notify the user that an anime suggestion is being sent
                    await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                    await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=True)
                else:
                    if not is_adult_content:
                        try:
                            # Notify the user that an anime suggestion is being sent
                            await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                            # Send the anime image and information as a photo without a spoiler warning
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=False)
                        except:
                            # If an error occurs, notify the user
                            await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
            except:
                await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
        elif lang != None:
            telebot.getAbbreviation(str(lang))
            # If the language setting in the telebot is not a string, use the set language
            mangaApp.changeLanguage(lang)
            # Change the anime source in the anime application to the user's input
            mangaApp.getOption('usermanga')
            # Request the user-specified anime from the anime application
            mangaApp.changemangaSource(name)
            # Get the anime data from the anime application
            mangadata = mangaApp.getMangaData()
            # Create a help_info string with the anime data formatted as "translated key: value"
            help_info = '\n'.join(f'{telebot.translatedData(k)}: {v}'for k,v in zip(telebot.info_manga.keys(),mangadata))
            # If the help_info string is longer than 1000 characters, truncate it and add ellipses
            if len(help_info)>=1000:
                help_info = help_info[0:997]+"..."
            # Check if the anime is categorized as hentai or erotica
            is_adult_content = (telebot.translatedData('#Hentai') in mangadata[7] or telebot.translatedData('#hentai') in mangadata[7] or telebot.translatedData('#Erotica') in mangadata[7] or telebot.translatedData('#erotica') in mangadata[7])
            # Check if the anime is categorized as hentai or erotica
            if is_adult_content and (age is None or age <18):
                await update.message.reply_text(telebot.translatedData("Sorry, we cannot show you this content (◞‸◟；)"))
            elif is_adult_content and (age>=18):
                # Notify the user that an anime suggestion is being sent
                await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=True)
            else:
                if not is_adult_content:
                    try:
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                        # Send the anime image and information as a photo without a spoiler warning
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=False)
                    except:
                        # If an error occurs, notify the user
                        await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
    else:
        # If the user did not provide an anime name, prompt them to type an anime name
        if lang == None:
            response = "Type your manga (ෆ˙ᵕ˙ෆ)♡"
            await update.message.reply_text(response)
        else:
            telebot.getAbbreviation(str(lang))
            response = telebot.translatedData("Type your manga (ෆ˙ᵕ˙ෆ)♡")
            await update.message.reply_text(response)

async def requestGenderManga(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the user's request for an anime by genre.

    Parameters:
    update (Update): The update object that contains all the information about the incoming update.
    context (ContextTypes.DEFAULT_TYPE): The context object that contains the bot's data and helper functions.
    """
    user_id = update.message.from_user['id']
    lang = get_language(user_id=user_id)
    age = get_user_age(user_id=user_id)
    # Get the user's input text and split it into command and genre name
    user_input = update.message.text.split(maxsplit=1)
    # Check if the user provided a genre name
    if len(user_input) > 1:
        name = user_input[1]
        # Check if the language setting in the telebot is set to a string (indicating English)
        if lang == None:
            # Change the language of the anime application to English
            mangaApp.changeLanguage('en')
            # Get the genre that closely matches the user's input
            gender_ = telebot.getSimilarity(name)
            # If a matching genre is found
            if gender_!='':
                try:
                    # Request anime suggestions by genre from the anime application
                    mangadata = mangaApp.getSuggestbyGenre(str(gender_))
                    # Create a help_info string with the anime data formatted as "key: value"
                    help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_manga.keys(),mangadata))
                    # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                    if len(help_info)>=1000:
                        help_info = help_info[0:997]+"..."
                    # Check if the anime is categorized as hentai or erotica
                    is_adult_content = ('#Hentai' in mangadata[7] or '#hentai' in mangadata[7] or '#Erotica'in mangadata[7] or '#erotica' in mangadata[7])
                    # Check if the anime is categorized as hentai or erotica
                    if is_adult_content and (age is None or age <18):
                        await update.message.reply_text("Sorry, we cannot show you this content (◞‸◟；)")
                    elif is_adult_content and (age>=18):
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=True)
                    else:
                        if not is_adult_content:
                            try:
                                # Notify the user that an anime suggestion is being sent
                                await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                                # Send the anime image and information as a photo without a spoiler warning
                                await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=False)
                            except:
                                # If an error occurs, notify the user
                                await update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
                except:update.message.reply_text("Error! Try it again, please. (╥﹏╥)")
            else:
                # If no matching genre is found, notify the user
                await update.message.reply_text("Error! Maybe your gender is not into the list. ( ˶°ㅁ°) !!\nPlease use the command /showgen to show the genders are available. (˶ᵔ ᵕ ᵔ˶)")
        elif lang != None:
            telebot.getAbbreviation(str(lang))
            # If the language setting in the telebot is not a string, use the set language
            mangaApp.changeLanguage(lang)
            # Get the genre that closely matches the user's input
            gender_ = telebot.getSimilarity(name)
            # If a matching genre is found
            if gender_!='':
                try:
                    # Request anime suggestions by genre from the anime application
                    mangadata = mangaApp.getSuggestbyGenre(str(gender_))
                    # Create a help_info string with the anime data formatted as "translated key: value"
                    help_info = '\n'.join(f'{k}: {v}'for k,v in zip(telebot.info_manga.keys(),mangadata))
                    # If the help_info string is longer than 1000 characters, truncate it and add ellipses
                    if len(help_info)>=1000:help_info = help_info[0:997]+"..."
                    # Check if the anime is categorized as hentai or erotica
                    is_adult_content = (telebot.translatedData('#Hentai') in mangadata[7] or telebot.translatedData('#hentai') in mangadata[7] or telebot.translatedData('#Erotica') in mangadata[7] or telebot.translatedData('#erotica') in mangadata[7])
                    # Check if the anime is categorized as hentai or erotica
                    if is_adult_content and (age is None or age <18):
                        await update.message.reply_text(telebot.translatedData("Sorry, we cannot show you this content (◞‸◟；)"))
                    elif is_adult_content and (age>=18):
                        # Notify the user that an anime suggestion is being sent
                        await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                        await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=True)
                    else:
                        if not is_adult_content:
                            try:
                                # Notify the user that an anime suggestion is being sent
                                await update.message.reply_text("Ok!⸜(｡˃ ᵕ ˂ )⸝♡")
                                # Send the anime image and information as a photo without a spoiler warning
                                await context.bot.send_photo(chat_id=update.message.chat_id,photo=mangadata[11],caption=help_info,has_spoiler=False)
                            except:
                                # If an error occurs, notify the user
                                await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
                except:await update.message.reply_text(telebot.translatedData("Error! Try it again, please. (╥﹏╥)"))
            else:
                # If no matching genre is found, notify the user
                await update.message.reply_text(telebot.translatedData("Error! Maybe your gender is not into the list. ( ˶°ㅁ°) !!\nPlease use the command /showgen to show the genders are available. (˶ᵔ ᵕ ᵔ˶)"))
    else:
        # If the user did not provide a genre name, prompt them to type a genre name
        if lang == None:
            response = "Type your anime (ෆ˙ᵕ˙ෆ)♡"
            await update.message.reply_text(response)
        else:
            telebot.getAbbreviation(str(lang))
            response = telebot.translatedData("Type the gender please (ෆ˙ᵕ˙ෆ)♡")
            await update.message.reply_text(response)

def main(TELEGRAM_TOKEN):
    """
    Main function to initialize and run the Telegram bot.

    Parameters:
    TELEGRAM_TOKEN (str): The token for the Telegram bot.
    """
    # Create an application instance with the provided Telegram token
    
    """
    application = Application.builder() 
        .token(str(TELEGRAM_TOKEN))   # Set the bot token
        .post_init(changeCommands)   # Set the post initialization hook to change commands
        .read_timeout(7)   # Set the read timeout to 7 seconds
        .get_updates_connect_timeout(42)   # Set the connect timeout for getting updates to 42 seconds
        .build()  # Build the application instance
    """
    application = Application.builder().token(str(TELEGRAM_TOKEN)).post_init(changeCommands).read_timeout(7).get_updates_connect_timeout(42).build()
    # Add command handlers to the application
    application.add_handler(CommandHandler("start",start))# Handle the /start command
    application.add_handler(CommandHandler("language", language))# Handle the /language command
    application.add_handler(CallbackQueryHandler(button, pattern='^lang_'))# Handle callback queries
    application.add_handler(CommandHandler("request",requestAnime))# Handle the /request command
    application.add_handler(CommandHandler("random",requestRandom))# Handle the /random command
    application.add_handler(CommandHandler("hoshii",requestgender))# Handle the /hoshii command
    application.add_handler(CallbackQueryHandler(buttonDownload,pattern='^(yes_option|no_option)$'))
    application.add_handler(CommandHandler("mangarand",requestRandomManga))
    application.add_handler(CommandHandler("mangarequest",requestManga))
    application.add_handler(CommandHandler("hoshiimanga",requestGenderManga))
    application.add_handler(CommandHandler("showgen",showGen)) #Handle the /showgen command
    application.add_handler(CommandHandler("help", help))# Handle the /help command
    application.add_handler(MessageHandler(filters.USER,handle_non_command_message))
    #Run the bot until the user presses Ctrl-C
    application.run_polling()