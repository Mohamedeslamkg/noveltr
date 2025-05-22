# Telegram Link Finder & Discord Notifier

A Python script to find Telegram channel links from specified web sources and send them to a Discord webhook.

## Features

- Scrapes websites for Telegram links (`t.me/...`).
- Sends found links to a Discord webhook.
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
3.  **Configure the script:**
    - Open `config.json` (located in the root of the project) and replace the placeholder values:
        - `"discord_webhook_url"`: Your actual Discord webhook URL.
        - `"sources_to_scrape"`: A list of URLs where the script should look for Telegram links.
    Example `config.json`:
    ```json
    {
      "discord_webhook_url": "https://discord.com/api/webhooks/your/webhook_id_and_token",
      "sources_to_scrape": [
        "https://example.com/some-page-with-links",
        "https://another-site.org/relevant-page"
      ]
    }
    ```

## Usage

Once configured, run the script from the root directory of the project:

```bash
python telegram_linker.py
```

The script will output its progress to the console, including any links found and whether they were successfully sent to Discord.

## Dependencies

- Python 3.x
- `requests`: For making HTTP requests. (Listed in `requirements.txt`)

## How it Works

The script fetches the content of each URL specified in `sources_to_scrape` from the `config.json` file. It then uses regular expressions to identify potential Telegram channel links. Unique links found are then sent as individual messages to the Discord webhook URL also specified in `config.json`.

---
