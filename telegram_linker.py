import requests # requests is still needed for send_to_discord
import json
from utils import find_telegram_links # Import from utils.py

def send_to_discord(webhook_url: str, links: list[str]):
    """
    Sends a list of Telegram links to a Discord webhook.

    Args:
        webhook_url: The Discord webhook URL.
        links: A list of Telegram links to send.
    """
    if not links:
        print("No links to send to Discord.")
        return

    for link in links:
        message = {"content": link}
        try:
            response = requests.post(webhook_url, json=message, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"Successfully sent {link} to Discord.")
        except requests.exceptions.RequestException as e:
            print(f"Error sending {link} to Discord: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while sending {link} to Discord: {e}")

if __name__ == "__main__":
    # Main script logic will be added in a later step
    print("Starting link search...")

    config_file = "config.json"
    discord_webhook_url = None
    sources_to_scrape = []

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            discord_webhook_url = config.get("discord_webhook_url")
            sources_to_scrape = config.get("sources_to_scrape")

        if not discord_webhook_url or not isinstance(discord_webhook_url, str):
            print(f"Error: 'discord_webhook_url' not found or invalid in {config_file}.")
            print("Please ensure it is a string.")
            discord_webhook_url = None # Ensure it's None if invalid

        if not sources_to_scrape or not isinstance(sources_to_scrape, list):
            print(f"Error: 'sources_to_scrape' not found or invalid in {config_file}.")
            print("Please ensure it is a list of URLs.")
            sources_to_scrape = [] # Ensure it's empty if invalid

    except FileNotFoundError:
        print(f"Error: {config_file} not found.")
        print(f"Please create {config_file} with 'discord_webhook_url' and 'sources_to_scrape'.")
        print("Example:")
        print("""
{
  "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL",
  "sources_to_scrape": [
    "https://example.com/page1",
    "https://another-example.com/links"
  ]
}
""")
    except json.JSONDecodeError:
        print(f"Error: Could not decode {config_file}. Please ensure it is valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred while reading {config_file}: {e}")


    if discord_webhook_url and sources_to_scrape:
        print(f"Found {len(sources_to_scrape)} source(s) to scrape.")
        telegram_links = find_telegram_links(sources_to_scrape)
        print(f"Found {len(telegram_links)} unique Telegram link(s).")

        if telegram_links:
            print("Sending links to Discord...")
            send_to_discord(discord_webhook_url, telegram_links)
            print("Finished sending links to Discord.")
        else:
            print("No Telegram links found to send.")
    elif not discord_webhook_url:
        print("Cannot proceed without a valid Discord webhook URL in the config.")
    elif not sources_to_scrape:
        print("Cannot proceed without a list of sources to scrape in the config.")


    print("Script finished.")
