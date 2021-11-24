import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

USER_NAME = os.getenv('USER_NAME')
API_KEY = os.getenv('API_KEY')
URL = os.getenv('URL')

all_tickets = {}
ticket_ids = {}

# Displays the menu options for viewing tickets
def display_menu():
    print('\nSelect an option:')
    print('* Press 1 to view all tickets (1)')
    print('* Press 2 to view a single ticket (2)')
    print('* Press 3 to quit (3)\n')
    response = input()

    if response == '1':
        display_all_tickets()
        return 1
    elif response == '2':
        display_single_ticket()
        return 2
    elif response == '3':
        print('Thanks for using the ticket viewer!\n')
        return 3
    else:
        print('Please enter a valid response.')
        return -1

# Displays all tickets in paginated manner
def display_all_tickets():
    # Determine out how many pages of tickets we have
    if len(all_tickets) > 25:
        num_pages = (len(all_tickets) + 25 - 1) // 25
    else:
        num_pages = len(all_tickets)

    response = ''
    current_page = 1
    valid_response = True
    
    # Keep prompting user for page number until they decide to go back
    while response != 'back':
        if valid_response:
            # If last page, make sure we don't try to print past the last ticket
            if current_page == num_pages:
                max_per_page = len(all_tickets) % 25
            else:
                max_per_page = 25
            for i in range(0, max_per_page):
                ticket = all_tickets[i + (25 * (current_page - 1))]
                print('Ticket #' + str(ticket['id']) + ': \'' + ticket['subject'] + '\' last updated on ' + ticket['updated_at'][0:10])
                i += 1

            print('Viewing tickets ' + str(1 + 25 * (int(current_page) - 1)) + '-' + str(max_per_page) + ' of ' + str(len(all_tickets)) + 
                ', page ' + str(current_page) + ' of ' + str(num_pages) + '\n')
            response = input('Enter the number page you would like to view or type \'back\' to return to the menu: ')
        if response == 'back':
            return False
        if is_valid_response(response, num_pages):
            current_page = int(response)
            valid_response = True
        # If invalid response, prompt user again
        else: 
            response = input('Invalid reponse, please enter a valid response: ')
            valid_response = False

# Check if inputted value is a number and if it is within page limit.
# Returns True if valid reponse and False if not
def is_valid_response(response, num_pages):
    if not response.isnumeric() or int(response) > num_pages or int(response) < 1:
        return False
    else:
        return True

# Displays a single ticket with user given id
def display_single_ticket():
    response = input('Enter ticket number: ')
    found_ticket = False

    # Loops until a valid ticket number is entered
    while not found_ticket:
        if not response.isnumeric():
            response = input('Please only enter a numerical value: ')
        # Search in created hash table for the id
        elif int(response) in ticket_ids:
            ticket_number = int(response)
            display_ticket_information(ticket_number, 'users/' + str(ticket_ids[ticket_number]['requester_id']) + '.json')
            found_ticket = True
        else:
            response = input('Unable to find that ticket. Please enter a valid ticket number: ')
    return True

# Displays detailed information for a single ticket
# Shows requester name, subject, and description of ticket
def display_ticket_information(ticket_number, arg):
    # Convert requester_id from ticket information to the user's actual name
    name = call_api(arg)

    if name == -1:
        exit()
    else:
        name = name['user']['name']

    print('\nRequestor: ' + name)
    print('Subject: ' + ticket_ids[ticket_number]['subject'])
    print('\nDescription: ' + ticket_ids[ticket_number]['description'] + '\n')
    return name

# Store ticket_ids in a hash table for O(1) look up times

# This allows us to quickly search if the user provided ticket number exists
# rather than doing a linear search each time

# I use 2 different hash tables here - one just for storing ticket information
# and one for ticket ids. This is due to the fact we cannot get a select 25 
# ticket when selecting from a dictionary when trying to display all tickets

# Offset is to account for multiple pages of tickets
def store_tickets(offset, tickets):
    for i, ticket in enumerate(tickets):
        all_tickets[i + offset * 100] = ticket
        ticket_ids[ticket['id']] = ticket

# Connect to API and make a request
def call_api(arg):
    try:
        # Handles getting tickets
        if arg == 'tickets.json':
            offset = 0
            arg = arg + '?page[size]=100'
            r = requests.get(URL + arg, auth=(USER_NAME + '/token', API_KEY))
            store_tickets(offset, r.json()['tickets'])

            # Keep getting tickets in pages of 100 until no more left
            while r.json()['meta']['has_more']:
                r = requests.get(r.json()['links']['next'], auth=(USER_NAME + '/token', API_KEY))
                offset += 1
                store_tickets(offset, r.json()['tickets'])

        else: 
            r = requests.get(URL + arg, auth=(USER_NAME + '/token', API_KEY))

        r.raise_for_status() # Allows for http errors to raise exceptions

    # Handles HTTP error i.e 401, 403, etc.
    except requests.exceptions.RequestException as err:
        print (err)
        return -1
    # Handles invalid HTTP response
    except requests.exceptions.HTTPError as errh:
        print ('Http Error:', errh)
        return -1
    # Handles network issues
    except requests.exceptions.ConnectionError as errc:
        print ('Error Connecting:', errc)
        return -1
    # Handles request timeout error
    except requests.exceptions.Timeout as err:
        print('Timeout error: ', err)
        return -1

    return r.json()

if __name__ == "__main__":
    # Makes a single call to the API to get all tickets
    # As someone who works in an IT Support setting, there aren't normally an 
    # abnormally large amount of tickets in the queue, so using a single API
    # call to get them all at once seems better in this situation
    if call_api('tickets.json') == -1:
        exit()

    print('Welcome to the ticket viewer!')
    response = ''

    # Keep looping until quit is typed
    while response != 'quit':
        response = input('Type \'menu\' to view options or \'quit\' to exit: ')
        if response == 'menu':
            # Check if choice in menu is 'quit'
            if display_menu() == 3:
                break
        elif response == 'quit':
            print('Thanks for using the ticket viewer!\n')
        else:
            print('Please enter a valid response.\n')
