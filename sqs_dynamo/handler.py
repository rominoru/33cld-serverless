import json 
import boto3
from datetime import datetime

def to_dynamo_db(status, event):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pedidos-pizzaria')
    for record in event['Records']:
        message_body = json.loads(record['body'])
        pedido, cliente = message_body['key'].replace('pronto/', "").split('-')
        item = {
            'pedido': pedido,
            'datetime': datetime.utcnow().isoformat(),
            'cliente': cliente,
            'status': status
        }
        table.put_item(Item=item)

def em_preparacao_to_dynamodb(event, context):
    to_dynamo_db('em-preparacao', event)

def pronto_to_dynamodb(event, context):
    to_dynamo_db('pronto', event)
