import sys
import json
import boto3

channel = sys.argv[1]
image_url = sys.argv[2]
title = sys.argv[3]

payload = {
    'channel': channel,
    'attachments': [{
        'text': title,
        'image_url': image_url
    }]
}

client = boto3.client('lambda')
response = client.invoke(
    FunctionName='upordownbot-mention',
    InvocationType='Event',
    Payload=json.dumps(payload)
)
