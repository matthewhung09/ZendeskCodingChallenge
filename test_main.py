import pytest
import requests
from pytest_mock import mocker
from main import *

# Testing user input calls the correct function/gives correct response
def test_display_menu_1(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', lambda: '1')  
    mocker.patch('main.display_all_tickets') # Mock the function that should be called  
    assert display_menu() == 1

def test_display_menu_2(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', lambda: '2') 
    mocker.patch('main.display_single_ticket')  
    assert display_menu() == 2

# Quit menu - user input 3
def test_display_menu_3(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', lambda: '3')  
    assert display_menu() == 3

# Invalid response
def test_display_menu_4(monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', lambda: 'asdf')  
    assert display_menu() == -1


def test_display_all_tickets(monkeypatch, mocker):
    test_ticket = [
        {
            "url": "https://zccmhung.zendesk.com/api/v2/tickets/101.json",
            "id": 1,
            "subject": "in nostrud occaecat consectetur aliquip",
            "raw_subject": "in nostrud occaecat consectetur aliquip",
            "description": "Esse esse quis ut esse nisi tempor sunt. Proident officia incididunt cupidatat laborum ipsum duis. Labore qui labore elit consequat.\n\nDo id nisi qui et fugiat culpa veniam consequat ad amet ut nisi ipsum. Culpa exercitation consectetur adipisicing sunt reprehenderit. Deserunt consequat aliquip tempor anim officia elit proident commodo consequat aute. Magna enim esse tempor incididunt ipsum dolore Lorem cupidatat incididunt.",
            "updated_at": "2021-11-19T22:01:55Z",
            "status": "open",
            "requester_id": 1523681605421,
            "submitter_id": 1523681584221,
            "assignee_id": 1523681584221,
            "organization_id": 1500627827201,
            "group_id": 1500006565301
        }
    ]
    monkeypatch.setattr('builtins.input', lambda _: 'back')
    store_tickets(0, test_ticket)
    assert not display_all_tickets()


def test_display_single_ticket(monkeypatch, mocker):
    test_ticket = [
        {
            "url": "https://zccmhung.zendesk.com/api/v2/tickets/101.json",
            "id": 1,
            "subject": "in nostrud occaecat consectetur aliquip",
            "raw_subject": "in nostrud occaecat consectetur aliquip",
            "description": "Esse esse quis ut esse nisi tempor sunt. Proident officia incididunt cupidatat laborum ipsum duis. Labore qui labore elit consequat.\n\nDo id nisi qui et fugiat culpa veniam consequat ad amet ut nisi ipsum. Culpa exercitation consectetur adipisicing sunt reprehenderit. Deserunt consequat aliquip tempor anim officia elit proident commodo consequat aute. Magna enim esse tempor incididunt ipsum dolore Lorem cupidatat incididunt.",
            "status": "open",
            "requester_id": 1523681605421,
            "submitter_id": 1523681584221,
            "assignee_id": 1523681584221,
            "organization_id": 1500627827201,
            "group_id": 1500006565301
        }
    ]
    monkeypatch.setattr('builtins.input', lambda _: '1')
    mocker.patch('main.display_ticket_information')  
    store_tickets(0, test_ticket)
    assert display_single_ticket() 

def test_display_ticket_information(mocker):
    user_info = {
        "user": {
            "id": 1523681605421,
            "url": "https://zccmhung.zendesk.com/api/v2/users/1523681605421.json",
            "name": "The Customer",
            "email": "customer@example.com",
        }
    }
    test_ticket = [
        {
            "url": "https://zccmhung.zendesk.com/api/v2/tickets/101.json",
            "id": 1,
            "subject": "in nostrud occaecat consectetur aliquip",
            "raw_subject": "in nostrud occaecat consectetur aliquip",
            "description": "Esse esse quis ut esse nisi tempor sunt. Proident officia incididunt cupidatat laborum ipsum duis. Labore qui labore elit consequat.\n\nDo id nisi qui et fugiat culpa veniam consequat ad amet ut nisi ipsum. Culpa exercitation consectetur adipisicing sunt reprehenderit. Deserunt consequat aliquip tempor anim officia elit proident commodo consequat aute. Magna enim esse tempor incididunt ipsum dolore Lorem cupidatat incididunt.",
            "status": "open",
            "requester_id": 1523681605421,
            "submitter_id": 1523681584221,
            "assignee_id": 1523681584221,
            "organization_id": 1500627827201,
            "group_id": 1500006565301
        }
    ]
    mocker.patch('main.call_api', return_value=user_info)
    store_tickets(0, test_ticket)
    assert display_ticket_information(1, 'users/1523681605421.json') == "The Customer"

def test_is_valid_response():
    assert(is_valid_response('1', 5))
    assert(is_valid_response('5', 5))
    assert(is_valid_response('3', 5))
    assert(is_valid_response('1', 1))

    assert not (is_valid_response('asdf', 5)) # non-number input
    assert not (is_valid_response('0', 5)) # invalid page input (lower)
    assert not (is_valid_response('10', 5)) # invalid page input (upper)
    assert not (is_valid_response('', 5)) # empty string
