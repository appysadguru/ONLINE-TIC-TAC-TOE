import json
import boto3
import decimal
import time
from botocore.exceptions import ClientError

#same letter in one of these sequences leads to win
winning_sequences = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
dict_input = {"player1": "X", "player2": "O"}

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

#check if the pre-defined sequences of indexes(winning_sequences) have same consecutive letters in the given list(board_list)
def sequence_check(board_list):
    
    for sequence in winning_sequences:
        
        sequence_str = board_list[sequence[0]]+board_list[sequence[1]]+board_list[sequence[2]]
    
        if sequence_str =="XXX":
            return 'player1'
            
        elif sequence_str == "OOO":
            return 'player2'
            
dynamodb = boto3.resource("dynamodb", region_name='us-east-2')
table = dynamodb.Table('Game')

# after updating the game with the given input('input_position'), check if a sequence is formed and return the result accordingly
def lambda_handler(event, context):
    
    data = json.loads(event["body"])
    gameId = data["gameId"]
    which_player = data["which_player"]
    input_position = data["input_position"]
    
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
    
        entered_inputs = response['Item']['entered_inputs']
        
        board_list = response['Item']['board_list']
        
        entered_inputs.append(input_position)
        
        board_list[input_position-1] = dict_input[which_player]
        
        result = sequence_check(board_list)
        
        if result == "player1":
            pass
        elif result == "player2":
            pass
        elif len(entered_inputs) == 9:
            result = "tie"
        else:
            result = "keep going"
        
        try:
            response2 = table.update_item(
                Key={
                    'gameId': gameId,
                },
                UpdateExpression="set #en = :ev, #bn = :bv, #rn = :rv",
                ExpressionAttributeNames={'#en': 'entered_inputs', '#bn': 'board_list', '#rn': 'result'},
                ExpressionAttributeValues={':ev': entered_inputs, ':bv': board_list, ':rv': result},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            status_code = e.response['ResponseMetadata']['HTTPStatusCode']
            return return_data(status_code, e.response["Error"]["Message"])
        else:
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            return return_data(status_code, {"board_list": board_list, "entered_inputs": entered_inputs, "result": result})
    
    