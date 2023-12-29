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
            content_type = "video"
        else:
            content_type = "blog"

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
        
        if content_type == "video":
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
        elif content_type == "blog":
            article_div = main.find('article')
            article = article_div.text

        if content_type == "video":
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
        elif content_type == "blog":
            blog_item = BlogItem(
                title.text,
                people_list,
                url,
                content_type,
                article
                )
            blog_items.append(blog_item)

    for item in video_items:
        speakers = []
        for speaker in item.people:
            speakers.append(speaker.name + "(" + speaker.link + ")")
        print(item.title)
        print(speakers)
        print(item.link)
        print(item.content_type)
        print(item.side_copy)
        print(item.summary)
        print(item.transcript)
        print("----")
    
    for item in blog_items:
        authors = []
        for author in item.people:
            authors.append(author.name + "(" + author.link + ")")
        print(item.title)
        print(authors)
        print(item.link)
        print(item.content_type)
        print(item.article)
        print("----")

exit()