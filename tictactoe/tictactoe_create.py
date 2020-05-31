import json
import boto3
import decimal
import time
import math
from botocore.exceptions import ClientError

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
                
        return super(DecimalEncoder, self).default(o)
        
def return_data(status, text):
    return {
        "isBase64Encoded": False,
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*' 
        }, 
        'body': json.dumps(text, indent=4, cls=DecimalEncoder)
        
    }
    
dynamodb = boto3.resource("dynamodb", region_name='us-east-2')
table = dynamodb.Table('Game')

# create a game object with the provided 'returned_count' value as the gameId(partition key)
def lambda_handler(event, context):
    
    data = json.loads(event["body"])
    returned_count = data["returned_count"]
    
    try:
        response = table.put_item(
            Item={
                'gameId': returned_count,
                'player1_status': "-",
                'player2_status': 'waiting',
                'board_list':["-"]*9,
                'entered_inputs':[],
                'result': "-",
                'time_to_live': math.floor(time.time())  + 3600
            }
        )
    except ClientError as e:
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, "odd - Re-direct, something went wrong while creating the gameId")
    else:
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, returned_count)
                
