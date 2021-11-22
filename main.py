import requests
import json

url = 'https://{subdomain}.zendesk.com/api/v2/tickets.json'

def display_menu():
    print('\nSelect an option:')
    print('* View all tickets (1)')
    print('* View a single ticket (2)')
    print('* Quit (3)\n')
    response = input()

    if response == '1':
        display_all_tickets()
    elif response == '2':
        display_single_ticket()
    elif response == '3':
        print('Thanks for using the ticket viewer!\n')
        return -1
    else:
        print('Please enter a valid response.')
    print('\n')

def display_all_tickets():
    tickets = get_tickets()
    if len(tickets) > 25:
        num_pages = (len(tickets) + 25 - 1) // 25
    current_page = 1
    print('Displaying page ' + str(current_page) + ' of ' + str(num_pages) + ':\n')

    #for page in num_pages:
    print('Use the left and right arrow keys to navigate the ticket viewer.')
    for i, ticket in enumerate(tickets):
        print('Ticket #' + str(ticket['id']) + ': \'' + ticket['subject'] + '\' last updated on ' + ticket['updated_at'])

def display_single_ticket():
    tickets = get_tickets()
    response = input('Enter ticket number: ')
    for ticket in tickets:
        if ticket['id'] == int(response):
            print('Ticket #' + response + ': \'' + ticket['subject'] + '\' last updated on ' + ticket['updated_at'])
            return 1;
    print('Unable to find that ticket. Please enter a valid ticket number.')

def get_tickets():
    try:
        r = requests.get(url, auth=('{email}', '{password}'))
    except requests.exceptions.HTTPError as errh:
        print ('Http Error:', errh)
    except requests.exceptions.ConnectionError as errc:
        print ('Error Connecting:', errc)
    except requests.exceptions.Timeout as err:
        print('Timeout error: ', err)
    return r.json()['tickets']

if __name__ == "__main__":
    response = ''
    print('Welcome to the ticket viewer!')
    while response != 'quit':
        response = input('Type \'menu\' to view options or \'quit\' to exit: ')
        if response == 'menu':
            if display_menu() == -1:
                break
        elif response == 'quit':
            print('Thanks for using the ticket viewer!\n')
        else:
            print('Please enter a valid response.\n')
