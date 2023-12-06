import logging
import json

version = "0.0.3"

data = {
    "caravana.cloud/": "https://github.com/sponsors/CaravanaCloud",
    "caravana.cloud/aws": "https://aws.amazon.com",
    "redhacks.net": "https://dev.to/redhacks/mentorship-group-mdj",
    "redhacks.net/google": "https://google.com",
    "well-architected.info": "https://aws.amazon.com/architecture/well-architected/"
}

logging.basicConfig(level=100)
log = logging.getLogger()

def debug(message, *args):
    # log.debug(message, *args)
    print(message, *args)
    
def lambda_handler(event, context):
    debug("lambda_handler()")
    debug(json.dumps(event, indent=4))
    response = lookup(event)
    return response

def keyOf(domain, path):
    return domain + path

def lookup_kvs(key):
    return None

def lookup_dict(key):
    return data.get(key)

def lookup(event):
    mvh = event.get("multiValueHeaders")
    host = mvh.get("host")[0] if mvh else None
    (domainPrefix, domainName) = split_host(host)
    path = event.get("path","")
    query = event.get("queryStringParameters")
    key = keyOf(domainName, path)
    location = lookup_kvs(key) or lookup_dict(key)
    headers = {
                'Content-Type': 'text/plain',
                'x-url-router-domainName': domainName,
                'x-url-router-domainPrefix': domainPrefix,
                'x-url-router-query': query,
                'x-url-router-path': path,
                'x-url-router-version': version
            }
    mvheaders = {
        "x-url-router-domainNames": [domainName]
    }
    if location:
        mvheaders['Location'] = [location]
        headers['Location'] = location
        response = {
            'statusCode': 302,
            'statusDescription': 'Found',
            'isBase64Encoded': False,
            'headers': headers,
            'multiValueHeaders': mvheaders,
            'body': 'Found '+location
        }
    else:
        response = {
            'statusCode': 404,
            'statusDescription': 'Not found',
            'headers': headers,
            'multiValueHeaders': mvheaders,
            'isBase64Encoded': False,
            'body': 'Not found '+path
        }
    debug("--- response ---")
    debug(json.dumps(response, indent=4))
    return response

def split_host(host):
    if not host: return ("","")
    if not "." in host: return ("", host)
    parts = host.split(".",2)
    if len(parts) == 3:
        return parts[0], parts[1] + "." + parts[2]
    else:
        return '', host