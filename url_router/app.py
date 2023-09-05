import json

# import requests


def lambda_handler(event, context):
    print(event);
    response = lookup(event);
    return response;

def lookup(event):
    def lambda_handler(event, context):

    # Generate HTTP redirect response with 302 status code and Location header.

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
