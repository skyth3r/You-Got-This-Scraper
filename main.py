#!/usr/bin/env python
#coding:utf-8

import constant
import requests
from bs4 import BeautifulSoup as soup

class Person:
    def __init__(self, name, link):
        self.name = name
        self.link = link
    
class VideoItem:
    def __init__(self, title, people, link, content_type, side_copy, summary, transcript):
        self.title = title
        self.people = people
        self.link = link
        self.content_type = content_type
        self.side_copy = side_copy
        self.summary = summary
        self.transcript = transcript

class BlogItem:
    def __init__(self, title, people, link, content_type, article):
        self.title = title
        self.people = people
        self.link = link
        self.content_type = content_type
        self.article = article

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

    video_items = []
    blog_items = []

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
        
        if content_type == "Video":
            # side copy
            aside_div = aside.find('div',  class_='box')
            side_copy = aside_div.text
            # summary (if present)
            if main.find('details'):
                summary_div = main.find('details').find('div', class_='text')
                summary = summary_div.text
            else:
                summary = ""
            # transcript (if present)
            if main.find('article'):
                article_div = main.find('article')
                article = article_div.text
            else:
                article = ""
        elif content_type == "Blog":
            article_div = main.find('article')
            article = article_div.text

        if content_type == "Video":
            video_item = VideoItem(
                title.text,
                people_list,
                url,
                content_type,
                side_copy,
                summary,
                article
                )
            video_items.append(video_item)
        elif content_type == "Blog":
            blog_item = BlogItem(
                title.text,
                people_list,
                url,
                content_type,
                article
                )
            blog_items.append(blog_item)

    # create text file
    file = open("data.txt", "a")

    for item in video_items:
        md_title = "[" + item.title + "]" + "(" + item.link + ")"

        speakers = []
        for speaker in item.people:
            speakers.append("[" + speaker.name.strip() + "]" + "(" + speaker.link + ")")
    
        item_string = "| " + md_title + " | " + item.content_type + " | " + ', '.join(speakers) + " | " + '<input type="checkbox" unchecked>' + " |\n" 
        file.write(item_string)

    for item in blog_items:
        md_title = "[" + item.title + "]" + "(" + item.link + ")"

        authors = []
        for author in item.people:
            authors.append("[" + author.name.strip() + "]" + "(" + author.link + ")")

        item_string = "| " + md_title + " | " + item.content_type + " | " + ', '.join(authors) + " | " + '<input type="checkbox" unchecked>' + " |\n" 
        file.write(item_string)

    file.close()

exit()