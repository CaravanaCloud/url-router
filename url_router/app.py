import json

# import requests


def lambda_handler(event, context):
    print(event)
    response = lookup(event)
    return response

def lookup(event):
    response = {
        'status': '302',
        'statusDescription': 'Found',
        'headers': {
            'location': [{
                'key': 'Location',
                'value': 'https://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html'
            }]
        }
    }
    return response
