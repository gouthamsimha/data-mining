import requests
from bs4 import BeautifulSoup
import csv
import time

def get_player_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # This selector needs to be adjusted based on the actual HTML structure
    players = soup.select('div.player-list a')
    return [(player.text, player['href']) for player in players]

def get_player_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # These selectors need to be adjusted based on the actual HTML structure
    name = soup.select_one('h1.player-name').text
    age = soup.select_one('span.player-age').text
    position = soup.select_one('span.player-position').text
    # Add more fields as needed
    return {
        'name': name,
        'age': age,
        'position': position,
        # Add more fields here
    }

def main():
    base_url = 'https://howstat.com/Cricket/Statistics/IPL/MatchList.asp'  # Replace with the actual website URL
    player_list_url = f'{base_url}/players'

    players = get_player_list(player_list_url)

    with open('player_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'age', 'position']  # Add more fields as needed
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player_name, player_url in players:
            full_url = base_url + player_url
            player_data = get_player_details(full_url)
            writer.writerow(player_data)
            time.sleep(1)  # Be polite, don't overwhelm the server

if __name__ == "__main__":
    main()