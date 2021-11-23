# ZendeskCodingChallenge
A ticket viewer that allows the user to connect to the Zendesk API and look at their tickets. Created for the Summer 2022 Zendesk Engineering Intern Coding Challenge.

## Setup
The required libraries for this project are located in requirements.txt. Install them with pip:
`pip install -r requirements.txt`

You also need to enter in your credentials into the `.env` file.\
`USER_NAME` should be replaced with your email.\
`API_KEY` should be replaced with the key obtained from Admin -> Channels -> API.\
`URL` only requires the domain to be replaced. (i.e. https://yourdomain.zendesk.com/api/v2/)

## How to run?

You can run the ticket viewer from the command line using
```
python main.py
```

## Usage

The application is very self explanatory. 
First, the program will prompt you to choose between the menu and closing the application.
<img src="https://raw.githubusercontent.com/matthewhung09/ZendeskCodingChallenge/master/.github/images/first_menu.PNG" width="60%" height="60%">

If menu is chosen, it will prompt you again to choose a viewing option.
<img src="https://raw.githubusercontent.com/matthewhung09/ZendeskCodingChallenge/master/.github/images/second_menu.PNG" width="55%" height="55%">

Once finished viewing with your selected option, it will return to the original menu and prompt again for your choice. 
