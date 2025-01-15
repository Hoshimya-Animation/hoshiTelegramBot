<p align="center">
  <img src="img/logo_draf.png" alt="Kawaii Bot" width="200px"/>
</p>

<h1 align="center">🌸 hoshiiTelegramBot 🌸</h1>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.2.1-brightgreen" alt="Version" />
  <img src="https://img.shields.io/badge/license-AGPL3.0-blue?style=flat&color=blue" alt="License" />
  <img src="https://img.shields.io/badge/test-passed-pass?style=flat&color=red" alt="Build" />
</p>

Welcome to the **hoshiiTelegramBot**! This adorable Telegram bot fetches anime and manga details from various APIs, including Jikan API and Google. It supports multiple languages and provides personalized! 🌟

## 🌟 Features

- Fetches detailed information about anime and manga from Jikan API and YouTube.
- Supports multiple languages for a global audience.
- Cute and user-friendly interface for the best experience.
- Download your favourite opening and ending from Anime (Not apply for Hentai or Erotica Animes).
- Anime/Manga reconmendations.
- Protect to child's. We block continent +18 if you are under-age. This will change until the age is 18 from your register.
- WE DON'T STORE YOUR PERSONAL INFO (Only we get your ID of Telegram and the age with the date). All songs are store into a temporal directory until upload to Telegram.


## 🛠️ Installation

> [!TIP]
> Use a virtual environment. Don't know how to create one? Let me show you how to create it. 👉 Click here **[documentation](https://docs.python.org/3/library/venv.html)**.

> [!NOTE]
> Previously, you should have created your Telegram Bot. Please, If you don't do it yet, check the official **[documentation](https://core.telegram.org/bots#how-do-i-create-a-bot)** 🤖.


1. Create and activate your virtual environment.
  ```bash
    source /.../my-env/bin/activate
  ```
2. Inside of your virtual enviroment, clone the repository:
    ```bash
    git clone https://github.com/Hoshimya-Animation/hoshiTelegramBot
    ```
    ```bash
    cd hoshiTelegramBot/
    ```

3. Install the required dependencies:
    ```bash
    pip3 install -r requirements.txt --no-deps
    ```
> [!NOTE]
> If you run ```main.py``` the interpreter shows you this message ```AttributeError: module 'httpcore' has no attribute 'SyncHTTPTransport```

> [!IMPORTANT]
> Googletrans has an important issue nowadays. HTTPX package version  for Googletrans is 0.13.0, on other hand, Python-Telegram-Bot requires the version 0.27.0. Therefore there is a problem. However, you can fix temporaly this issue. 
    
- In a new terminal use this command

    ```bash
    pip list -v
    ```

> [!NOTE]
> This command shows you all packages installed with pip.

- Then, search for the package *googletrans*🔤, go to the path where it's installed, and **ONLY MODIFY** ⚠️ the file ***client.py***. In this file, on line 62, you can comment it out and below it, type this:

    ```python
    proxies: typing.Dict[str, httpcore.AsyncHTTPProxy] = None,
    ```
- Finally, save the document. 📄

4. Open the file **main.py** and replace your Telegram Token of your Bot on ```TELEGRM_TOKEN```, i.e. ```"123+2"``` .


5. Run the bot: 🤖
    ```bash
    python3 main.py
    ```

## 🌐 Usage

Add the bot to your Telegram and start chatting with it! Use the following commands to get started:

- `/start` - The bot starts ₍^ >ヮ<^₎ .ᐟ. kawaii journey!
- `/language`- Change language of the Bot 🇪🇸 ➡️ 🇬🇧 (Available in Spanish, English, French, Italian, Traditional Chinese, Japanese, Hindi, German, Arabic, Romanian, and Korean)
- `/request [name]` - Request information about an anime from MyAnimeList 🗄🔎📺 (japanese or english).
- `/mangarequest [name]` - Request information about a manga from MyAnimeList 🗄🔎📖 (japanese or english).
- `/random` - Random information about an anime 🎲
- `/mangarand` - Random information about a manga 🎲📖
- `/hoshiimanga [gender]` - Manga suggestion by gender 🍱📖.
- `/showgen` - Show all available genders 🍘🎎.
- `/hoshii [gender]` - Anime suggestion by the gender 🌍🍱 .
- `/help` - Give you information about my functions 🆘❔.



## 📜 License

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for more details.

## 🙌 Contributing

We welcome contributions from the community! Please read the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## 💖 Acknowledgements

A big thank you to the developers of the Jikan API and Google for providing the data that makes this bot possible.

## 📬 Contact

If you have any questions or suggestions, feel free to open an issue or reach out to us at [hoshimiyanimation.contact@protonmail.com](mailto:hoshimiyanimation.contact@protonmail.com.).

<p align="center">
  <img src="img/logo_draf2.png" alt="Kawaii Bot2""/>
</p>

<p align="center">
  Made with 💖 by <a href="https://github.com/Hoshimya-Animation">Hoshimya Animation</a>, <a href="https://github.com/JohnKun136NVCP">John </a>
</p>
