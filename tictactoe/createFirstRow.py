import json
import boto3
import decimal
    
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
            
def lambda_handler(event, context):
    # TODO implement
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Game')
    
    response = table.put_item(
        Item={
            'gameId': 0,
            'count': 0,
            }
        }
    )
    
    print("result: ", json.dumps(response, indent=4, cls=DecimalEncoder))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
