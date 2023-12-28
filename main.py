#!/usr/bin/env python
#coding:utf-8

import constant
import requests
from bs4 import BeautifulSoup as soup

class LibraryItem:
    def __init__(self, title, speaker, link, content_type, length):
        self.title = title
        self.speaker = speaker
        self.link = link
        self.content_type = content_type
        self.length = length

def check_item_type(thumb):
    span = library_item_thumb.find('span')
    svg = span.find('svg')
    path = svg.find('path')
    if path['d'] == constant.VIDEOPATH:
        return "video"
    elif path['d'] == constant.BLOGPATH:
        return "blog"
    else:
        return "unknown"

def check_item_length(thumb):
    span = library_item_thumb.find('span')
    length = span.find('span')
    return length.text

if __name__ == '__main__': 

    base_url = 'https://yougotthis.io'

    response = requests.get('https://yougotthis.io/library/')

    if response.status_code!= 200:
        print('Error: {}'.format(response.status_code))
        exit()

    library = soup(response.content, 'html.parser')
    library_items = library.find_all('a', {'data-v-47be9a8d': True})

    library_items_list = []

    for library_item in library_items:
        # thumb div
        library_item_thumb = library_item.find('div', class_='thumb')
        library_item_content_type = "Type: " + check_item_type(library_item_thumb)
        library_item_content_length = check_item_length(library_item_thumb)
        # meta div
        library_item_meta = library_item.find('div', class_='meta')
        library_item_meta_title = library_item_meta.find('h2')
        library_item_meta_speaker = library_item_meta.find('p')
        library_item_link = base_url + library_item.get('href')
        # append to list
        library_items_list.append(LibraryItem(
            library_item_meta_title.text,
            library_item_meta_speaker.text,
            library_item_content_type,
            library_item_content_length,
            library_item_link
            ))

    for item in library_items_list:
        print(item.title)
        print(item.speaker)
        print(item.content_type)
        print(item.length)
        print(item.link)
        print('-----')

exit()