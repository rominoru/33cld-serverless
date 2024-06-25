import json
import boto3

def handler(event, context):
    # Initialize SQS client
    sqs = boto3.client('sqs')
    
    # Your SQS queue URL
    queue_url_pronto_pizzaria = 'https://sqs.us-east-1.amazonaws.com/981004968329/pronto-pizzaria'
    queue_url_em_preparacao_pizzaria = 'https://sqs.us-east-1.amazonaws.com/981004968329/em-preparacao-pizzaria'
    
    # Extract information from the S3 event
    for record in event['Records']:
        s3 = record['s3']
        bucket = s3['bucket']['name']
        key = s3['object']['key']
        
        print(s3)
        print(bucket)
        print(key)
        
        # Create a message with the bucket and object key
        message = {
            'bucket': bucket,
            'key': key
        }
        
        if('pronto-pizzaria/' in key):
            response = sqs.send_message(
                QueueUrl=queue_url_pronto_pizzaria,
                MessageBody=json.dumps(message)
            )
        elif('em-preparacao-pizzaria/' in key):
            response = sqs.send_message(
                QueueUrl=queue_url_em_preparacao_pizzaria,
                MessageBody=json.dumps(message)
            )
        
        print(f'Message sent to SQS queue: {response["MessageId"]}')

    return {
        'statusCode': 200,
        'body': json.dumps('Message successfully sent to SQS')
    }