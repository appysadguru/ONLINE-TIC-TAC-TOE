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
    
# check if 'player2_status' field of the gameId provided as 'returned_count', is changed from 'waiting'. If changed(player2 has
# joined the game), change 'player1_status' field to indicate the game can start
def lambda_handler(event, context):
    
    data = json.loads(event["body"])
    returned_count = data["returned_count"]
    
    try:
        response = table.update_item(
            Key={
                "gameId": returned_count
            },
            UpdateExpression="set player1_status = :e",
            ExpressionAttributeValues = {':e': 'player1 ready', ':s': 'waiting'},
            ConditionExpression="player2_status <> :s",
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return return_data(status_code, "odd - wait")
        else:
            return return_data(status_code, "odd - Re-direct, something went wrong while checking player2 status")
    else:
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, response['Attributes']['gameId'])
              
      