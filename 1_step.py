import requests
import json
from bs4 import BeautifulSoup

# Load cookies from the cookie.json file
with open('account_3.json', 'r') as f:
    cookies_data = json.load(f)

# Ensure cookies are in the correct format (convert to a dictionary if needed)
if isinstance(cookies_data, list):
    cookies = {cookie['name']: cookie['value'] for cookie in cookies_data}
elif isinstance(cookies_data, dict):
    cookies = cookies_data
else:
    print("Cookies data is not in the expected format")
    exit()

# Define the URL and headers
url = "https://seo-fast.ru/infoall.php"
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
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# Define the body for the POST request
payload = {
    "i_see_y": "ok"
}

# Send the POST request with the headers, cookies, and payload
response = requests.post(url, headers=headers, data=payload, cookies=cookies)



soup = BeautifulSoup(response.text, 'html.parser')

# Find all div elements with ids containing the video IDs
video_divs = soup.find_all('div', id=True)


for div in video_divs:
    div_id = div.get('id', '')
    # Check if the 'id' attribute contains 'id_i_see_y' and extract the numeric part 
    video_id = div_id.replace('id_i_see_y', '') 
    print(video_id) 
    url2 = "https://seo-fast.ru/ajax/ajax_rest_sf.php"
    data1 = {
    "sf": "del_i_see_y",
    "id": video_id
    }
    # Send POST request with cookies loaded from cookie.json
    response = requests.post(url2, headers=headers, data=data1, cookies=cookies)
    # Print the response text (or handle it as needed)
    print(response.text)

print("successfully deleted..")
