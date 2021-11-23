import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('PASSWORD')

url = 'https://zccmhung.zendesk.com/api/v2/tickets.json'
ticket_ids = {}

# Displays the menu options for viewing tickets
def display_menu(tickets):
    print('\nSelect an option:')
    print('* View all tickets (1)')
    print('* View a single ticket (2)')
    print('* Quit (3)\n')
    response = input()

    if response == '1':
        display_all_tickets(tickets)
    elif response == '2':
        display_single_ticket(tickets)
    elif response == '3':
        print('Thanks for using the ticket viewer!\n')
        return -1
    else:
        print('Please enter a valid response.')

# Displays all tickets in paginated manner
def display_all_tickets(tickets):
    # Determine out how many pages of tickets we have
    if len(tickets) > 25:
        print(len(tickets))
        num_pages = (len(tickets) + 25 - 1) // 25

    response = ''
    current_page = 1
    valid_response = True

    # Keep prompting user for page number until they decide to go back
    while response != 'back':
        if valid_response:
            for i in range(0, 25):
                ticket = tickets[i + (25 * (int(current_page) - 1))]
                print('Ticket #' + str(ticket['id']) + ': \'' + ticket['subject'] + '\' last updated on ' + ticket['updated_at'])

            print('Displaying page ' + str(current_page) + ' of ' + str(num_pages) + ':\n')
            response = input('Enter the number page you would like to view or type \'back\' to return to the menu: ')
        if response == 'back':
            break
        if is_valid_response(response, num_pages):
            current_page = response
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
def display_single_ticket(tickets):
    response = input('Enter ticket number: ')
    found_ticket = False

    # Loops until a valid ticket number is entered
    while not found_ticket:
        if not response.isnumeric():
            response = input('Please only enter a numberical value: ')
        # Search in created hash table for the id
        elif int(response) in ticket_ids:
            print('Ticket #' + response + ': \'' + ticket_ids[int(response)]['subject'] + '\' last updated on ' + ticket_ids[int(response)]['updated_at'] + '\n')
            found_ticket = True
        else:
            response = input('Unable to find that ticket. Please enter a valid ticket number: ')

# Store tickets in a hash table for O(1) look up times
def store_ticket_numbers(tickets):
    for ticket in tickets:
        ticket_ids[ticket['id']] = ticket

# Connect to API and get tickets
def get_tickets():
    try:
        r = requests.get(url, auth=(EMAIL_ADDRESS, PASSWORD))
    except requests.exceptions.HTTPError as errh:
        print ('Http Error:', errh)
    except requests.exceptions.ConnectionError as errc:
        print ('Error Connecting:', errc)
    except requests.exceptions.Timeout as err:
        print('Timeout error: ', err)
    return r.json()['tickets']

if __name__ == "__main__":
    response = ''
    tickets = get_tickets()
    store_ticket_numbers(tickets)
    print('Welcome to the ticket viewer!')
    while response != 'quit':
        response = input('Type \'menu\' to view options or \'quit\' to exit: ')
        if response == 'menu':
            # Check if choice in menu is 'quit'
            if display_menu(tickets) == -1:
                break
        elif response == 'quit':
            print('Thanks for using the ticket viewer!\n')
        else:
            print('Please enter a valid response.\n')
