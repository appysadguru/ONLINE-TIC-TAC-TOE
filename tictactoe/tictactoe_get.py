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

# return the entire item of the given partition key gameId
def lambda_handler(event, context):
    
    data = event["queryStringParameters"]
    gameId = int(data["gameId"])
    
    try:
        response = table.get_item(
            Key={
                "gameId": gameId
            }
        )
    except ClientError as e:
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, e.response["Error"]["Message"]+" something went wrong while getting data")
    else:
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        return return_data(status_code, response["Item"])

        
        
        
        
