""" This is main module web browser Akasia. """

import sys
import requests
import html2text


def get_request(url: str) -> None:
    """

    Function for translate binary code to text.

    Args:
        url (str): A variable that stores the URL that will open in the browser Akasia.

    Returns:
        None: The function returns nothing.

    """

    try:
        req_get = requests.get(url)
    except requests.exceptions.MissingSchema:
        choosing_the_right_url = input(
            f"Invalid URL '{url}': No schema supplied. Perhaps you meant http://{url}? (y/n) ")
        if choosing_the_right_url.lower() == 'y' or choosing_the_right_url.lower() == 'yes':
            req_get = requests.get(f'http://{url}')
        else:
            sys.exit()

    cont = str(req_get.content, 'utf-8')
    if len(cont) == 0:
        if req_get.status_code == 200:
            print(html2text.html2text(cont))
        elif req_get.status_code == 404:
            print('Error 404, Not Found!')
        elif req_get.status_code == 500:
            print('Error 500, Internal server error!')
        else:
            print(html2text.html2text(cont))

    # If non-empty content is detected, print it.
    # This is to allow customised html error messages.
    else:
        print(html2text.html2text(cont))


def main() -> None:
    """ This is main function, what initializing web browser Akasia. """

    print('''
          d8888 888                        d8b          
         d88888 888                        Y8P          
        d88P888 888                                     
       d88P 888 888  888  8888b.  .d8888b  888  8888b.  
      d88P  888 888 .88P     "88b 88K      888     "88b 
     d88P   888 888888K  .d888888 "Y8888b. 888 .d888888 
    d8888888888 888 "88b 888  888      X88 888 888  888 
   d88P     888 888  888 "Y888888  88888P' 888 "Y888888\n\n\n''')
    print('Akasia - A fork tiny python text-based web browser Asiakas.\n'.center(58))
    print('Type "quit" or "q" to shut down the browser.'.center(58))

    while True:
        link = input("URL: ")
        if link.lower() == "quit" or link.lower() == "q":
            break

        get_request(link)


main()
