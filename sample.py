from datetime import datetime
import requests
import pandas
import argparse


# Run more advanced user-supplied queries on inventory
def runInventoryQuery(query):
    body = {
        'sql_query': query
    }
    result = requests.get(
        f'https://sample.app/sql_query',
        cert = ('client.crt', 'client.key'),
        verify = 'ca.crt',
        json = body
    )

    return result.json()

# Gets a single item's details
def get_item(item_id):
    result = requests.get(
        'https://sample.app/get_item/' + item_id + '/',
        cert=('client.crt', 'client.key'),
        verify='ca.crt'
    )

    product_name = result.json()['product_name']
    quantity = result.json()['quantity']
    last_modified = result.json()['last_modified']

    last_modified_dt = datetime.strptime(last_modified, '%Y-%m-%dT%H:%M:%SZ')
    last_sold_delta = (datetime.utcnow() - last_modified_dt).days

    display_name = product_name + ' (' + item_id + ')'

    x = {
        'display_name': display_name,
        'quantity': quantity,
        'last_modified': last_modified,
        'days_ago_last_sold': last_sold_delta
    }

    return x

# Sells an item and returns updated item details
def sell_item(item_id, num_to_sell):
    result = requests.get(
        'https://sample.app/get_item/' + item_id + '/',
        cert=('client.crt', 'client.key'),
        verify='ca.crt'
    )

    product_name = result.json()['product_name']
    quantity = result.json()['quantity']
    last_modified = result.json()['last_modified']

    last_modified_dt = datetime.strptime(last_modified, '%Y-%m-%dT%H:%M:%SZ')
    last_sold_delta = (datetime.utcnow() - last_modified_dt).days

    display_name = product_name + ' (' + item_id + ')'

    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    new_quantity = quantity - num_to_sell

    body = {
        'product_name': product_name,
        'quantity': new_quantity,
        'last_modified': current_time
    }

    result = requests.patch(
        'https://sample.app/update_item/' + item_id + '/',
        cert=('client.crt', 'client.key'),
        verify='ca.crt',
        json = body
    )

    x = {
        'display_name': display_name,
        'quantity': new_quantity,
        'last_modified': current_time,
        'days_ago_last_sold': 0
    }

    return x

# Main
parser=argparse.ArgumentParser(description='Interact with inventory system')
parser.add_argument('ITEM_ID')
parser.add_argument('-s', '--sell')
parser.add_argument('-q', '--query')
args=parser.parse_args()

if not args.sell and not args.query:
    print(get_item(args.ITEM_ID))

if args.sell:
    print(sell_item(args.ITEM_ID, args.sell))

if args.query:
    print(runInventoryQuery(args.query))