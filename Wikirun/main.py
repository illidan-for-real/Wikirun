from bs4 import BeautifulSoup
import requests
import random
import urllib.request
import time


def game_end(guess_list_title, starting_url, ending_url):
    print("Congratulations, you arrived at your destination with " + str(guess_list_title.__len__()) + " links!")
    print()
    print(starting_url + ' to ' + ending_url)


def activate(option, starting_url, ending_url, links, base_url, guess_list_title, guess_list_href,
             depth, filter_keep_list, filter_out_list, ):
    select_link(option, starting_url, ending_url, links, base_url, guess_list_title, guess_list_href,
                depth, filter_keep_list, filter_out_list, )


def select_link(option, starting_url, ending_url, links, base_url, guess_list_title, guess_list_href,
                depth, filter_keep_list, filter_out_list, ):
    response = requests.get(starting_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    check_count = 0

    if links:

        url = base_url + str(links[option][1])

        guess_list_title.append(links[option][0])
        guess_list_href.append(links[option][1])

        print()
        print(url)
        print()

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

    else:

        url = starting_url

    if (url.lower()) == ending_url.lower():

        game_end(
            guess_list_title,
            starting_url,
            ending_url
        )
        return True, guess_list_title

    else:

        links.clear()

        for i in soup.findAll('a'):

            # print(type(i))

            link_string = str(i)
            if not depth <= 0:
                pass
                # print(i)

            for x in filter_keep_list:

                if x in link_string:
                    check_count += 1

                # print(check_count)

            for x in filter_out_list:

                if not x in link_string:
                    check_count += 1

            if check_count == filter_keep_list.__len__() + filter_out_list.__len__():

                start_indx = link_string.find('title') + 7
                href_start_indx = link_string.find('href') + 6

                title_string = link_string[start_indx:]
                href_string = link_string[href_start_indx:]

                end_indx = title_string.find('"')
                href_end_indx = href_string.find('"')

                title = title_string[0:end_indx]
                href = href_string[0:href_end_indx]

                if not [title, href] in links:
                    links.append([title, href])
                    print(str(links.index([title, href]) + 1) + ' ' + title)
                    # print()

                check_count = 0

            check_count = 0

        print()
        print('List length: ' + str(links.__len__()))
        print()
        print('(' + str(guess_list_title.__len__()) + ') ' + 'Links visited: ' + ', '.join(
            '"{0}"'.format(w) for w in guess_list_title))
        print()

        if (url.lower()) != ending_url.lower():
            print("Enter an option: ")
            select_link(int(input()) - 1, starting_url, ending_url, links, base_url, guess_list_title, guess_list_href,
                     depth, filter_keep_list, filter_out_list, )


def main():
    # starting_url = 'https://en.wikipedia.org/wiki/Special:Random'
    # ending_url = 'https://en.wikipedia.org/wiki/Special:Random'

    # DEBUG PURPOSES
    starting_url = 'https://en.wikipedia.org/wiki/superman'
    ending_url = 'https://en.wikipedia.org/wiki/music'

    response = requests.get(starting_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    base_url = 'https://en.wikipedia.org'

    links = []

    depth = 10
    check_count = 0

    guess_list_title = []
    guess_list_href = []

    filter_keep_list = ['href', 'wiki', 'title']
    filter_out_list = ['zh', 'pedia', 'identifier', 'accesskey', 'extiw', '/Portal', 'mw-wiki-logo', '/Category',
                       '/Help', '/Special', 'Template:']

    print()
    print('Starting URL: ' + response.url)
    print('Destination URL: ' + ending_url)
    print()

    select_link(
        0,
        starting_url,
        ending_url,
        links,
        base_url,
        guess_list_title,
        guess_list_href,
        depth,
        filter_keep_list,
        filter_out_list,
    )


if __name__ == '__main__':
    main()
