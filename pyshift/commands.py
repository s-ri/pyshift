# coding: utf-8

import os
import json
import requests
from requests.auth import HTTPBasicAuth
import jwt
import click
from . import helpers

# load shift settings
settings = helpers.load_settings()
endpoints = settings.get('endpoints')
shift = settings.get('shift')

ShiftCommand = click.Group()


def echo(http_code, response):
    parsed = json.dumps(response, indent=4, sort_keys=True)

    if http_code is not None:
        print('code:', http_code)

    print('data:', parsed)


@ShiftCommand.command()
def client_credentials():
    """
    Client Credentials Grant Flow
    """
    payload = {
        'grant_type': 'client_credentials',
        'scope': 'batch',
    }
    r = requests.post(endpoints['token'],
                      auth=HTTPBasicAuth(
                          shift['private_client_id'], shift['client_secret']),
                      json=payload)

    echo(r.status_code, r.json())


@ShiftCommand.command()
@click.option('-t', '--token', type=click.STRING, help='ID Token')
@click.option('--cache', is_flag=True, help='Access Token info cached')
def issue_token(token, cache):
    """
    Issue AccessToken
    """
    payload = {
        'grant_type': 'id_token',
        'id_token': token,
    }

    r = requests.post(endpoints['token'],
                      auth=HTTPBasicAuth(
                          shift['private_client_id'], shift['client_secret']),
                      json=payload)

    echo(r.status_code, r.json())

    if cache and r.status_code == 200:
        with open('cache.txt', 'w') as f:
            f.write(json.dumps(r.json()))
    else:
        with open('cache.txt', 'w') as f:
            f.write('')


@ShiftCommand.command()
@click.option('-t', '--token', type=click.STRING, help='Verify ID Token')
@click.option('--force', is_flag=True, help='Is force verify options')
def verify(token, force):
    """
    Verify id_token
    """
    # load public_key.pem
    _key_file = os.path.join(helpers.BASE_DIR, shift['public_key'])

    with open(_key_file) as f:
        public_key = f.read()

    payload = None
    # JWT decode
    try:
        payload = jwt.decode(token, public_key,
                             algorithm='RS256', verify=force)
    except jwt.PyJWTError as e:
        print(e)

    echo(None, payload)


@ShiftCommand.command()
@click.option('-t', '--token', type=click.STRING, help='Access Token')
@click.option('--cache', is_flag=True, help='Using cache data')
def refresh_token(token, cache):
    """
    Refresh AccessToken
    """
    if cache:
        with open('cache.txt') as f:
            d = json.loads(f.read())
            token = d['refresh_token']

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': token,
    }

    r = requests.post(endpoints['token'],
                      auth=HTTPBasicAuth(
                          shift['private_client_id'], shift['client_secret']),
                      json=payload)

    echo(r.status_code, r.json())

    if cache and r.status_code == 200:
        with open('cache.txt', 'w') as f:
            f.write(json.dumps(r.json()))


@ShiftCommand.command()
def login():
    """
    Simulation shift login
    """
    payload = settings.get('developer_account')

    r = requests.post(endpoints['token'],
                      auth=HTTPBasicAuth(
                          shift['public_client_id'], shift['client_secret']),
                      json=payload)

    echo(r.status_code, r.json())


@ShiftCommand.command()
@click.option('-t', '--token', type=click.STRING, help='Access Token')
@click.option('--cache', is_flag=True, help='Using cache data')
def payment_order(token, cache):
    """
    Make payment order
    """
    if cache:
        with open('cache.txt') as f:
            d = json.loads(f.read())
            token = d['token']

    payload = {
        'client_order_id': helpers.make_transation_id(),  # transation_id
        'item_name': 'アイテム100',
        'price': 1,
    }

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    print("payload: ", payload)
    print('headers: ', headers)
    print('api: ', endpoints['payment'])

    r = requests.post(endpoints['payment'],
                      json=payload,
                      headers=headers)

    echo(r.status_code, r.json())


@ShiftCommand.command()
@click.option('-o', '--order_id', type=click.STRING, help='Order Id')
@click.option('-t', '--token', type=click.STRING, help='Access Token')
@click.option('--cache', is_flag=True, help='Using cache data')
def payment_verify_receipt(order_id, token, cache):
    if cache:
        with open('cache.txt') as f:
            d = json.loads(f.read())
            token = d['token']

    endpoint = '{api}/{order_id}'.format(api=endpoints['payment'],
                                         order_id=order_id)

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    r = requests.get(endpoint, headers=headers)

    echo(r.status_code, r.json())


@ShiftCommand.command()
@click.option('-o', '--order_id', type=click.STRING, help='Order Id')
@click.option('-t', '--token', type=click.STRING, help='Access Token')
@click.option('--cache', is_flag=True, help='Using cache data')
def payment_cancel(order_id, token, cache):
    if cache:
        with open('cache.txt') as f:
            d = json.loads(f.read())
            token = d['token']

    endpoint = '{api}/{order_id}'.format(api=endpoints['payment'],
                                         order_id=order_id)

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    r = requests.delete(endpoint, headers=headers)

    echo(r.status_code, r.json())
