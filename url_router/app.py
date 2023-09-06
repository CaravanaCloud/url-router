version = "0.0.1"

caravana = {
    "": "https://github.com/sponsors/CaravanaCloud",
    "aws": "https://aws.amazon.com"
}

redhacks = {
    "": "https://dev.to/redhacks/mentorship-group-mdj",
    "google": "https://google.com"
}

domains = {
    "caravana.cloud": caravana,
    "redhacks.net": redhacks
}

def lambda_handler(event, context):
    # print(event)
    response = lookup(event)
    return response

def lookup(event):
    mvh = event.get("multiValueHeaders")
    host = mvh.get("host")[0]
    (domainPrefix, domainName) = split_host(host)
    path = event.get("path")
    query = event.get("queryStringParameters")

    if (path.startswith("/")):
        path = path[1:]
    
    domain = domains.get(domainName) 
    location = domain.get(path) if domain else None
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
    # print(response)
    return response

def split_host(host):
    if not host: return ("","")
    if not "." in host: return ("", host)
    parts = host.split(".",2)
    if len(parts) == 3:
        return parts[0], parts[1] + "." + parts[2]
    else:
        return '', host