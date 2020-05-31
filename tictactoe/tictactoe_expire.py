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
    
# change 'player2_status' field to 'expired' of the gameId to indicate that it has stopped searching for player2
def lambda_handler(event, context):
    
    data = json.loads(event["body"])
    returned_count = data["returned_count"]
    
    try:
        response = table.update_item(
        Key={
            "gameId": returned_count
        },
        UpdateExpression="set player2_status = :e",
        ExpressionAttributeValues = {':e': "expired"},
        ReturnValues="ALL_NEW"
    )
    except ClientError as e:
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, "odd - Re-direct, something went wrong while changing player2 status to - expired")
    else:
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, "odd - Expired")