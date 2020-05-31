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

# increment and return the 'count' field of the first game item
def lambda_handler(event, context):
    try:
        response = table.update_item(
            Key={
                'gameId': 0,
            },
            UpdateExpression="set #c = #c + :r",
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':r': 1},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, "odd - Re-direct, something went wrong while updating the game count")
    else:
        returned_count = response["Attributes"]["count"]
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, returned_count)
        
        
        
        
        
        
