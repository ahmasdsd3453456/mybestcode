import asyncio
import json
from playwright.async_api import async_playwright
import time
import os

# Function to handle a single video
async def play_video(context, url, timer):
    page = await context.new_page()
    print(f"Opening URL: {url}")
    await page.goto(url)

    try:
        # Wait for the iframe to load
        await page.wait_for_selector('iframe#video-start')

        # Access the iframe
        iframe = page.frame_locator('iframe#video-start')

        # Wait for the YouTube play button to appear within the iframe
        await iframe.locator('button.ytp-large-play-button').wait_for()

        # Switch to the tab (bring it to the front)
        print(f"Switching to tab for URL: {url}")
        await page.bring_to_front()  # Bring the page to the front

        # Click on the play button within the iframe
        print(f"Playing video for URL: {url}")
        await iframe.locator('button.ytp-large-play-button').click()

        

        # Wait for the duration specified in the timer
        await asyncio.sleep(timer)
        print(f"Completed playback for URL: {url}")

    except Exception as e:
        print(f"Error handling URL {url}: {e}")

    finally:
        await page.close()

# Function to handle videos dynamically
async def handle_videos(urls):
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Queue to track active tasks
        tasks = set()

        for url_data in urls:
            # Extract URL and timer value from the JSON
            url = url_data["url"]
            timer = int(url.split("timer=")[1].split("&")[0]) + 5  # Extract timer value
            if timer > 300:
                print(f"Ignoring URL {url} as timer is greater than 300.")
                continue
            # Schedule a new task and add to the set
            task = asyncio.create_task(play_video(context, url, timer))
            tasks.add(task)

            # Wait for any task to complete if the limit (3) is reached
            if len(tasks) >= 6:
                # Wait for at least one task to complete
                done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                print(f"Task completed. Remaining tasks: {len(tasks)}")

        # Wait for remaining tasks to complete
        if tasks:
            await asyncio.gather(*tasks)

        # Close the browser
        await browser.close()

# Main function to read URLs and start the process
async def main():
    # Load the URLs from a JSON file
    with open("urls.txt", "r") as file:
        urls = json.load(file)

    print("Starting video playback for URLs...")
    await handle_videos(urls)
    print("Completed video playback for all URLs.")
    os.remove("./urls.txt")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
