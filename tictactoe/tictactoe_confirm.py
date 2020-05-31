import json
import boto3
import decimal
import time
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

#confirm player1 has not expired the game(check 'player1_status' field) after player2 has joined
def lambda_handler(event, context):
    
    data = event["queryStringParameters"]
    returned_count = int(data["returned_count"])
    
    for wait_increment in range(20):
        time.sleep(0.1)
        try:
            response = table.get_item(
                Key={
                    "gameId": returned_count-1
                }
            )
        except ClientError as e:
            status_code = e.response['ResponseMetadata']['HTTPStatusCode']
            return return_data(status_code, "even - Re-direct, something went wrong while confirming player1 status")
        else:
            if response['Item']['player1_status'] == "player1 ready":
                status_code = response['ResponseMetadata']['HTTPStatusCode']
                return return_data(status_code, response["Item"]["gameId"])
    return return_data(400, "even - Re-direct, player1 missed")             
                
                
        
       