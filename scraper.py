from __future__ import division
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import random



def get_script(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')
    script_list = soup.find_all('script')
    selected_script = script_list[9]
    return selected_script

def find_song_links(url):
    selected_script = get_script(url)
    links_list = re.findall('(?<=tab_url":")(.*?)(?=",)', str(selected_script))
    links_list = [link.replace("\\", "") for link in links_list]
    return links_list

def find_artist_links(url):
    retry_count = 0
    links_list = []
    while(not links_list and retry_count <= 5):
        try:
            selected_script = get_script(url)
            links_list = re.findall('(?<=},"artist_url":")(.*?)(?=",)', str(selected_script))
            links_list = [link.replace("\\", "") for link in links_list]
            chord_filter = "?filter=chords"
            links_list = [link + chord_filter for link in links_list]
        except:
            print("Error finding artist links, retrying...")
            time.sleep(random.uniform(3, 6))
            retry_count += 1
    return set(links_list)

def save_to_json(path, data):
    js = json.dumps(data)
    fp = open(path, 'a')
    fp.write(js)
    fp.close()

def open_file(path):
    json1_file = open(path)
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    return json1_data

def song_scraper(url):
    selected_script = get_script(url)
    chord_list = re.findall('(?<=\[ch\])(.*?)(?=\[\\\/ch\])', str(selected_script))
    chord_list = [chord.replace("\\", "") for chord in chord_list]
    bulk_info = re.search('(?<=,"tab":{)(.*?)(?=,"date_update":")', str(selected_script)).group()
    song_dict = json.loads("{"+bulk_info+"}")
    song_dict["chord_progression"] = chord_list
    return song_dict

def artist_find_next_pages(url):
    selected_script = get_script(url)
    links_list = re.findall('(?<="pages":)(.*?)(?=,"sorting")', str(selected_script))
    # retry
    if not links_list:
        tries = 0
        while(not links_list and tries <= 4):
            print("Retrying to find links to other pages at:", url)
            time.sleep(5)
            selected_script = get_script(url)
            links_list = re.findall('(?<="pages":)(.*?)(?=,"sorting")', str(selected_script))
            tries += 1
    if links_list:
        print("Successfully found links!")
        page_dict = json.loads('{"pagination":' + links_list[0])
        #print(page_dict)
        base_url = "https://www.ultimate-guitar.com"
        page_links = [base_url + x["url"]for x in page_dict["pagination"]]
        return page_links
    else:
        return []

def find_next_pages(url):
    selected_script = get_script(url)
    pagination = re.findall('(?<="data":)(.*?)(?=,"totalResults")', str(selected_script))
    # retry
    if not pagination:
        tries = 0
        while(not pagination and tries <= 4):
            print("Retrying to find links to other pages at:", url)
            time.sleep(5)
            selected_script = get_script(url)
            pagination = re.findall('(?<="data":)(.*?)(?=,"totalResults")', str(selected_script))
            tries += 1
    if pagination:
        page_dict = json.loads(pagination[0] + "}")
        max_pages = page_dict["pagination"]["pages"] + 1
        base_url = url[:-14]
        chord_filter = "&type[]=Chords"
        links_list = [base_url + "&page=" + str(i) + chord_filter for i in range(1, max_pages)]
        return links_list
    else:
        return []

#print(find_next_pages("https://www.ultimate-guitar.com/explore?genres[]=4&type[]=Chords"))

#print(artist_find_next_pages("https://www.ultimate-guitar.com/artist/elvis_presley_11125?filter=chords"))


def crawler(url, path, filename):
    artist_visited_dictionary = {}
    song_urls = []
    print("Scanning for pages of links...", url)
    # find links to each page of artists:
    total_page_links = find_next_pages(url)
    for page_link in total_page_links:
        print("Finding artist links...", page_link)
        time.sleep(random.uniform(2.5, 4.3))
        artist_links = find_artist_links(page_link)
        for artist_link in artist_links:
            if(artist_link not in artist_visited_dictionary):
                artist_visited_dictionary[artist_link] = True
                time.sleep(random.uniform(2, 7))
                print("Finding pages for artist at:", artist_link)
                artist_pages = artist_find_next_pages(artist_link)
                for artist_page in artist_pages:
                    print("Adding songs to queue at:", artist_page)
                    time.sleep(5)
                    song_urls = song_urls + find_song_links(artist_page)

    print("----------------Finished Scanning Pages----------------")
    print("---------------Scraping Individual Songs---------------")
    num_songs = len(song_urls)
    print("Number of Found Songs:", num_songs)
    json_output = []
    song_count = 0
    save_count = 0
    for song in song_urls:
        try:
            print("Scraping at...", song)
            time.sleep(random.uniform(1.5, 2.1))
            song_output = song_scraper(song)
            print("Successfully scraped:", song_output["song_name"])
            json_output.append(song_output)
            song_count += 1
            per_complete = 100*song_count / num_songs
            if song_count % 10 == 0:
                print("-----------------Songs Saved:", song_count, "-----------------")
                print("------------", per_complete, "% complete------------")
            if song_count % 50 == 0:
                new_file = path + filename + str(save_count + 1) + ".json"
                print("Saving file now to", new_file)
                save_to_json(new_file, json_output)
                save_count += 1
                json_output = []
        except:
            print("Error: Failed Scraping at", url)
    new_file = path + filename + str(save_count + 1) + ".json"
    print("Saving file now to", new_file)
    save_to_json(new_file, json_output)
    print("----------------Scraping Complete!-----------------------")
    return


#output = crawler("https://www.ultimate-guitar.com/explore?decade[]=1950&genres[]=4&order=hitstotal_desc&type[]=Chords")
path = 'f:/WebCrawlers/RockMusic/2010Rock/'
filename = '2010batch'

crawler("https://www.ultimate-guitar.com/explore?decade[]=2010&genres[]=4&type[]=Chords", path, filename)







#print(find_artist_links("https://www.ultimate-guitar.com/explore?decade[]=1950&genres[]=4&order=hitstotal_desc&page=4&type[]=Chords"))

#print(find_artist_links("https://www.ultimate-guitar.com/explore?decade[]=1950&genres[]=4&page=2&type[]=Chords"))


#print(find_next_pages("https://www.ultimate-guitar.com/explore?decade[]=1950&genres[]=4&order=hitstotal_desc&type[]=Chords"))
#path = 'f:/WebCrawlers/1960Rock.json'


# "artist_url":"https:\/\/www.ultimate-guitar.com\/artist\/elvis_presley_11125",

# [
# {
#     "artist": "whatever",
#     "artist_id": "some-unique-id",  #maybe
#     "song_name": "wahtever",
#     "chords": ["a", "b"]
# },
# ...
# ]

