import requests
from bs4 import BeautifulSoup
import json
import re
import time

url2 = "https://seo-fast.ru/site_youtube/ajax/ajax_youtube_nobd.php"
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Chromium\";v=\"118\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "https://seo-fast.ru/work_youtube",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}


def running(account_number):
    # URL to fetch
    url = "https://seo-fast.ru/login"

    # Load cookies from file
    with open(f'account_{account_number}.json', 'r') as f:
        cookies_data = json.load(f)

    # Check if cookies_data is a list or dict, and convert it to a dictionary if necessary
    if isinstance(cookies_data, list):
        cookies = {cookie['name']: cookie['value'] for cookie in cookies_data}
    elif isinstance(cookies_data, dict):
        cookies = cookies_data
    else:
        print("Cookies data is not in the expected format")
        return

    # Send a GET request to the login page with cookies
    response = requests.get(url, cookies=cookies)
    if response.status_code != 200:
        print("Failed to retrieve login page.")
        return






    # Fetch the work_youtube page
    work_youtube_url = "https://seo-fast.ru/work_youtube?youtube_time"
    response = requests.get(work_youtube_url, cookies=cookies)
    if response.status_code != 200:
        print("Failed to retrieve work_youtube page.")
        return

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> elements with 'onclick' containing "start_youtube_view"
    links = soup.find_all('a', onclick=lambda value: value and "start_youtube_view" in value)

    # Extract IDs from the 'onclick' attribute
    ids = []
    for link in links:
        onclick_value = link['onclick']
        start = onclick_value.find("start_youtube_view('") + len("start_youtube_view('")
        end = onclick_value.find("')", start)
        extracted_id = onclick_value[start:end]
        ids.append(extracted_id)

    print("Extracted IDs:", ids)



    # List to store extracted data
    all_data = []

    # Process each extracted ID
    count = 0
    for extracted_id in ids:
        if count >= 10:  # Process only 10 items
            break

        payload = {
            "sf": "start_youtube_view_y",
            "id": extracted_id
        }

        time.sleep(0.2)
        response = requests.post(url2, headers=headers, data=payload, cookies=cookies)
        print(f"Response Text: {response.text}")
        response_data = json.loads(response.text)

        url1 = response_data.get("url")

        # Remove the prefix "https://noref.site/#" from the URL
        if url1 and url1.startswith("https://noref.site/#"):
            url1 = url1[len("https://noref.site/#"):]
            print(url1)
            data_to_save = {"url": url1}
            all_data.append(data_to_save)

        count += 1

    # Save the extracted data to a file
    with open("urls.txt", "w") as f:
        json.dump(all_data, f, indent=4)

    print("All data saved to 'urls.txt'.")


# Run the function for account 3
running("3")
