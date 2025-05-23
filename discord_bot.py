import discord
from discord.ext import commands, tasks # Import tasks
import json
from utils import find_telegram_links # Import from utils.py

# Define bot instance
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    """
    Event handler for when the bot has successfully connected to Discord.
    """
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('Bot is ready to receive commands.')
    print('------')
    if not scheduled_scan_sources_task.is_running():
        print("Starting scheduled scan task...")
        scheduled_scan_sources_task.start()

# Configuration file path
CONFIG_FILE = "config.json"

@bot.command(name='add_source')
async def add_source(ctx, url: str):
    """Adds a new URL to the list of sources to scrape."""
    try:
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file not found or corrupted, create a default structure
            config = {"discord_webhook_url": None, "sources_to_scrape": [], "discord_bot_token": None, "output_channel_id": None}
            print(f"Warning: {CONFIG_FILE} was not found or was invalid. A new default config structure will be used.")


        if "sources_to_scrape" not in config or not isinstance(config["sources_to_scrape"], list):
            config["sources_to_scrape"] = []
            print(f"Warning: 'sources_to_scrape' was missing or invalid in {CONFIG_FILE}. Initialized as empty list.")

        if url not in config["sources_to_scrape"]:
            config["sources_to_scrape"].append(url)
            try:
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
                await ctx.send(f"Added `{url}` to sources.")
                print(f"Added {url} to sources in {CONFIG_FILE}")
            except IOError as e:
                await ctx.send(f"Error: Could not write to {CONFIG_FILE}. Details: {e}")
                print(f"Error writing to {CONFIG_FILE}: {e}")
        else:
            await ctx.send(f"`{url}` is already in the list of sources.")

    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
        print(f"Unexpected error in add_source: {e}")

@bot.command(name='remove_source')
async def remove_source(ctx, url: str):
    """Removes a URL from the list of sources to scrape."""
    try:
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            await ctx.send(f"Error: {CONFIG_FILE} not found or is invalid. Cannot remove source.")
            print(f"Error: {CONFIG_FILE} not found or invalid in remove_source.")
            return

        if "sources_to_scrape" not in config or not isinstance(config["sources_to_scrape"], list) or not config["sources_to_scrape"]:
            await ctx.send("There are no sources to remove.")
            return

        if url in config["sources_to_scrape"]:
            config["sources_to_scrape"].remove(url)
            try:
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
                await ctx.send(f"Removed `{url}` from sources.")
                print(f"Removed {url} from sources in {CONFIG_FILE}")
            except IOError as e:
                await ctx.send(f"Error: Could not write to {CONFIG_FILE}. Details: {e}")
                print(f"Error writing to {CONFIG_FILE}: {e}")
        else:
            await ctx.send(f"`{url}` not found in the list of sources.")

    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
        print(f"Unexpected error in remove_source: {e}")

@bot.command(name='list_sources')
async def list_sources(ctx):
    """Lists all URLs currently in the sources_to_scrape list."""
    try:
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            await ctx.send(f"Error: {CONFIG_FILE} not found or is invalid. Cannot list sources.")
            print(f"Error: {CONFIG_FILE} not found or invalid in list_sources.")
            return

        sources = config.get("sources_to_scrape")
        if sources and isinstance(sources, list):
            if not sources:
                await ctx.send("There are no sources currently configured.")
            else:
                message = "Current sources to scrape:\n```\n"
                for idx, source_url in enumerate(sources):
                    message += f"{idx + 1}. {source_url}\n"
                message += "```"
                await ctx.send(message)
        else:
            await ctx.send(f"'sources_to_scrape' is missing or invalid in {CONFIG_FILE}. Please add some sources first.")
            print(f"Warning: 'sources_to_scrape' missing or invalid in list_sources from {CONFIG_FILE}.")

    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
        print(f"Unexpected error in list_sources: {e}")

@bot.command(name='scan_sources')
async def scan_sources(ctx):
    """Scans all sources and sends found Telegram links to the configured output channel."""
    try:
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            await ctx.send(f"Error: {CONFIG_FILE} not found or is invalid. Cannot scan sources.")
            print(f"Error: {CONFIG_FILE} not found or invalid in scan_sources.")
            return

        sources = config.get("sources_to_scrape")
        output_channel_id_str = config.get("output_channel_id")

        if not sources or not isinstance(sources, list) or not len(sources):
            await ctx.send("There are no sources configured to scan. Add some with `!add_source <url>`.")
            return

        if not output_channel_id_str:
            await ctx.send(f"Error: `output_channel_id` is not configured in {CONFIG_FILE}. Use `!set_channel` to set it.")
            print(f"Error: output_channel_id missing from {CONFIG_FILE} in scan_sources.")
            return
        
        try:
            output_channel_id = int(output_channel_id_str)
        except ValueError:
            await ctx.send(f"Error: `output_channel_id` ('{output_channel_id_str}') in {CONFIG_FILE} is not a valid channel ID.")
            print(f"Error: output_channel_id ('{output_channel_id_str}') is not a valid integer.")
            return

        output_channel = bot.get_channel(output_channel_id)
        if not output_channel:
            await ctx.send(f"Error: Could not find the output channel with ID `{output_channel_id}`. Please check the ID and ensure the bot has access to it.")
            print(f"Error: Output channel with ID {output_channel_id} not found or bot lacks access.")
            return

        await ctx.send(f"Starting scan of {len(sources)} source(s)... This may take a moment.")
        
        # In a real scenario, find_telegram_links might block for a while.
        # For very long scans, consider running in an executor:
        # loop = asyncio.get_event_loop()
        # telegram_links = await loop.run_in_executor(None, find_telegram_links, sources)
        print(f"Scanning sources: {sources}")
        telegram_links = find_telegram_links(sources) # This is a blocking call
        print(f"Found links: {telegram_links}")

        if telegram_links:
            await ctx.send(f"Scan complete. Found {len(telegram_links)} Telegram link(s). Sending to {output_channel.mention}...")
            for link in telegram_links:
                try:
                    await output_channel.send(link)
                except discord.errors.Forbidden:
                    await ctx.send(f"Error: Bot does not have permission to send messages in {output_channel.mention}. Please check channel permissions.")
                    print(f"Error: Forbidden to send messages in channel {output_channel_id}")
                    # Stop sending further links if permission is denied for one.
                    return 
                except Exception as e:
                    await ctx.send(f"Error sending link `{link}` to {output_channel.mention}: {e}")
                    print(f"Error sending link {link} to channel {output_channel_id}: {e}")
            await ctx.send(f"Finished sending {len(telegram_links)} link(s) to {output_channel.mention}.")
        else:
            await ctx.send("Scan complete. No new Telegram links found.")

    except Exception as e:
        await ctx.send(f"An unexpected error occurred during the scan: {e}")
        print(f"Unexpected error in scan_sources: {e}")

