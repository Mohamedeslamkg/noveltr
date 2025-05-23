# Telegram Link Finder & Discord Notifier

A Python script to find Telegram channel links from specified web sources and send them to a Discord webhook. This project also includes an optional Discord bot that can manage sources and automatically scan for Telegram links.

## Features

- Scrapes websites for Telegram links (`t.me/...`).
- **Standalone Script**: Sends found links to a Discord webhook (via `telegram_linker.py`).
- **Discord Bot**:
    - Manages a list of source URLs via commands.
    - Manually trigger scans via a command.
    - Automatically scans sources periodically.
    - Posts found links to a designated Discord channel.
- Configurable via a `config.json` file.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd <YOUR_REPOSITORY_DIRECTORY>
    ```
    (Replace `<YOUR_REPOSITORY_URL>` and `<YOUR_REPOSITORY_DIRECTORY>` with the actual URL and directory name of this repository.)

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt 
    ```
    (Note: `requirements.txt` includes `discord.py` for the bot and `requests` for both script and bot.)

3.  **Configure the project (`config.json`):**
    - Open `config.json` (located in the root of the project) and replace the placeholder values. This file is used by both the standalone script and the Discord bot.
    Example `config.json`:
    ```json
    {
      "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE_FOR_SCRIPT",
      "sources_to_scrape": [
        "https://example.com/page_with_telegram_links1",
        "https://another-example.org/some_other_page"
      ],
      "discord_bot_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
      "output_channel_id": "YOUR_DISCORD_CHANNEL_ID_FOR_BOT_MESSAGES_HERE"
    }
    ```
    -   `"discord_webhook_url"`: Your actual Discord webhook URL (used by `telegram_linker.py`).
    -   `"sources_to_scrape"`: A list of URLs where the script/bot should look for Telegram links.
    -   `"discord_bot_token"`: Your Discord Bot Token (see Discord Bot Setup below).
    -   `"output_channel_id"`: The ID of the Discord channel where the bot will post found links (see Discord Bot Setup below).

## Standalone Script Usage (`telegram_linker.py`)

If you only want to use the simple script to find links and send them to a webhook (without bot commands or scheduled scans):

1.  Ensure `discord_webhook_url` and `sources_to_scrape` are correctly set in `config.json`.
2.  Run the script:
    ```bash
    python telegram_linker.py
    ```
    The script will output its progress to the console.

## Discord Bot Functionality

The Discord bot provides more advanced features like source management, manual scans, and automated periodic scans.

### Discord Bot Setup

1.  **Create a Discord Application & Bot:**
    *   Go to the [Discord Developer Portal](https://discord.com/developers/applications).
    *   Click "New Application". Give it a name (e.g., "Telegram Link Scanner") and click "Create".
    *   Navigate to the "Bot" tab on the left menu.
    *   Click "Add Bot" and confirm by clicking "Yes, do it!".
    *   Under the bot's username, you'll see a "TOKEN" section. Click "Reset Token" (if it's your first time, it might say "View Token" or you might just see the token). Copy this token. This is your **Bot Token**.
        *   **Important**: Keep this token secret! Do not share it publicly.
    *   Paste this token into the `"discord_bot_token"` field in your `config.json` file.
    *   Under "Privileged Gateway Intents", enable:
        *   **Server Members Intent**: Might be useful for future features or more complex command handling.
        *   **Message Content Intent**: This is necessary for the bot to read messages and process commands (like `!add_source`).

2.  **Get Bot Invite Link:**
    *   In the Discord Developer Portal, navigate to "OAuth2" -> "URL Generator".
    *   Under "SCOPES", select `bot`.
    *   Under "BOT PERMISSIONS", select the following:
        *   `Send Messages` (to send links and command responses)
        *   `Read Message History` (might be needed for some command interactions or future features)
    *   Copy the "GENERATED URL".

3.  **Invite the Bot to Your Server:**
    *   Paste the generated URL into your web browser.
    *   Select the Discord server you want to add the bot to from the dropdown menu.
    *   Click "Continue" and then "Authorize". Complete any CAPTCHA if prompted.

4.  **Get Output Channel ID:**
    *   The bot needs to know which channel to send the found Telegram links to. You need to provide its ID in `config.json` under `"output_channel_id"`.
    *   To get a channel ID:
        *   In Discord, go to User Settings (the gear icon near your username).
        *   Go to App Settings -> Advanced.
        *   Enable "Developer Mode".
        *   Close User Settings.
        *   Right-click on the text channel where you want the bot to post messages (e.g., `#telegram-links`) and select "Copy ID".
        *   Paste this ID into the `"output_channel_id"` field in `config.json`.

### Running the Bot

Once `config.json` is updated with your `discord_bot_token` and `output_channel_id`:

```bash
python discord_bot.py
```
The console will show messages indicating the bot has logged in and is ready.

### Bot Commands

-   `!add_source <url>`: Adds a new URL to the list of sources for scanning.
    Example: `!add_source https://some.site/with/telegram/links`
-   `!remove_source <url>`: Removes a URL from the list.
    Example: `!remove_source https://some.site/with/telegram/links`
-   `!list_sources`: Shows all current URLs being scanned.
-   `!scan_sources`: Manually triggers a scan of all sources. Links will be posted to the channel specified by `output_channel_id`.

### Scheduled Scans

The bot is configured to automatically scan all sources periodically.
*   In the current code (`discord_bot.py`), this interval is set to every **5 minutes** for testing purposes.
*   For production use, you should change `@tasks.loop(minutes=5)` to a longer interval, such as `@tasks.loop(hours=24)` for daily scans.
Found links from these automatic scans are posted to the channel specified by `output_channel_id`.

## Core Logic (`utils.py`)

Both the standalone script and the Discord bot use the `find_telegram_links` function located in `utils.py`. This function is responsible for fetching web content and extracting Telegram links using regular expressions.

## Dependencies

- Python 3.x
- `requests`: For making HTTP requests (used by `utils.py`).
- `discord.py`: For the Discord bot functionality.

(These are listed in `requirements.txt`)

---
