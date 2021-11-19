import requests
import json

url = 'https://{subdomain}.zendesk.com/api/v2/tickets.json'

def display_menu():
    print('Select view options:')
    print('* Press 1 to view all tickets')
    print('* Press 2 to view a tickets')
    print('* Type \'quit\' 1 to exit\n')
    response = input()

    if response == '1':
        print('viewing all tickets:\n')
    elif response == '2':
        print('viewing single ticket\n')
    elif response == 'quit':
        print('Goodbye.\n')
        return -1

if __name__ == "__main__":
    response = ''
    print('Welcome to the ticket viewer!')
    while response != 'quit':
        response = input('Type \'menu\' to view options or \'quit\' to exit:\n')
        if response == 'menu':
            if display_menu() == -1:
                response = 'quit'
        elif response == 'quit':
            print('Goodbye.\n')
        else:
            print('Please enter a valid response.\n')

    r = requests.get(url, auth=('email_address', 'password'))
    print(r.json()['tickets'][0]['description'])