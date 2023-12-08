import re
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import sys
import json

def extract_sectors_numbers_from_html(span_elements):
    numbers = []

    for tag in span_elements:
        # Extract numbers using regular expression
        number = re.findall(r'\d[\d,]*', tag.text)
        if number:
            numbers.append(number[0].replace(',', ''))  # Remove commas for pure numerical value

    return numbers

def parseHTML(selected_tag):
    return selected_tag.text.strip().split()[0]

def scrape_miner_data(url):
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
        try:
            response = session.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Connection refused")
        response.raise_for_status()  # Raise an error for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        # Example of extracting specific data - this will need to be customized
        adjusted_power = parseHTML(soup.select('div.flex.items-center.justify-between.w-full>p.font-medium.text-2xl')[0])
        win_count = soup.find('div', class_='text-sm items-center justify-end flex').text.strip().split()[-1]
        sectors = extract_sectors_numbers_from_html(soup.select('div.text-sm.mt-2.items-center.justify-between.flex > div span'))

        return {
            'Address': url.split('/')[-1],
            'AdjustedPower': adjusted_power,
            'WinCount': win_count,
            'SectorTotal': sectors[0],
            'SectorActive': sectors[1],
            'SectorFaults': sectors[2],
            'SectorRecoveries': sectors[3]
        }
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
def write_json_to_file(json_object, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(json_object, file, indent=4)
        print(f"JSON data successfully written to {file_path}")
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")
    
def main(input_address):
    miner_url = f'https://filfox.info/en/address/{input_address}'
    print("miner url", miner_url)
    print("input_address", input_address)

    new_miner = scrape_miner_data(miner_url)
    write_json_to_file(json_object=new_miner, file_path="newminer.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Must pass arguments. Format: [command] input_address")
        sys.exit()

    main(sys.argv[1])