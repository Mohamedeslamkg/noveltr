import re
import requests

# NOTE: The temporary mock for requests.get and debug prints have been removed.

def find_telegram_links(sources: list[str]) -> list[str]:
    """
    Finds Telegram channel links from a list of URLs.

    Args:
        sources: A list of URLs to scrape.

    Returns:
        A list of unique Telegram links found.
    """
    telegram_links = set()
    # Regex to find t.me or telegram.me links. It will capture the channel name.
    # It looks for http(s)://t.me/channel_name or http(s)://telegram.me/channel_name
    # It also handles links that might just be t.me/channel_name without http(s)
    link_pattern = re.compile(r"(?:https?://)?(?:t\.me|telegram\.me)/([a-zA-Z0-9_]+)")

    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            content = response.text
            found_links = link_pattern.findall(content)
            for channel_name in found_links:
                telegram_links.add(f"t.me/{channel_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {url}: {e}")
    return list(telegram_links)
