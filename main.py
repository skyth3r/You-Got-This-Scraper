#!/usr/bin/env python
#coding:utf-8

import constant
import requests
from bs4 import BeautifulSoup as soup

class Person:
    def __init__(self, name, link):
        self.name = name
        self.link = link

class Item:
    def __init__(self, title, people, link, content_type):
        self.title = title
        self.people = people
        self.link = link
        self.content_type = content_type

if __name__ == '__main__': 

    base_url = 'https://yougotthis.io'

    response = requests.get(base_url + '/library/')

    if response.status_code!= 200:
        print('Error: {}'.format(response.status_code))
        exit()

    library = soup(response.content, 'html.parser')
    library_items = library.find_all('a', {'data-v-47be9a8d': True})

    urls_list = []

    for library_item in library_items:
        library_item_link = base_url + library_item.get('href')
        urls_list.append(library_item_link)

    items = []

    for url in urls_list:
        item_page_response = requests.get(url)
        
        item_page = soup(item_page_response.content, 'html.parser')

        if item_page_response.status_code!= 200:
            print("Error: {}, url: {}".format(item_page_response.status_code, url))
            continue

        # find item type
        main = item_page.find('main')
        if main.find('iframe'):
            content_type = "Video"
        else:
            content_type = "Blog"

        # get item title
        title = item_page.find('h1')

        # get people
        aside = item_page.find('aside')
        a_tags = aside.find_all('a')

        people_list = []

        for person in a_tags:
            if person['href'].startswith("/people/"):
                name = person.find('p')
                person_url = base_url + person['href']
                people_list.append(Person(name.text, person_url))

        # add item to list
        item = Item(title.text,
                    people_list,
                    url,
                    content_type
                    )
        items.append(item)

    # create text file
    file = open("data.txt", "a")

    # add items to text file
    for item in items:
        md_title = "[" + item.title + "]" + "(" + item.link + ")"

        people = []
        for person in item.people:
            people.append("[" + person.name.strip() + "]" + "(" + person.link + ")")
        
        item_string = "| " + md_title + " | " + item.content_type + " | " + ', '.join(people) + " | " + '<input type="checkbox" unchecked>' + " |\n" 

        file.write(item_string)

    file.close()

exit()