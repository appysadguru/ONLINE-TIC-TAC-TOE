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

# if the provided gameId is not expired and it's 'player2_status' field is not 'expired' then change 'player2_status' field to
# indicate that player2 has joined
def lambda_handler(event, context):
    
    data = json.loads(event["body"])
    returned_count = data["returned_count"]
    
    try:
        response = table.update_item(
            Key={
                "gameId": returned_count-1
            },
            UpdateExpression="set player2_status = :f",
            ExpressionAttributeValues = {
                ':f': "player2 ready",
                ':v': "expired",
                },
            ConditionExpression="attribute_exists(gameId) AND player2_status <> :v",
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            #immediately from front-end, re-direct to a new game without any input
            return return_data(status_code, "even - Immediate Re-direct")
        else:
            return return_data(status_code, "even - Re-direct, something went wrong while checking player2 status")
    else:
        return return_data(200, returned_count)      
            
        
        