# Scheduled task to automatically scan sources
# For production, it's recommended to change to hours=24
@tasks.loop(minutes=5)  # SET TO hours=24 for production
async def scheduled_scan_sources_task():
    """Periodically scans sources and sends found Telegram links to the configured output channel."""
    print("Scheduled scan running...")
    try:
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            print(f"Error (Scheduled Scan): {CONFIG_FILE} not found. Skipping scan.")
            return
        except json.JSONDecodeError:
            print(f"Error (Scheduled Scan): Could not decode {CONFIG_FILE}. Skipping scan.")
            return

        sources = config.get("sources_to_scrape")
        output_channel_id_str = config.get("output_channel_id")

        if not sources or not isinstance(sources, list) or not len(sources):
            print("Info (Scheduled Scan): No sources configured to scan. Skipping.")
            return

        if not output_channel_id_str:
            print(f"Error (Scheduled Scan): `output_channel_id` is not configured in {CONFIG_FILE}. Skipping scan.")
            return
        
        try:
            output_channel_id = int(output_channel_id_str)
        except ValueError:
            print(f"Error (Scheduled Scan): `output_channel_id` ('{output_channel_id_str}') in {CONFIG_FILE} is not a valid channel ID. Skipping.")
            return

        output_channel = bot.get_channel(output_channel_id)
        if not output_channel:
            print(f"Error (Scheduled Scan): Could not find the output channel with ID `{output_channel_id}`. Skipping scan.")
            return
        
        print(f"Info (Scheduled Scan): Scanning {len(sources)} source(s)...")
        # In a real scenario, find_telegram_links might block for a while.
        # For very long scans, consider running in an executor:
        # loop = asyncio.get_event_loop()
        # telegram_links = await loop.run_in_executor(None, find_telegram_links, sources)
        telegram_links = find_telegram_links(sources) # This is a blocking call

        if telegram_links:
            print(f"Info (Scheduled Scan): Found {len(telegram_links)} Telegram link(s). Sending to channel ID {output_channel_id}.")
            for link in telegram_links:
                try:
                    await output_channel.send(link)
                except discord.errors.Forbidden:
                    print(f"Error (Scheduled Scan): Bot does not have permission to send messages in channel {output_channel_id}. Skipping further messages for this scan.")
                    return 
                except Exception as e:
                    print(f"Error (Scheduled Scan): Could not send link `{link}` to channel {output_channel_id}: {e}")
            print(f"Info (Scheduled Scan): Finished sending {len(telegram_links)} link(s).")
        else:
            print("Info (Scheduled Scan): No new Telegram links found.")

    except Exception as e:
        print(f"An unexpected error occurred during the scheduled scan: {e}")

@scheduled_scan_sources_task.before_loop
async def before_scheduled_scan():
    """Ensures the bot is ready before the scheduled task starts."""
    print("Preparing for scheduled scan... waiting for bot to be ready.")
    await bot.wait_until_ready()
    print("Bot is ready. Scheduled scan will start on its defined interval.")


if __name__ == "__main__":
    config_file = CONFIG_FILE # Use the global constant
    discord_bot_token = None

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            discord_bot_token = config.get("discord_bot_token")

        if not discord_bot_token:
            print(f"Error: 'discord_bot_token' not found in {config_file}.")
            print(f"Please add your bot token to {config_file} like this:")
            print("""
{
  "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
  "sources_to_scrape": [
    "https://example.com/page_with_telegram_links1",
    "https://another-example.org/some_other_page"
  ],
  "discord_bot_token": "YOUR_ACTUAL_BOT_TOKEN_HERE" 
}
""")
        else:
            print("Discord bot token loaded. Starting bot...")
            bot.run(discord_bot_token)

    except FileNotFoundError:
        print(f"Error: {config_file} not found.")
        print(f"Please ensure {config_file} exists and contains 'discord_bot_token'.")
        print("Example content for config.json if it's missing:")
        print("""
{
  "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
  "sources_to_scrape": [
    "https://example.com/page_with_telegram_links1",
    "https://another-example.org/some_other_page"
  ],
  "discord_bot_token": "YOUR_ACTUAL_BOT_TOKEN_HERE" 
}
""")
    except json.JSONDecodeError:
        print(f"Error: Could not decode {config_file}. Please ensure it is valid JSON.")
    except discord.errors.LoginFailure:
        print("Error: Login failed. Please check if the 'discord_bot_token' is correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
