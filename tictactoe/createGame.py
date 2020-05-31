import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

def lambda_handler(event, context):
    # TODO implement
    
    table = dynamodb.create_table(
        TableName='Game',
        KeySchema=[
            {
                'AttributeName': 'gameId',
                'KeyType': 'HASH'  #Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'gameId',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 3,
            'WriteCapacityUnits': 3
        }
    )
    
    print("Table status:", table.table_status)
    
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
    }